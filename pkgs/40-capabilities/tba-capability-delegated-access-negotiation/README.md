# tba-capability-delegated-access-negotiation

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-delegated-access-negotiation/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-delegated-access-negotiation/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-delegated-access-negotiation/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities"><img alt="Layer: 40 capabilities" src="https://img.shields.io/badge/Layer-40%20capabilities-0a7f5a"></a>
<a href="https://pypi.org/project/tba-capability-delegated-access-negotiation/"><img alt="PyPI version for tba-capability-delegated-access-negotiation" src="https://img.shields.io/pypi/v/tba-capability-delegated-access-negotiation?label=tba-capability-delegated-access-negotiation%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-capability-delegated-access-negotiation"><img alt="Monthly PyPI downloads for tba-capability-delegated-access-negotiation" src="https://static.pepy.tech/badge/tba-capability-delegated-access-negotiation/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-delegated-access-negotiation/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Layer-40 protocol-neutral composition for requesting, continuing, and rotating
negotiated grants.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_capability_delegated_access_negotiation import GrantNegotiationCapability

assert callable(GrantNegotiationCapability)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-capability-delegated-access-negotiation==0.4.0.dev2" python quickstart.py
```

The import and assertion succeed when the GrantNegotiationCapability entry point is available.

## Injected dependencies

A grant-request target is required. Continuation and access-token rotation
targets are optional. Layer-60 composition may build these targets from
layer-20 key/token providers and the layer-30 GNAP grant-state operations.

## Operations and readiness

`request_grant` is required. `continue_grant` and `rotate_access_token` are
optional and report unavailable when unbound. Readiness follows the required
request target; no grant or token state is retained in this package.

## Protocol consumers

The layer-50 GNAP package maps RFC 9635 grant request, continuation, and token
rotation semantics to these operations. Other grant-negotiation protocols may
reuse the normalized contracts through their own mappings.

## Non-goals

This package does not parse GNAP messages, validate key proofs, mint tokens,
generate continuation secrets, open database sessions, or mount routes.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-delegated-access-negotiation/src/tba_capability_delegated_access_negotiation/__init__.py).
