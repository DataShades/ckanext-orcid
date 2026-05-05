import requests
from unittest.mock import MagicMock, patch

from ckanext.orcid import auth as orcid_auth

import pytest


@pytest.mark.parametrize(
    ("sandbox", "expected_base"),
    [
        (False, "https://orcid.org"),
        (True, "https://sandbox.orcid.org"),
    ],
)
def test_build_auth_url_contains_base(sandbox, expected_base, ckan_config, monkeypatch):
    monkeypatch.setitem(ckan_config, "ckanext.orcid.sandbox", sandbox)
    monkeypatch.setitem(ckan_config, "ckanext.orcid.client_id", "test-client")
    url = orcid_auth.build_auth_url("https://example.com/callback", "mystate")
    assert url.startswith(expected_base)


def test_build_auth_url_contains_required_params(ckan_config, monkeypatch):
    monkeypatch.setitem(ckan_config, "ckanext.orcid.sandbox", False)
    monkeypatch.setitem(ckan_config, "ckanext.orcid.client_id", "test-client")
    url = orcid_auth.build_auth_url("https://example.com/callback", "mystate")
    assert "client_id=test-client" in url
    assert "response_type=code" in url
    assert "state=mystate" in url
    assert "scope=%2Fauthenticate" in url


def test_exchange_code_returns_none_on_request_error(ckan_config, monkeypatch):
    monkeypatch.setitem(ckan_config, "ckanext.orcid.sandbox", False)
    monkeypatch.setitem(ckan_config, "ckanext.orcid.client_id", "test-client")
    monkeypatch.setitem(ckan_config, "ckanext.orcid.client_secret", "test-secret")

    with patch(
        "ckanext.orcid.auth.requests.post",
        side_effect=requests.exceptions.ConnectionError,
    ):
        result = orcid_auth.exchange_code("somecode", "https://example.com/callback")
    assert result is None


def test_exchange_code_returns_json_on_success(ckan_config, monkeypatch):
    monkeypatch.setitem(ckan_config, "ckanext.orcid.sandbox", False)
    monkeypatch.setitem(ckan_config, "ckanext.orcid.client_id", "test-client")
    monkeypatch.setitem(ckan_config, "ckanext.orcid.client_secret", "test-secret")

    mock_response = MagicMock()
    mock_response.json.return_value = {
        "access_token": "token123",
        "orcid": "0000-0002-1825-0097",
        "name": "Test User",
    }
    mock_response.raise_for_status.return_value = None

    with patch("ckanext.orcid.auth.requests.post", return_value=mock_response):
        result = orcid_auth.exchange_code("code123", "https://example.com/callback")

    assert result is not None
    assert result["orcid"] == "0000-0002-1825-0097"
    assert result["access_token"] == "token123"
