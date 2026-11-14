# tba-capability-security-event-delivery

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-security-event-delivery/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-security-event-delivery/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-security-event-delivery/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities"><img alt="Layer: 40 capabilities" src="https://img.shields.io/badge/Layer-40%20capabilities-0a7f5a"></a>
<a href="https://pypi.org/project/tba-capability-security-event-delivery/"><img alt="PyPI version for tba-capability-security-event-delivery" src="https://img.shields.io/pypi/v/tba-capability-security-event-delivery?label=tba-capability-security-event-delivery%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-capability-security-event-delivery"><img alt="Monthly PyPI downloads for tba-capability-security-event-delivery" src="https://static.pepy.tech/badge/tba-capability-security-event-delivery/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-security-event-delivery/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Layer-40 orchestration for security-event transmission, receipt, durable
recording, subscription authorization, delivery history, and replay defense.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_capability_security_event_delivery import SecurityEventsCapability

assert callable(SecurityEventsCapability)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-capability-security-event-delivery==0.4.0.dev2" python quickstart.py
```

The import and assertion succeed when the SecurityEventsCapability entry point is available.

## Injected dependencies

Required collaborators are transmitter/receiver ports plus event recorder,
subscription resolver, delivery recorder, and replay reserver callables. All
may be synchronous or asynchronous; durable callables normally adapt layer 30.

## Operations and readiness

Operations are `record_event`, `resolve_subscription`, `record_delivery`,
`reserve_replay`, `transmit`, and `receive`. All are required. Transmission
checks the subscription and records delivery; receipt reserves replay state
before recording the event.

## Protocol consumers

The layer-50 SET package maps RFC 8417 event tokens and delivery semantics to
this capability. Shared-signals profiles may compose the same operations.

## Non-goals

This package does not encode/decode SETs, choose endpoints or transport,
resolve signing keys/trust, own tables, or expose HTTP.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-security-event-delivery/src/tba_capability_security_event_delivery/__init__.py).
