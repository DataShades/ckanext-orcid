from ckanext.orcid import utils

import ckan.plugins.toolkit as tk


def orcid_profile_url(orcid_id: str) -> str:
    base_url = utils.get_base_url()

    if tk.config.get("ckanext.orcid.sandbox"):
        return f"{base_url}/{orcid_id}"
    return f"{base_url}/{orcid_id}"
