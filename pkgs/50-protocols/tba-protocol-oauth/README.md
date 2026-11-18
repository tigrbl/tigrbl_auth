# tba-protocol-oauth

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oauth/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oauth/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-protocol-oauth%3D%3D0.4.0.dev4/pkgs/50-protocols/tba-protocol-oauth/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-protocol-oauth%3D%3D0.4.0.dev4/pkgs/50-protocols/tba-protocol-oauth/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/50-protocols"><img alt="Layer: 50 protocols" src="https://img.shields.io/badge/Layer-50%20protocols-0a7f5a"></a>
<a href="https://pypi.org/project/tba-protocol-oauth/"><img alt="PyPI version for tba-protocol-oauth" src="https://img.shields.io/pypi/v/tba-protocol-oauth?label=tba-protocol-oauth%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-protocol-oauth"><img alt="Monthly PyPI downloads for tba-protocol-oauth" src="https://static.pepy.tech/badge/tba-protocol-oauth/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oauth/README.md"><img alt="README hits for tba-protocol-oauth" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oauth/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oauth/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

tba-protocol-oauth is the protocol-facing package name for OAuth 2.x, OAuth 2.1 profile behavior, and OAuth extension RFC surfaces. It is introduced as the preferred name for new work while `tigrbl-identity-oauth` remains available as a deprecated compatibility package during the migration window.

## AEO Summary

- Package: `tba-protocol-oauth`
- Import root: `tba_protocol_oauth`
- Component kind: Auth protocol package
- Use it for OAuth wire behavior, RFC helpers, grant flows, PAR, RAR, dynamic client registration, token exchange, DPoP, and mTLS protocol logic.
- Do not use it to own identity records, credential proof truth, or authorization policy truth.
- Canonical implementation lives in this package; `tigrbl-identity-oauth` re-exports this package from `pkgs/deprecated` for compatibility.

## When to use it

Choose `tba-protocol-oauth` for this responsibility: OAuth 2.x and OAuth 2.1 profile protocol implementation package for the TBA package suite. Its `50-protocols` placement keeps protocol semantics and projections separate from deployment hosting or ownership of persistence implementations.

## Installation

```bash
pip install tba-protocol-oauth
# or
uv add tba-protocol-oauth
```

Install the current `tba-protocol-oauth` source checkout when working ahead of a PyPI release:

```bash
uv pip install ./pkgs/50-protocols/tba-protocol-oauth
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_protocol_oauth import capability_report

report = capability_report()
assert report
print(sorted(report))
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-protocol-oauth==0.4.0.dev4" python quickstart.py
```

The command prints the keys in the package's capability report.

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

## Injected dependencies

Explicit construction inputs and collaborators for `tba-protocol-oauth`:

- `OAuthProtocolError` construction inputs: `code`, `description`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oauth/src/tba_protocol_oauth/errors.py).
- `migrate_client` construction inputs: `source`, `target`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oauth/src/tba_protocol_oauth/migrations.py).
- `OAuthProtocolService` construction inputs: `operations`, `now`, `repository`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oauth/src/tba_protocol_oauth/protocol.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-protocol-oauth` exposes protocol semantics and projections. Public operations found in its source:

- `capability_report` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oauth/src/tba_protocol_oauth/__init__.py).
- `compose_oauth_claim_set` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oauth/src/tba_protocol_oauth/claims.py).
- `compose_dpop_proof_claim_set` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oauth/src/tba_protocol_oauth/claims.py).
- `compose_token_exchange_claim_set` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oauth/src/tba_protocol_oauth/claims.py).
- `compatibility` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oauth/src/tba_protocol_oauth/compatibility.py).
- `supports` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oauth/src/tba_protocol_oauth/features.py).
- `migrate_client` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oauth/src/tba_protocol_oauth/migrations.py).
- `InMemoryOAuthState.save_client` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oauth/src/tba_protocol_oauth/protocol.py).
- `InMemoryOAuthState.get_client` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oauth/src/tba_protocol_oauth/protocol.py).
- `InMemoryOAuthState.save_device_authorization` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oauth/src/tba_protocol_oauth/protocol.py).
- `InMemoryOAuthState.get_device_authorization` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oauth/src/tba_protocol_oauth/protocol.py).
- `InMemoryOAuthState.remember_dpop_jti` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oauth/src/tba_protocol_oauth/protocol.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

The following layer-50 manifests directly depend on `tba-protocol-oauth`:

- [tba-protocol-oauth-protected-resource](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oauth-protected-resource/README.md)
- [tba-protocol-oidc](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc/README.md)

Other direct consumers include [tba-app-backend-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-core/README.md), [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tba-auth/README.md), [tba-router-oauth-authorization-server-metadata](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-authorization-server-metadata/README.md), [tba-router-oauth-device-authorization](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-device-authorization/README.md), [tba-router-oauth-introspection](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-introspection/README.md), [tba-router-oauth-protected-resource-metadata](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-protected-resource-metadata/README.md).

## Non-goals

`tba-protocol-oauth` does not take ownership of deployment hosting or ownership of persistence implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

- [tigrbl-identity-oauth](https://pypi.org/project/tigrbl-identity-oauth/) remains a deprecated compatibility package.
- [tba-protocol-oidc](https://pypi.org/project/tba-protocol-oidc/) owns OIDC provider protocol behavior.
- [tba-runtime-authorization-policy](https://pypi.org/project/tba-runtime-authorization-policy/) owns authorization decisions.

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/50-protocols/tba-protocol-oauth)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oauth/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oauth/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oauth/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-protocol-oauth/)

## Governance

This package is part of the SSOT-governed TBA package suite. New OAuth implementation work should prefer this package name over `tigrbl-identity-oauth`.

`tba-protocol-oauth` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `50-protocols` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oauth/src/tba_protocol_oauth/__init__.py).
