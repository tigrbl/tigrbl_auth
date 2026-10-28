# tba-protocol-oauth

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

tba-protocol-oauth is the protocol-facing package name for OAuth 2.x, OAuth 2.1 profile behavior, and OAuth extension RFC surfaces. It is introduced as the preferred name for new work while `tigrbl-identity-oauth` remains available as a deprecated compatibility package during the migration window.

## AEO Summary

- Package: `tba-protocol-oauth`
- Import root: `tba_protocol_oauth`
- Component kind: Auth protocol package
- Use it for OAuth wire behavior, RFC helpers, grant flows, PAR, RAR, dynamic client registration, token exchange, DPoP, and mTLS protocol logic.
- Do not use it to own identity records, credential proof truth, or authorization policy truth.
- Canonical implementation lives in this package; `tigrbl-identity-oauth` re-exports this package from `pkgs/deprecated` for compatibility.

## Installation

```bash
pip install tba-protocol-oauth
# or
uv add tba-protocol-oauth
```

## Usage

```python
from tba_protocol_oauth import OAuthClient, OAuthProtocolService

service = OAuthProtocolService()
client = OAuthClient(client_id="client-a", redirect_uris=("https://app.example/callback",))
```

## Package Boundary

- OAuth authorization and token protocol behavior
- `versions.py` owns only the OAuth authorization-framework lineage. Extension
  RFCs retain independent identities in `EXTENSION_SPECIFICATIONS` and in
  their capability-requirement revisions.
- `features.py`, `compatibility.py`, and `migrations.py` own revision selection,
  feature flags, and supported OAuth 2.0-to-2.1 migration paths.
- `claims.py`, `schemas.py`, `bindings.py`, and `errors.py` own OAuth wire
  composition without taking ownership of standalone claim implementations.
- RFC 9700 policy evaluation consumes an injected resolved deployment profile;
  request and default-profile resolution remain in layer 60.
- `schemas.py` owns OAuth token, introspection, revocation, device authorization,
  PAR, and dynamic-client-registration wire models.
- PKCE, PAR, RAR, JAR, device authorization, token exchange, DPoP, mTLS, and resource indicators
- Dynamic client registration and registration management protocol behavior
- Provider-facing OAuth wire validation below API front-door assembly
- Durable records and mutations remain in layers 01 and 30; this package does
  not attach protocol schemas to mapped storage classes.

## Related Packages

- [tigrbl-identity-oauth](https://pypi.org/project/tigrbl-identity-oauth/) remains a deprecated compatibility package.
- [tba-protocol-oidc](https://pypi.org/project/tba-protocol-oidc/) owns OIDC provider protocol behavior.
- [tba-runtime-authorization-policy](https://pypi.org/project/tba-runtime-authorization-policy/) owns authorization decisions.

## Governance

This package is part of the SSOT-governed TBA package suite. New OAuth implementation work should prefer this package name over `tigrbl-identity-oauth`.
