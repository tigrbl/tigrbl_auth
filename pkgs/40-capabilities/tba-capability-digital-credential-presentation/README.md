# tba-capability-digital-credential-presentation

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-digital-credential-presentation/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-digital-credential-presentation/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-digital-credential-presentation/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities"><img alt="Layer: 40 capabilities" src="https://img.shields.io/badge/Layer-40%20capabilities-0a7f5a"></a>
<a href="https://pypi.org/project/tba-capability-digital-credential-presentation/"><img alt="PyPI version for tba-capability-digital-credential-presentation" src="https://img.shields.io/pypi/v/tba-capability-digital-credential-presentation?label=tba-capability-digital-credential-presentation%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-capability-digital-credential-presentation"><img alt="Monthly PyPI downloads for tba-capability-digital-credential-presentation" src="https://static.pepy.tech/badge/tba-capability-digital-credential-presentation/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-digital-credential-presentation/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Layer-40 orchestration for holder consent, replay reservation, presentation
verification, and durable transaction/result recording.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_capability_digital_credential_presentation import DigitalCredentialPresentationCapability

assert callable(DigitalCredentialPresentationCapability)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-capability-digital-credential-presentation==0.4.0.dev2" python quickstart.py
```

The import and assertion succeed when the DigitalCredentialPresentationCapability entry point is available.

## Injected dependencies

Required collaborators are a `PresentationVerifierPort`, consent checker,
replay reserver, transaction recorder, and result recorder. Each collaborator
may be synchronous or asynchronous.

## Operations and readiness

Operations are `check_consent`, `reserve_replay`, `verify_presentation`,
`record_transaction`, `record_result`, and the composed `present` operation.
All are required; construction fails if any target is missing. `present`
records every attempt and outcome, including consent and replay rejection.

## Protocol consumers

Layer-50 OID4VP maps presentation requests/responses to this capability. HAIP
configures its permitted credential formats, bindings, and trust rules.

## Non-goals

This package does not parse OID4VP/VP wire formats, select disclosure, retain
claims, choose trust anchors, open sessions, or expose routes.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-digital-credential-presentation/src/tba_capability_digital_credential_presentation/__init__.py).
