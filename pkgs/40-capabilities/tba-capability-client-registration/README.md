# tba-capability-client-registration

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-client-registration/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-client-registration/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-client-registration/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities"><img alt="Layer: 40 capabilities" src="https://img.shields.io/badge/Layer-40%20capabilities-0a7f5a"></a>
<a href="https://pypi.org/project/tba-capability-client-registration/"><img alt="PyPI version for tba-capability-client-registration" src="https://img.shields.io/pypi/v/tba-capability-client-registration?label=tba-capability-client-registration%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-capability-client-registration"><img alt="Monthly PyPI downloads for tba-capability-client-registration" src="https://static.pepy.tech/badge/tba-capability-client-registration/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-client-registration/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Layer-40 orchestration for the protocol-neutral lifecycle of a registered
client.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_capability_client_registration import ClientRegistrationCapability

assert callable(ClientRegistrationCapability)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-capability-client-registration==0.4.0.dev2" python quickstart.py
```

The import and assertion succeed when the ClientRegistrationCapability entry point is available.

## Injected dependencies

Create, read, update, and disable callables are required and normally adapt
layer-30 table operations. A durable audit callable is optional. Every
collaborator may be synchronous or asynchronous.

## Operations and readiness

Operations are `register_client`, `get_registration`, `update_registration`,
`disable_registration`, and optional `record_audit_event`. Readiness is true
only when all four lifecycle targets are bound; the report separately exposes
whether audit recording is available.

## Protocol consumers

The layer-50 OAuth package maps RFC 7591/7592 behavior to this capability; OIDC
uses that OAuth registration mapping where enabled.

## Non-goals

This package does not parse HTTP, generate/hash secrets, validate OAuth
metadata, select protocol errors, open storage sessions, or own registration
state.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-client-registration/src/tba_capability_client_registration/__init__.py).
