# tba-capability-token-issuance

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-token-issuance/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-token-issuance/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-token-issuance/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities"><img alt="Layer: 40 capabilities" src="https://img.shields.io/badge/Layer-40%20capabilities-0a7f5a"></a>
<a href="https://pypi.org/project/tba-capability-token-issuance/"><img alt="PyPI version for tba-capability-token-issuance" src="https://img.shields.io/pypi/v/tba-capability-token-issuance?label=tba-capability-token-issuance%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-capability-token-issuance"><img alt="Monthly PyPI downloads for tba-capability-token-issuance" src="https://static.pepy.tech/badge/tba-capability-token-issuance/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-token-issuance/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Layer-40 orchestration for token-pair issuance and refresh rotation.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_capability_token_issuance import TokenIssuanceCapability

assert callable(TokenIssuanceCapability)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-capability-token-issuance==0.4.0.dev2" python quickstart.py
```

The import and assertion succeed when the TokenIssuanceCapability entry point is available.

## Injected dependencies

Required callables issue a token pair and redeem/rotate a refresh token. An
optional audit callable records lifecycle events. Runtime composition supplies
signing providers and durable layer-30 state behind these callables.

## Operations and readiness

Required operations are `issue_token_pair` and `redeem_refresh_token`; optional
`record_audit_event` reports unavailable when unbound. Readiness requires both
issuance targets.

## Protocol consumers

Layer-50 OAuth grant/token bindings and OIDC token flows consume these
operations with explicit token profiles.

## Non-goals

This package does not parse requests, authenticate clients, select grants,
sign tokens, choose token profiles, open sessions, or own lifecycle state.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-token-issuance/src/tba_capability_token_issuance/__init__.py).
