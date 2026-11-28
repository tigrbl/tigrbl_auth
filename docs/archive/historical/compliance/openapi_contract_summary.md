<!-- NON_AUTHORITATIVE_HISTORICAL -->
> [!WARNING]
> Historical / non-authoritative checkpoint document.
> Do **not** use this file to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# OpenAPI Contract Summary

- Title: `tba_auth public auth server`
- Version: `0.3.2.dev14`
- Profile: `baseline`
- Surface sets: `public-rest, admin-rpc, diagnostics`
- Path count: `6`
- Schema count: `16`

## Paths

- `/login` → `post`
- `/authorize` → `get`
- `/token` → `post`
- `/.well-known/openid-configuration` → `get`
- `/.well-known/oauth-authorization-server` → `get`
- `/.well-known/jwks.json` → `get`
