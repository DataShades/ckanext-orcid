[![Tests](https://github.com/DataShades/ckanext-orcid/actions/workflows/test.yml/badge.svg)](https://github.com/DataShades/ckanext-orcid/actions/workflows/test.yml)

# ckanext-orcid

ORCID SSO integration for CKAN. Allows users to log in to your CKAN instance using their ORCID iD via OAuth2.

## Requirements

Compatibility with core CKAN versions:

| CKAN version    | Compatible? |
| --------------- | ----------- |
| 2.10            | not tested  |
| 2.11+           | yes         |


## Installation

1. Clone the source and install it on the virtualenv:
```py
git clone https://github.com/DataShades/ckanext-orcid.git
cd ckanext-orcid
pip install -e .
```

2. Add `orcid` to the `ckan.plugins` setting in your CKAN config file:
```ini
ckan.plugins = ... orcid
```

3. Run the database migration:
```py
ckan db upgrade
```

4. Configure your ORCID credentials (see [Obtaining ORCID credentials](#obtaining-orcid-credentials) below).

6. Restart CKAN.


## Obtaining ORCID credentials

To enable ORCID login you need to register an application in the ORCID developer portal and obtain a **Client ID** and **Client Secret**.

### Using the sandbox (recommended for development)

The ORCID sandbox is a free test environment with no real user data.

1. Create a sandbox account at <https://sandbox.orcid.org/register>.
2. Log in and go to **Developer Tools** (under your account name menu).
3. If prompted, verify your email address first.
4. Click **Register for the free ORCID public API**.
5. Fill in the application details:
   - **Name** — your portal's name
   - **Website URL** — your CKAN instance URL (e.g. `http://127.0.0.1:5000`)
   - **Description** — short description of your portal
   - **Redirect URIs** — add your callback URL: `http://127.0.0.1:5000/orcid/callback`
     (replace the host with your actual domain in production)
6. Save. You will be shown a **Client ID** (format `APP-XXXXXXXXXXXXXXXXX`) and **Client Secret**.

Set in your CKAN config:
```ini
  ckanext.orcid.client_id = APP-XXXXXXXXXXXXXXXXX
  ckanext.orcid.client_secret = your-client-secret
  ckanext.orcid.sandbox = true
```

### Using the production ORCID registry

1. Log in (or register) at <https://orcid.org>.
2. Go to **Developer Tools** under your account menu.
3. Click **Register for the free ORCID public API** and follow the same steps as above, using your production redirect URI (e.g. `https://yourckan.example.org/orcid/callback`).
4. Copy the **Client ID** and **Client Secret**.

Set in your CKAN config:
```ini
ckanext.orcid.client_id = APP-XXXXXXXXXXXXXXXXX
ckanext.orcid.client_secret = your-client-secret
```

> **Note:** `ckanext.orcid.sandbox` defaults to `false`, so omit it (or set it to `false`) for production.

### Members API

Email retrieval from ORCID requires access to the **ORCID Members API**, which is only available to ORCID member organisations. The public API used above supports authentication (verifying a user's identity) but not reading private profile data such as email addresses. If your organisation is an ORCID member, contact ORCID support to obtain member API credentials and a separate client ID/secret with the `/read-limited` scope.


## Config settings

| Setting | Required | Default | Description |
| ------- | -------- | ------- | ----------- |
| `ckanext.orcid.client_id` | yes | — | OAuth2 Client ID from the ORCID developer portal |
| `ckanext.orcid.client_secret` | yes | — | OAuth2 Client Secret from the ORCID developer portal |
| `ckanext.orcid.sandbox` | no | `false` | Set to `true` to use the ORCID sandbox environment |


## Tests
```py
pytest --ckan-ini=test.ini
```

## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
