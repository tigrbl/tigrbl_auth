# tba-protocol-oauth

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oauth/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oauth/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oauth/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/50-protocols"><img alt="Layer: 50 protocols" src="https://img.shields.io/badge/Layer-50%20protocols-0a7f5a"></a>
<a href="https://pypi.org/project/tba-protocol-oauth/"><img alt="PyPI version for tba-protocol-oauth" src="https://img.shields.io/pypi/v/tba-protocol-oauth?label=tba-protocol-oauth%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-protocol-oauth"><img alt="Monthly PyPI downloads for tba-protocol-oauth" src="https://static.pepy.tech/badge/tba-protocol-oauth/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oauth/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

tba-protocol-oauth is the protocol-facing package name for OAuth 2.x, OAuth 2.1 profile behavior, and OAuth extension RFC surfaces. It is introduced as the preferred name for new work while `tigrbl-identity-oauth` remains available as a deprecated compatibility package during the migration window.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_protocol_oauth import capability_report

report = capability_report()
assert report
print(sorted(report))
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-protocol-oauth==0.4.0.dev2" python quickstart.py
```

The command prints the keys in the package's capability report.

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

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oauth/src/tba_protocol_oauth/__init__.py).
