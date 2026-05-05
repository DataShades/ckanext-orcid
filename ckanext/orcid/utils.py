import re

import ckan.plugins.toolkit as tk
import requests

ORCID_PATTERN = re.compile(r"^\d{4}-\d{4}-\d{4}-\d{3}[0-9X]$")


def is_valid_orcid(orcid: str) -> bool:
    if not check_pattern(orcid):
        return False

    return check_api(orcid)


def check_pattern(orcid: str) -> bool:
    return bool(ORCID_PATTERN.match(orcid))


def check_api(orcid: str) -> bool:
    try:
        resp = requests.get(f"https://pub.orcid.org/v3.0/{orcid}")
    except requests.exceptions.RequestException:
        return False
    else:
        return resp.status_code == requests.status_codes.codes.OK


def get_base_url() -> str:
    return "https://sandbox.orcid.org" if tk.config.get("ckanext.orcid.sandbox") else "https://orcid.org"
