from flask import Blueprint, Response

blueprint = Blueprint("orcid", __name__, url_prefix="/orcid")


@blueprint.route("/login")
def login() -> Response:
    return Response("login")


@blueprint.route("/callback")
def callback() -> Response:
    return Response("callback")
