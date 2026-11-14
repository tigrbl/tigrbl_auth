# tba-capability-authorization-request-staging

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-authorization-request-staging/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-authorization-request-staging/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-authorization-request-staging/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities"><img alt="Layer: 40 capabilities" src="https://img.shields.io/badge/Layer-40%20capabilities-0a7f5a"></a>
<a href="https://pypi.org/project/tba-capability-authorization-request-staging/"><img alt="PyPI version for tba-capability-authorization-request-staging" src="https://img.shields.io/pypi/v/tba-capability-authorization-request-staging?label=tba-capability-authorization-request-staging%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-capability-authorization-request-staging"><img alt="Monthly PyPI downloads for tba-capability-authorization-request-staging" src="https://static.pepy.tech/badge/tba-capability-authorization-request-staging/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-authorization-request-staging/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Layer-40 orchestration for persisting an already normalized and authenticated
pushed authorization request.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_capability_authorization_request_staging import PushedAuthorizationCapability

assert callable(PushedAuthorizationCapability)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-capability-authorization-request-staging==0.4.0.dev2" python quickstart.py
```

The import and assertion succeed when the PushedAuthorizationCapability entry point is available.

## Injected dependencies

A durable request-URI creation callable is required. A durable audit callable
is optional. Both may be synchronous or asynchronous.

## Operations and readiness

`push_authorization_request` is required; `record_audit_event` is optional.
Readiness follows the persistence binding, and the report exposes audit
availability separately.

## Protocol consumers

The layer-50 OAuth package maps RFC 9126 PAR to this capability. OIDC and HAIP
consume it through their configured OAuth/FAPI compositions where applicable.

## Non-goals

This package does not parse HTTP, authenticate clients, validate request
objects/DPoP, choose FAPI policy or RFC errors, open sessions, or own state.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-authorization-request-staging/src/tba_capability_authorization_request_staging/__init__.py).
