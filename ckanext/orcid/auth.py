import logging
from urllib.parse import urlencode

from ckanext.orcid import utils

import ckan.plugins.toolkit as tk
import requests

log = logging.getLogger(__name__)


def build_auth_url(redirect_uri: str, state: str) -> str:
    params = urlencode(
        {
            "client_id": tk.config.get("ckanext.orcid.client_id"),
            "response_type": "code",
            "scope": "/authenticate",
            "redirect_uri": redirect_uri,
            "state": state,
        }
    )
    return f"{utils.get_base_url()}/oauth/authorize?{params}"


def exchange_code(code: str, redirect_uri: str) -> dict | None:
    try:
        resp = requests.post(
            f"{utils.get_base_url()}/oauth/token",
            data={
                "client_id": tk.config.get("ckanext.orcid.client_id"),
                "client_secret": tk.config.get("ckanext.orcid.client_secret"),
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": redirect_uri,
            },
            headers={"Accept": "application/json"},
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException:
        log.exception("Failed to exchange ORCID authorization code")
        return None


def get_orcid_user_emails(orcid: str, token: str) -> str | None:
    """Fetch the primary email address for an ORCID user.

    TODO: it seems if we want to make a request to this API endpoint,
    we need to get an access for members API from ORCID team.

    For now, it returns 403. We wait for their response to issue us
    a new access token and a secret key.

    """
    headers = {"Accept": "application/json", "Authorization": f"Bearer {token}"}
    url = f"https://api.sandbox.orcid.org/v3.0/{orcid}/email"

    try:
        result = requests.get(url, headers=headers).json()
    except requests.exceptions.RequestException:
        log.exception("Failed to get ORCID user emails")
        return None

    primary_email = ""

    for email in result.get("email", []):
        if email.get("email") is not None and email.get("primary") is True:
            primary_email = email.get("email")
            break

    return primary_email
