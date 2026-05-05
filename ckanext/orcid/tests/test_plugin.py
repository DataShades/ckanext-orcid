from __future__ import annotations

import pytest


@pytest.mark.usefixtures("with_plugins", "clean_db")
class TestOrcidLogin:
    def test_login_page_has_orcid_button(self, app):
        response = app.get("/user/login")
        assert "Login with ORCID" in response.body

    def test_login_redirects_to_orcid(self, app, ckan_config, monkeypatch):
        monkeypatch.setitem(ckan_config, "ckanext.orcid.client_id", "test-client")
        monkeypatch.setitem(ckan_config, "ckanext.orcid.sandbox", False)
        response = app.get("/orcid/login", follow_redirects=False)
        assert response.status_code == 302
        assert "orcid.org/oauth/authorize" in response.headers["Location"]

    def test_callback_with_missing_state_redirects_to_login(self, app):
        response = app.get("/orcid/callback?code=abc&state=bad", follow_redirects=False)
        assert response.status_code == 302
        assert "/user/login" in response.headers["Location"]

    def test_callback_with_error_param_redirects_to_login(self, app):
        response = app.get("/orcid/callback?error=access_denied", follow_redirects=False)
        assert response.status_code == 302
        assert "/user/login" in response.headers["Location"]
