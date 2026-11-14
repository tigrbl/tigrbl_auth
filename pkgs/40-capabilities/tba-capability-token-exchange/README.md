# tba-capability-token-exchange

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-token-exchange/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-token-exchange/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-token-exchange/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities"><img alt="Layer: 40 capabilities" src="https://img.shields.io/badge/Layer-40%20capabilities-0a7f5a"></a>
<a href="https://pypi.org/project/tba-capability-token-exchange/"><img alt="PyPI version for tba-capability-token-exchange" src="https://img.shields.io/pypi/v/tba-capability-token-exchange?label=tba-capability-token-exchange%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-capability-token-exchange"><img alt="Monthly PyPI downloads for tba-capability-token-exchange" src="https://static.pepy.tech/badge/tba-capability-token-exchange/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-token-exchange/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Layer-40 protocol-neutral orchestration for security-token exchange.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_capability_token_exchange import TokenExchangeCapability

assert callable(TokenExchangeCapability)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-capability-token-exchange==0.4.0.dev2" python quickstart.py
```

The import and assertion succeed when the TokenExchangeCapability entry point is available.

## Injected dependencies

A required exchange implementation receives a normalized exchange request and
trusted execution context. Runtime composition supplies verification, issuance,
durable lineage, and audit collaborators behind that implementation.

## Operations and readiness

The required operation is `exchange_token`. Construction fails when its target
is absent, so the bound required-operation set determines readiness.

## Protocol consumers

The layer-50 OAuth package maps RFC 8693 request/response fields and errors to
this capability. Other profiles must reuse the typed exchange operation rather
than fork its semantic identity.

## Non-goals

This package does not own RFC wire names, HTTP, deployment settings,
persistence, token signing, key/trust policy, or grant authorization.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-token-exchange/src/tba_capability_token_exchange/__init__.py).
