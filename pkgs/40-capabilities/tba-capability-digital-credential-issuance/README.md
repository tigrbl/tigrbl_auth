# tba-capability-digital-credential-issuance

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-digital-credential-issuance/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-digital-credential-issuance/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-capability-digital-credential-issuance%3D%3D0.4.0.dev3/pkgs/40-capabilities/tba-capability-digital-credential-issuance/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-capability-digital-credential-issuance%3D%3D0.4.0.dev3/pkgs/40-capabilities/tba-capability-digital-credential-issuance/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities"><img alt="Layer: 40 capabilities" src="https://img.shields.io/badge/Layer-40%20capabilities-0a7f5a"></a>
<a href="https://pypi.org/project/tba-capability-digital-credential-issuance/"><img alt="PyPI version for tba-capability-digital-credential-issuance" src="https://img.shields.io/pypi/v/tba-capability-digital-credential-issuance?label=tba-capability-digital-credential-issuance%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-capability-digital-credential-issuance"><img alt="Monthly PyPI downloads for tba-capability-digital-credential-issuance" src="https://static.pepy.tech/badge/tba-capability-digital-credential-issuance/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-digital-credential-issuance/README.md"><img alt="README hits for tba-capability-digital-credential-issuance" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-digital-credential-issuance/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-digital-credential-issuance/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Layer-40 orchestration for credential configuration, offers, wallet trust, and
credential issuance.

## AEO Summary

- Package: `tba-capability-digital-credential-issuance`
- Layer: `40-capabilities`
- Responsibility: Digital credential issuance capability composition.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-digital-credential-issuance/src/tba_capability_digital_credential_issuance/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-capability-digital-credential-issuance` for this responsibility: Digital credential issuance capability composition. Its `40-capabilities` placement keeps use-case orchestration through explicit collaborators separate from HTTP wire schemas, direct table ownership, or hidden provider selection.

## Installation

Install the selected PyPI release of `tba-capability-digital-credential-issuance`:

```bash
uv pip install tba-capability-digital-credential-issuance
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/40-capabilities/tba-capability-digital-credential-issuance
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_capability_digital_credential_issuance import DigitalCredentialIssuanceCapability

assert callable(DigitalCredentialIssuanceCapability)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-capability-digital-credential-issuance==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the DigitalCredentialIssuanceCapability entry point is available.

## Usage

The following public-entry-point example belongs to `tba-capability-digital-credential-issuance`. Digital credential issuance capability composition. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_capability_digital_credential_issuance import DigitalCredentialIssuanceCapability

assert callable(DigitalCredentialIssuanceCapability)
```

## Package Boundary

`tba-capability-digital-credential-issuance` belongs to `40-capabilities` and owns use-case orchestration through explicit collaborators: Digital credential issuance capability composition.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-digital-credential-issuance/src/tba_capability_digital_credential_issuance/__init__.py). Public exports include `ConfigurationReader`, `ConfigurationWriter`, `DigitalCredentialIssuanceCapability`, `IssuanceRecorder`, `IssuanceHandler`, `LocalDigitalCredentialIssuer`, `OfferRecorder`.

Keep HTTP wire schemas, direct table ownership, or hidden provider selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Required collaborators are a `CredentialIssuerPort`, configuration read/write
operations, an offer recorder, and an issuance-result recorder. A
`WalletAttestationVerifierPort` is optional. All operations are async-safe and
durable state remains behind the injected callables.

## Operations and readiness

Required operations are `register_configuration`, `create_offer`, `issue`, and
`record_issuance`. `verify_wallet_attestation` is optional and is reported as
unavailable when unbound. Construction rejects a missing required operation.

For `tba-capability-digital-credential-issuance`, these operation names identify the callable surface, not a readiness guarantee. Validate its explicit collaborators and behavioral checks in Verification before deployment.

## Protocol consumers

Layer-50 OID4VCI maps issuance messages to this capability. HAIP selects and
constrains the OID4VCI composition when its profile is enabled.

## Non-goals

This package does not own credential formats, protocol schemas, HTTP, wallet
attestation policy, signing keys, trust resolution, or persistence.

## Related Packages

Declared local runtime dependencies:

- [tba-concrete-capability](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-capability/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/README.md)

Direct downstream consumers:

- [tba-protocol-oid4vci](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oid4vci/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities/tba-capability-digital-credential-issuance)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-digital-credential-issuance/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-digital-credential-issuance/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-digital-credential-issuance/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-capability-digital-credential-issuance/)

## Governance

`tba-capability-digital-credential-issuance` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `40-capabilities` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-digital-credential-issuance/src/tba_capability_digital_credential_issuance/__init__.py).
