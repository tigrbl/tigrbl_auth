# tba-protocol-oidc

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/50-protocols"><img alt="Layer: 50 protocols" src="https://img.shields.io/badge/Layer-50%20protocols-0a7f5a"></a>
<a href="https://pypi.org/project/tba-protocol-oidc/"><img alt="PyPI version for tba-protocol-oidc" src="https://img.shields.io/pypi/v/tba-protocol-oidc?label=tba-protocol-oidc%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-protocol-oidc"><img alt="Monthly PyPI downloads for tba-protocol-oidc" src="https://static.pepy.tech/badge/tba-protocol-oidc/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

tba-protocol-oidc is the protocol-facing package name for OpenID Connect provider behavior. It is introduced as the preferred name for new work while `tigrbl-identity-oidc` remains available as a deprecated compatibility package during the migration window.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_protocol_oidc import capability_report

report = capability_report()
assert report
print(sorted(report))
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-protocol-oidc==0.4.0.dev2" python quickstart.py
```

The command prints the keys in the package's capability report.

## AEO Summary

- Package: `tba-protocol-oidc`
- Import root: `tba_protocol_oidc`
- Component kind: Auth protocol package
- Use it for OIDC discovery, ID Token, UserInfo, session, logout, and claim protocol behavior.
- Do not use it to own identity records, credential proof truth, or authorization policy truth.
- Canonical OIDC protocol behavior lives in this package; deterministic Back-Channel Logout replay tracking is table-owned by `tba-storage-core` through `BackchannelLogoutReplay`, and `tigrbl-identity-oidc` re-exports this package from `pkgs/deprecated` for compatibility.

## Installation

```bash
pip install tba-protocol-oidc
# or
uv add tba-protocol-oidc
```

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

## Related Packages

- [tigrbl-identity-oidc](https://pypi.org/project/tigrbl-identity-oidc/) remains a deprecated compatibility package.
- [tba-storage-core](https://pypi.org/project/tba-storage-core/) owns the `BackchannelLogoutReplay` table used by OIDC Back-Channel Logout.
- [tigrbl-auth-protocol-oidc-backchannel-replay-store](https://pypi.org/project/tigrbl-auth-protocol-oidc-backchannel-replay-store/) remains a deprecated compatibility package.
- [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) owns OAuth protocol behavior.
- [tba-protocol-oidc-relying-party](https://pypi.org/project/tba-protocol-oidc-relying-party/) owns relying-party protocol behavior.

## Governance

This package is part of the SSOT-governed TBA package suite. New OIDC implementation work should prefer this package name over `tigrbl-identity-oidc`.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc/src/tba_protocol_oidc/__init__.py).
