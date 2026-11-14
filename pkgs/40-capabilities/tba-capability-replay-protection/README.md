# tba-capability-replay-protection

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-replay-protection/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-replay-protection/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-replay-protection/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities"><img alt="Layer: 40 capabilities" src="https://img.shields.io/badge/Layer-40%20capabilities-0a7f5a"></a>
<a href="https://pypi.org/project/tba-capability-replay-protection/"><img alt="PyPI version for tba-capability-replay-protection" src="https://img.shields.io/pypi/v/tba-capability-replay-protection?label=tba-capability-replay-protection%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-capability-replay-protection"><img alt="Monthly PyPI downloads for tba-capability-replay-protection" src="https://static.pepy.tech/badge/tba-capability-replay-protection/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-replay-protection/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Layer-40 orchestration for protocol-neutral atomic replay reservations.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_capability_replay_protection import ReplayCapabilityDescriptor

assert callable(ReplayCapabilityDescriptor)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-capability-replay-protection==0.4.0.dev2" python quickstart.py
```

The import and assertion succeed when the ReplayCapabilityDescriptor entry point is available.

## Injected dependencies

A required `ReplayReservationPort` performs the reservation. Layer 60 selects
an ephemeral layer-20 provider or durable layer-30 operation and supplies the
allowed normalized namespaces.

## Operations and readiness

The required operation is `check_and_reserve`. Readiness, health, status,
provider identity, persistence mode, and namespaces are derived from the
effective provider binding and included in the capability report.

## Protocol consumers

OAuth, OIDC, OID4VCI, OID4VP, SET, EAT, GNAP, and HAIP layer-50 packages may
map their nonce/JTI/proof replay requirements to this operation.

## Non-goals

This package does not interpret protocol wire fields, choose retention windows,
own tables, open sessions, or silently claim durable persistence.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-replay-protection/src/tba_capability_replay_protection/__init__.py).
