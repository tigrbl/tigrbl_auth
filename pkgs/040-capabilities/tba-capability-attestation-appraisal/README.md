# tba-capability-attestation-appraisal

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-attestation-appraisal/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-attestation-appraisal/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-capability-attestation-appraisal%3D%3D0.4.0.dev3/pkgs/040-capabilities/tba-capability-attestation-appraisal/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-capability-attestation-appraisal%3D%3D0.4.0.dev3/pkgs/040-capabilities/tba-capability-attestation-appraisal/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/040-capabilities"><img alt="Layer: 040 capabilities" src="https://img.shields.io/badge/Layer-040%20capabilities-0a7f5a"></a>
<a href="https://pypi.org/project/tba-capability-attestation-appraisal/"><img alt="PyPI version for tba-capability-attestation-appraisal" src="https://img.shields.io/pypi/v/tba-capability-attestation-appraisal?label=tba-capability-attestation-appraisal%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-capability-attestation-appraisal"><img alt="Monthly PyPI downloads for tba-capability-attestation-appraisal" src="https://static.pepy.tech/badge/tba-capability-attestation-appraisal/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-attestation-appraisal/README.md"><img alt="README hits for tba-capability-attestation-appraisal" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-attestation-appraisal/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-attestation-appraisal/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Layer-40 orchestration for verifying attestation evidence, resolving reference
material, appraising verified evidence, and recording appraisal results.

## AEO Summary

- Package: `tba-capability-attestation-appraisal`
- Layer: `040-capabilities`
- Responsibility: Attestation appraisal capability composition.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-attestation-appraisal/src/tba_capability_attestation_appraisal/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-capability-attestation-appraisal` for this responsibility: Attestation appraisal capability composition. Its `040-capabilities` placement keeps use-case orchestration through explicit collaborators separate from HTTP wire schemas, direct table ownership, or hidden provider selection.

## Installation

Install the selected PyPI release of `tba-capability-attestation-appraisal`:

```bash
uv pip install tba-capability-attestation-appraisal
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/040-capabilities/tba-capability-attestation-appraisal
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_capability_attestation_appraisal import AttestationAppraisalCapability

assert callable(AttestationAppraisalCapability)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-capability-attestation-appraisal==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the AttestationAppraisalCapability entry point is available.

## Usage

The following public-entry-point example belongs to `tba-capability-attestation-appraisal`. Attestation appraisal capability composition. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_capability_attestation_appraisal import AttestationAppraisalCapability

assert callable(AttestationAppraisalCapability)
```

## Package Boundary

`tba-capability-attestation-appraisal` belongs to `040-capabilities` and owns use-case orchestration through explicit collaborators: Attestation appraisal capability composition.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-attestation-appraisal/src/tba_capability_attestation_appraisal/__init__.py). Public exports include `AttestationAppraisalCapability`, `ResultRecorder`.

Keep HTTP wire schemas, direct table ownership, or hidden provider selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Required: `EvidenceVerifierPort` and `AttestationAppraiserPort`. Optional:
`ReferenceMaterialProviderPort` and a durable result-recorder callable.

## Operations and readiness

Required operations are `verify_evidence` and `appraise`. Optional operations
are `resolve_reference_material` and `record_result`; the capability report
marks either unavailable when its collaborator is absent. Raw evidence is
never passed to the appraiser before successful verification.

For `tba-capability-attestation-appraisal`, these operation names identify the callable surface, not a readiness guarantee. Validate its explicit collaborators and behavioral checks in Verification before deployment.

## Protocol consumers

Layer-50 EAT, CoRIM, and HAIP packages consume these operations when their
selected profiles require evidence appraisal or reference material.

## Non-goals

This package does not parse EAT/CoRIM wire artifacts, choose trust anchors,
store evidence/results, open sessions, or expose transports.

## Related Packages

Declared local runtime dependencies:

- [tba-concrete-capability](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-capability/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/040-capabilities/tba-capability-attestation-appraisal)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-attestation-appraisal/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-attestation-appraisal/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-attestation-appraisal/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-capability-attestation-appraisal/)

## Governance

`tba-capability-attestation-appraisal` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `040-capabilities` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-attestation-appraisal/src/tba_capability_attestation_appraisal/__init__.py).
