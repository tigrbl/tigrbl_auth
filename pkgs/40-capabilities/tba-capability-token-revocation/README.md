# tba-capability-token-revocation

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-token-revocation/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-token-revocation/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-token-revocation/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities"><img alt="Layer: 40 capabilities" src="https://img.shields.io/badge/Layer-40%20capabilities-0a7f5a"></a>
<a href="https://pypi.org/project/tba-capability-token-revocation/"><img alt="PyPI version for tba-capability-token-revocation" src="https://img.shields.io/pypi/v/tba-capability-token-revocation?label=tba-capability-token-revocation%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-capability-token-revocation"><img alt="Monthly PyPI downloads for tba-capability-token-revocation" src="https://static.pepy.tech/badge/tba-capability-token-revocation/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-token-revocation/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Layer-40 orchestration for protocol-neutral durable token revocation.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_capability_token_revocation import TokenRevocationCapability

assert callable(TokenRevocationCapability)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-capability-token-revocation==0.4.0.dev2" python quickstart.py
```

The import and assertion succeed when the TokenRevocationCapability entry point is available.

## Injected dependencies

A required revocation callable mutates durable token state; an optional audit
callable records the lifecycle event. Both may be synchronous or asynchronous.

## Operations and readiness

`revoke_token` is required and `record_audit_event` is optional. Readiness
follows the revocation binding, while the report separately exposes audit
availability.

## Protocol consumers

The layer-50 OAuth package maps RFC 7009 behavior to this capability. Other
protocol profiles reuse the normalized revocation result where applicable.

## Non-goals

This package does not parse HTTP, authenticate callers, select RFC responses,
open sessions, resolve token profiles, or own revocation storage.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-token-revocation/src/tba_capability_token_revocation/__init__.py).
