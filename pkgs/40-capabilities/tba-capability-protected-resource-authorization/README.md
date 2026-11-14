# tba-capability-protected-resource-authorization

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-protected-resource-authorization/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-protected-resource-authorization/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-protected-resource-authorization/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities"><img alt="Layer: 40 capabilities" src="https://img.shields.io/badge/Layer-40%20capabilities-0a7f5a"></a>
<a href="https://pypi.org/project/tba-capability-protected-resource-authorization/"><img alt="PyPI version for tba-capability-protected-resource-authorization" src="https://img.shields.io/pypi/v/tba-capability-protected-resource-authorization?label=tba-capability-protected-resource-authorization%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-capability-protected-resource-authorization"><img alt="Monthly PyPI downloads for tba-capability-protected-resource-authorization" src="https://static.pepy.tech/badge/tba-capability-protected-resource-authorization/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-protected-resource-authorization/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Layer-40 orchestration for a protected resource's normalized authorization
decision over validated access-token material.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_capability_protected_resource_authorization import ProtectedResourceAuthorizationCapability

assert callable(ProtectedResourceAuthorizationCapability)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-capability-protected-resource-authorization==0.4.0.dev2" python quickstart.py
```

The import and assertion succeed when the ProtectedResourceAuthorizationCapability entry point is available.

## Injected dependencies

A required `ResourceServerVerifierPort` supplies token and claims verification.
The injected implementation may compose local signature validation,
introspection, sender constraints, and policy evaluation below this boundary.

## Operations and readiness

The required delegated operations are `verify_token` and `verify_claims`.
Construction fails when either operation is unavailable. The capability report
exposes both effective bindings and provider readiness.

## Protocol consumers

Layer-50 OAuth protected-resource profiles map bearer-token, JWT access-token,
introspection, DPoP, mTLS, and authorization requirements to this capability.

## Non-goals

This package does not parse HTTP, decode protocol wire formats, resolve keys,
open storage sessions, select trust anchors, or publish resource-server routes.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-protected-resource-authorization/src/tba_capability_protected_resource_authorization/__init__.py).
