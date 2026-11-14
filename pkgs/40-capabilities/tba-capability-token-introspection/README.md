# tba-capability-token-introspection

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-token-introspection/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-token-introspection/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-token-introspection/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities"><img alt="Layer: 40 capabilities" src="https://img.shields.io/badge/Layer-40%20capabilities-0a7f5a"></a>
<a href="https://pypi.org/project/tba-capability-token-introspection/"><img alt="PyPI version for tba-capability-token-introspection" src="https://img.shields.io/pypi/v/tba-capability-token-introspection?label=tba-capability-token-introspection%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-capability-token-introspection"><img alt="Monthly PyPI downloads for tba-capability-token-introspection" src="https://static.pepy.tech/badge/tba-capability-token-introspection/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-token-introspection/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Layer-40 protocol-neutral orchestration for typed token-state introspection.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_capability_token_introspection import TokenIntrospectionCapability

assert callable(TokenIntrospectionCapability)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-capability-token-introspection==0.4.0.dev2" python quickstart.py
```

The import and assertion succeed when the TokenIntrospectionCapability entry point is available.

## Injected dependencies

A required synchronous or asynchronous lookup callable accepts a
`TokenIntrospectionRequest` and returns a typed result or normalized mapping.
It normally composes durable token state with profile validation below layer 40.

## Operations and readiness

The required operation is `introspect_token`. Construction fails without its
target and the capability report exposes the effective binding and state.

## Protocol consumers

The layer-50 OAuth package maps RFC 7662 to this capability; the layer-50
resource-server package may consume the normalized result for authorization.

## Non-goals

This package does not parse HTTP, authenticate callers, open sessions, verify
cryptography, choose protocol errors, or publish routes.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-token-introspection/src/tba_capability_token_introspection/__init__.py).
