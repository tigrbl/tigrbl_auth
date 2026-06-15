# OpenAPI Contract Summary

- Title: `tigrbl_auth public auth server`
- Version: `0.4.0.dev2`
- Profile: `baseline`
- Surface sets: `public-rest`
- Path count: `18`
- Schema count: `16`

## Paths

- `/login` → `post`
- `/authorize` → `get`
- `/token` → `post`
- `/account/profile` → `get, patch`
- `/account/sessions` → `delete, get`
- `/account/sessions/{session_id}` → `delete, get`
- `/account/consents` → `delete, get`
- `/account/consents/{consent_id}` → `delete, get`
- `/account/authorized-apps` → `delete, get`
- `/account/authorized-apps/{client_id}` → `delete, get`
- `/account/password/change` → `post`
- `/.well-known/openid-configuration` → `get`
- `/tenants/{tenant_slug}/.well-known/openid-configuration` → `get`
- `/realms/{realm_slug}/.well-known/openid-configuration` → `get`
- `/.well-known/oauth-authorization-server` → `get`
- `/.well-known/jwks.json` → `get`
- `/tenants/{tenant_slug}/.well-known/jwks.json` → `get`
- `/realms/{realm_slug}/.well-known/jwks.json` → `get`
