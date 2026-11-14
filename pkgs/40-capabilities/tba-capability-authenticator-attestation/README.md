# tba-capability-authenticator-attestation

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-authenticator-attestation/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-authenticator-attestation/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-authenticator-attestation/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities"><img alt="Layer: 40 capabilities" src="https://img.shields.io/badge/Layer-40%20capabilities-0a7f5a"></a>
<a href="https://pypi.org/project/tba-capability-authenticator-attestation/"><img alt="PyPI version for tba-capability-authenticator-attestation" src="https://img.shields.io/pypi/v/tba-capability-authenticator-attestation?label=tba-capability-authenticator-attestation%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-capability-authenticator-attestation"><img alt="Monthly PyPI downloads for tba-capability-authenticator-attestation" src="https://static.pepy.tech/badge/tba-capability-authenticator-attestation/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-authenticator-attestation/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Mountable appraisal, metadata resolution, and reappraisal operations for authenticator attestations.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_capability_authenticator_attestation import AuthenticatorAttestationCapability

assert callable(AuthenticatorAttestationCapability)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-capability-authenticator-attestation==0.4.0.dev2" python quickstart.py
```

The import and assertion succeed when the AuthenticatorAttestationCapability entry point is available.

## Injected dependencies

An attestation appraiser plus optional metadata resolver and registered-authenticator reappraiser.

## Operations and readiness

Appraisal is required. Metadata resolution and reappraisal are optional and report unavailable when unbound.

## Protocol consumers

WebAuthn registration and the FIDO2 server profile consume normalized appraisal results.

## Non-goals

This package does not parse attestation formats, fetch metadata, validate certificate paths, or choose trust policy.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-authenticator-attestation/src/tba_capability_authenticator_attestation/__init__.py).
