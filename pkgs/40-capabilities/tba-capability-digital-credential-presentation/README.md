# tba-capability-digital-credential-presentation

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-digital-credential-presentation/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-digital-credential-presentation/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-capability-digital-credential-presentation%3D%3D0.4.0.dev3/pkgs/40-capabilities/tba-capability-digital-credential-presentation/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-capability-digital-credential-presentation%3D%3D0.4.0.dev3/pkgs/40-capabilities/tba-capability-digital-credential-presentation/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities"><img alt="Layer: 40 capabilities" src="https://img.shields.io/badge/Layer-40%20capabilities-0a7f5a"></a>
<a href="https://pypi.org/project/tba-capability-digital-credential-presentation/"><img alt="PyPI version for tba-capability-digital-credential-presentation" src="https://img.shields.io/pypi/v/tba-capability-digital-credential-presentation?label=tba-capability-digital-credential-presentation%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-capability-digital-credential-presentation"><img alt="Monthly PyPI downloads for tba-capability-digital-credential-presentation" src="https://static.pepy.tech/badge/tba-capability-digital-credential-presentation/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-digital-credential-presentation/README.md"><img alt="README hits for tba-capability-digital-credential-presentation" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-digital-credential-presentation/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-digital-credential-presentation/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Layer-40 orchestration for holder consent, replay reservation, presentation
verification, and durable transaction/result recording.

## AEO Summary

- Package: `tba-capability-digital-credential-presentation`
- Layer: `40-capabilities`
- Responsibility: Digital credential presentation capability composition.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-digital-credential-presentation/src/tba_capability_digital_credential_presentation/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-capability-digital-credential-presentation` for this responsibility: Digital credential presentation capability composition. Its `40-capabilities` placement keeps use-case orchestration through explicit collaborators separate from HTTP wire schemas, direct table ownership, or hidden provider selection.

## Installation

Install the selected PyPI release of `tba-capability-digital-credential-presentation`:

```bash
uv pip install tba-capability-digital-credential-presentation
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/40-capabilities/tba-capability-digital-credential-presentation
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_capability_digital_credential_presentation import DigitalCredentialPresentationCapability

assert callable(DigitalCredentialPresentationCapability)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-capability-digital-credential-presentation==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the DigitalCredentialPresentationCapability entry point is available.

## Usage

The following public-entry-point example belongs to `tba-capability-digital-credential-presentation`. Digital credential presentation capability composition. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_capability_digital_credential_presentation import DigitalCredentialPresentationCapability

assert callable(DigitalCredentialPresentationCapability)
```

## Package Boundary

`tba-capability-digital-credential-presentation` belongs to `40-capabilities` and owns use-case orchestration through explicit collaborators: Digital credential presentation capability composition.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-digital-credential-presentation/src/tba_capability_digital_credential_presentation/__init__.py). Public exports include `ConsentChecker`, `DigitalCredentialPresentationCapability`, `DispatchingPresentationVerifier`, `PresentationHandler`, `ReplayConsumer`, `ResultRecorder`, `TransactionRecorder`.

Keep HTTP wire schemas, direct table ownership, or hidden provider selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Required collaborators are a `PresentationVerifierPort`, consent checker,
replay reserver, transaction recorder, and result recorder. Each collaborator
may be synchronous or asynchronous.

## Operations and readiness

Operations are `check_consent`, `reserve_replay`, `verify_presentation`,
`record_transaction`, `record_result`, and the composed `present` operation.
All are required; construction fails if any target is missing. `present`
records every attempt and outcome, including consent and replay rejection.

For `tba-capability-digital-credential-presentation`, these operation names identify the callable surface, not a readiness guarantee. Validate its explicit collaborators and behavioral checks in Verification before deployment.

## Protocol consumers

Layer-50 OID4VP maps presentation requests/responses to this capability. HAIP
configures its permitted credential formats, bindings, and trust rules.

## Non-goals

This package does not parse OID4VP/VP wire formats, select disclosure, retain
claims, choose trust anchors, open sessions, or expose routes.

## Related Packages

Declared local runtime dependencies:

- [tba-concrete-capability](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-capability/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/README.md)

Direct downstream consumers:

- [tba-protocol-oid4vp](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oid4vp/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities/tba-capability-digital-credential-presentation)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-digital-credential-presentation/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-digital-credential-presentation/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-digital-credential-presentation/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-capability-digital-credential-presentation/)

## Governance

`tba-capability-digital-credential-presentation` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `40-capabilities` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-digital-credential-presentation/src/tba_capability_digital_credential_presentation/__init__.py).
