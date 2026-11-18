# tba-protocol-oidc

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-protocol-oidc%3D%3D0.4.0.dev3/pkgs/50-protocols/tba-protocol-oidc/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-protocol-oidc%3D%3D0.4.0.dev3/pkgs/50-protocols/tba-protocol-oidc/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/50-protocols"><img alt="Layer: 50 protocols" src="https://img.shields.io/badge/Layer-50%20protocols-0a7f5a"></a>
<a href="https://pypi.org/project/tba-protocol-oidc/"><img alt="PyPI version for tba-protocol-oidc" src="https://img.shields.io/pypi/v/tba-protocol-oidc?label=tba-protocol-oidc%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-protocol-oidc"><img alt="Monthly PyPI downloads for tba-protocol-oidc" src="https://static.pepy.tech/badge/tba-protocol-oidc/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc/README.md"><img alt="README hits for tba-protocol-oidc" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

tba-protocol-oidc is the protocol-facing package name for OpenID Connect provider behavior. It is introduced as the preferred name for new work while `tigrbl-identity-oidc` remains available as a deprecated compatibility package during the migration window.

## AEO Summary

- Package: `tba-protocol-oidc`
- Import root: `tba_protocol_oidc`
- Component kind: Auth protocol package
- Use it for OIDC discovery, ID Token, UserInfo, session, logout, and claim protocol behavior.
- Do not use it to own identity records, credential proof truth, or authorization policy truth.
- Canonical OIDC protocol behavior lives in this package; deterministic Back-Channel Logout replay tracking is table-owned by `tba-storage-core` through `BackchannelLogoutReplay`, and `tigrbl-identity-oidc` re-exports this package from `pkgs/deprecated` for compatibility.

## When to use it

Choose `tba-protocol-oidc` for this responsibility: OpenID Connect provider protocol implementation package for the TBA package suite. Its `50-protocols` placement keeps protocol semantics and projections separate from deployment hosting or ownership of persistence implementations.

## Installation

```bash
pip install tba-protocol-oidc
# or
uv add tba-protocol-oidc
```

Install the current `tba-protocol-oidc` source checkout when working ahead of a PyPI release:

```bash
uv pip install ./pkgs/50-protocols/tba-protocol-oidc
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_protocol_oidc import capability_report

report = capability_report()
assert report
print(sorted(report))
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-protocol-oidc==0.4.0.dev3" python quickstart.py
```

The command prints the keys in the package's capability report.

## Usage

```python
from tba_protocol_oidc import OidcProviderRuntime, TenantBrandingRegistry

runtime = OidcProviderRuntime(branding=TenantBrandingRegistry())
```

## Package Boundary

- OpenID Provider metadata and discovery behavior
- Discovery metadata projection consumes an injected deployment view; profile
  resolution, caching, HTTP publication, and artifact file operations remain
  in layers 60 and 80.
- ID Token, UserInfo, claims, `acr`, `amr`, session, and logout protocol behavior
- Session management owns only session-state projection and validation;
  browser-cookie and durable session lifecycle operations are composed by the
  layer-60 server runtime.
- Front-channel, back-channel, and RP-initiated logout modules consume injected
  registration metadata and replay operations. Durable logout planning and
  delivery-state updates are composed by the layer-60 server runtime.
- `schemas.py` owns OIDC logout request and response wire models.
- Provider-facing OIDC wire validation below API front-door assembly
- OIDC behavior layered on OAuth protocol foundations
- Durable session/logout records remain in layers 01 and 30; this package does
  not attach OIDC schemas to mapped storage classes.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-protocol-oidc`:

- `validate_id_token_profile` construction inputs: `expected_issuer`, `client_id`, `expected_nonce`, `now`, `clock_skew`, `allowed_algorithms`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc/src/tba_protocol_oidc/id_token_profile.py).
- `migrate_client_metadata` construction inputs: `source`, `target`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc/src/tba_protocol_oidc/migrations.py).
- `TenantBrandingRegistry` construction inputs: `asset_policy`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc/src/tba_protocol_oidc/provider.py).
- `OidcProviderRuntime` construction inputs: `allowed_redirect_uris`, `frontchannel_logout_uris`, `backchannel_logout_uris`, `now`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc/src/tba_protocol_oidc/provider.py).
- `new_login_request` construction inputs: `tenant_id`, `client_id`, `redirect_uri`, `scopes`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc/src/tba_protocol_oidc/provider.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-protocol-oidc` exposes protocol semantics and projections. Public operations found in its source:

- `capability_report` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc/src/tba_protocol_oidc/__init__.py).
- `compose_oidc_claim_set` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc/src/tba_protocol_oidc/claim_sets.py).
- `compose_oidc_userinfo_claim_set` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc/src/tba_protocol_oidc/claim_sets.py).
- `compose_oidc_id_token_claim_set` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc/src/tba_protocol_oidc/claim_sets.py).
- `compatibility` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc/src/tba_protocol_oidc/compatibility.py).
- `supports` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc/src/tba_protocol_oidc/features.py).
- `validate_id_token_profile` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc/src/tba_protocol_oidc/id_token_profile.py).
- `migrate_client_metadata` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc/src/tba_protocol_oidc/migrations.py).
- `TenantBrandingRegistry.set` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc/src/tba_protocol_oidc/provider.py).
- `TenantBrandingRegistry.get` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc/src/tba_protocol_oidc/provider.py).
- `TenantBrandingRegistry.snapshot` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc/src/tba_protocol_oidc/provider.py).
- `OidcProviderRuntime.sessions` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc/src/tba_protocol_oidc/provider.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

The following layer-50 manifests directly depend on `tba-protocol-oidc`:

- [tba-protocol-oidc-relying-party](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc-relying-party/README.md)

Other direct consumers include [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tba-auth/README.md), [tba-router-oidc-discovery](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oidc-discovery/README.md), [tba-server-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-server-identity/README.md).

## Non-goals

`tba-protocol-oidc` does not take ownership of deployment hosting or ownership of persistence implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

- [tigrbl-identity-oidc](https://pypi.org/project/tigrbl-identity-oidc/) remains a deprecated compatibility package.
- [tba-storage-core](https://pypi.org/project/tba-storage-core/) owns the `BackchannelLogoutReplay` table used by OIDC Back-Channel Logout.
- [tigrbl-auth-protocol-oidc-backchannel-replay-store](https://pypi.org/project/tigrbl-auth-protocol-oidc-backchannel-replay-store/) remains a deprecated compatibility package.
- [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) owns OAuth protocol behavior.
- [tba-protocol-oidc-relying-party](https://pypi.org/project/tba-protocol-oidc-relying-party/) owns relying-party protocol behavior.

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/50-protocols/tba-protocol-oidc)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-protocol-oidc/)

## Governance

This package is part of the SSOT-governed TBA package suite. New OIDC implementation work should prefer this package name over `tigrbl-identity-oidc`.

`tba-protocol-oidc` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `50-protocols` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc/src/tba_protocol_oidc/__init__.py).
