import logging
import secrets

from ckanext.orcid import auth

import ckan.plugins.toolkit as tk
from ckan import model
from flask import Blueprint, redirect, request, session, url_for

from .model import OrcidUserLink

log = logging.getLogger(__name__)

blueprint = Blueprint("orcid", __name__, url_prefix="/orcid")

STATE_KEY = "orcid_oauth_state"


@blueprint.route("/login")
def login():
    if not tk.config.get("ckanext.orcid.client_id"):
        tk.h.flash_error(
            tk._(
                "ORCID login is not configured.",
                "Set ckanext.orcid.client_id and ckanext.orcid.client_secret in your CKAN config.",
            )
        )
        return redirect(url_for("user.login"))

    state = secrets.token_urlsafe(16)
    session[STATE_KEY] = state
    redirect_uri = url_for("orcid.callback", _external=True)
    return redirect(auth.build_auth_url(redirect_uri, state))


@blueprint.route("/login/callback")
def callback():  # noqa: PLR0911
    if error := request.args.get("error"):
        tk.h.flash_error(tk._("ORCID login failed: {}").format(error))
        return redirect(url_for("user.login"))

    state = request.args.get("state")
    code = request.args.get("code")

    if not state or state != session.pop(STATE_KEY, None):
        tk.h.flash_error(tk._("ORCID login failed: invalid state parameter."))
        return redirect(url_for("user.login"))

    if not code:
        tk.h.flash_error(tk._("ORCID login failed: missing authorization code."))
        return redirect(url_for("user.login"))

    token_data = auth.exchange_code(code, url_for("orcid.callback", _external=True))
    log.debug("Received token data: %s", token_data)

    if not token_data:
        tk.h.flash_error(tk._("ORCID login failed: could not exchange authorization code."))
        return redirect(url_for("user.login"))

    orcid_id = token_data.get("orcid")
    access_token = token_data.get("access_token")
    orcid_name = token_data.get("name") or ""

    if not orcid_id or not access_token:
        tk.h.flash_error(tk._("ORCID login failed: incomplete response from ORCID."))
        return redirect(url_for("user.login"))

    user_email = auth.get_orcid_user_emails(orcid_id, access_token)

    log.info("Found ORCID user %s with email %s", orcid_id, user_email)

    if link := OrcidUserLink.get(orcid_id):
        link.access_token = access_token
        model.Session.commit()
        user_obj = model.User.get(link.user_id)
    else:
        user_obj = _find_or_create_user(orcid_id, orcid_name, access_token)

    if not user_obj or not user_obj.is_active:
        tk.h.flash_error(tk._("ORCID login failed: user account not found or inactive."))
        return redirect(url_for("user.login"))

    tk.login_user(user_obj)

    return redirect(tk.url_for("home.index"))


def _find_or_create_user(orcid_id: str, orcid_name: str, access_token: str) -> model.User | None:
    username = "orcid_" + orcid_id.replace("-", "")
    user_obj = model.User.by_name(username)

    if not user_obj:
        data_dict = {
            "name": username,
            "email": f"orcid+{orcid_id}@placeholder.invalid",
            "password": secrets.token_urlsafe(32),
            "fullname": orcid_name or orcid_id,
        }
        try:
            user_dict = tk.get_action("user_create")({"ignore_auth": True}, data_dict)
            user_obj = model.User.get(user_dict["id"])
        except tk.ValidationError:
            log.exception("Failed to create CKAN user for ORCID %s", orcid_id)
            return None

    if user_obj:
        OrcidUserLink.add(orcid_id, user_obj.id, access_token)

    return user_obj
