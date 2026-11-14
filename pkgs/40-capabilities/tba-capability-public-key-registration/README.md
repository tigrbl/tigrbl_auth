# tba-capability-public-key-registration

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-public-key-registration/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-public-key-registration/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-public-key-registration/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities"><img alt="Layer: 40 capabilities" src="https://img.shields.io/badge/Layer-40%20capabilities-0a7f5a"></a>
<a href="https://pypi.org/project/tba-capability-public-key-registration/"><img alt="PyPI version for tba-capability-public-key-registration" src="https://img.shields.io/pypi/v/tba-capability-public-key-registration?label=tba-capability-public-key-registration%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-capability-public-key-registration"><img alt="Monthly PyPI downloads for tba-capability-public-key-registration" src="https://static.pepy.tech/badge/tba-capability-public-key-registration/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-public-key-registration/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Protocol-neutral orchestration for beginning and completing verified public-key credential registration.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_capability_public_key_registration import PublicKeyRegistrationCapability

assert callable(PublicKeyRegistrationCapability)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-capability-public-key-registration==0.4.0.dev2" python quickstart.py
```

The import and assertion succeed when the PublicKeyRegistrationCapability entry point is available.

## Injected dependencies

Begin and completion callables backed by durable ceremony operations, protocol verification, and credential insertion.

## Operations and readiness

`begin_public_key_registration` and `complete_public_key_registration` are required; readiness is false until both are bound.

## Protocol consumers

WebAuthn and versioned FIDO2 server profiles map their registration messages to these operations.

## Non-goals

This package owns neither WebAuthn wire parsing nor database tables, HTTP routes, keys, or trust anchors.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-public-key-registration/src/tba_capability_public_key_registration/__init__.py).
