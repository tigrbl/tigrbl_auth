# tba-capability-digital-credential-issuance

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-digital-credential-issuance/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-digital-credential-issuance/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-digital-credential-issuance/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities"><img alt="Layer: 40 capabilities" src="https://img.shields.io/badge/Layer-40%20capabilities-0a7f5a"></a>
<a href="https://pypi.org/project/tba-capability-digital-credential-issuance/"><img alt="PyPI version for tba-capability-digital-credential-issuance" src="https://img.shields.io/pypi/v/tba-capability-digital-credential-issuance?label=tba-capability-digital-credential-issuance%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-capability-digital-credential-issuance"><img alt="Monthly PyPI downloads for tba-capability-digital-credential-issuance" src="https://static.pepy.tech/badge/tba-capability-digital-credential-issuance/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-digital-credential-issuance/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Layer-40 orchestration for credential configuration, offers, wallet trust, and
credential issuance.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_capability_digital_credential_issuance import DigitalCredentialIssuanceCapability

assert callable(DigitalCredentialIssuanceCapability)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-capability-digital-credential-issuance==0.4.0.dev2" python quickstart.py
```

The import and assertion succeed when the DigitalCredentialIssuanceCapability entry point is available.

## Injected dependencies

Required collaborators are a `CredentialIssuerPort`, configuration read/write
operations, an offer recorder, and an issuance-result recorder. A
`WalletAttestationVerifierPort` is optional. All operations are async-safe and
durable state remains behind the injected callables.

## Operations and readiness

Required operations are `register_configuration`, `create_offer`, `issue`, and
`record_issuance`. `verify_wallet_attestation` is optional and is reported as
unavailable when unbound. Construction rejects a missing required operation.

## Protocol consumers

Layer-50 OID4VCI maps issuance messages to this capability. HAIP selects and
constrains the OID4VCI composition when its profile is enabled.

## Non-goals

This package does not own credential formats, protocol schemas, HTTP, wallet
attestation policy, signing keys, trust resolution, or persistence.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-digital-credential-issuance/src/tba_capability_digital_credential_issuance/__init__.py).
