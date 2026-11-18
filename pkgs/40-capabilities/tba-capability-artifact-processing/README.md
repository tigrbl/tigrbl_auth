# tba-capability-artifact-processing

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-artifact-processing/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-artifact-processing/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-capability-artifact-processing%3D%3D0.4.0.dev3/pkgs/40-capabilities/tba-capability-artifact-processing/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-capability-artifact-processing%3D%3D0.4.0.dev3/pkgs/40-capabilities/tba-capability-artifact-processing/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities"><img alt="Layer: 40 capabilities" src="https://img.shields.io/badge/Layer-40%20capabilities-0a7f5a"></a>
<a href="https://pypi.org/project/tba-capability-artifact-processing/"><img alt="PyPI version for tba-capability-artifact-processing" src="https://img.shields.io/pypi/v/tba-capability-artifact-processing?label=tba-capability-artifact-processing%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-capability-artifact-processing"><img alt="Monthly PyPI downloads for tba-capability-artifact-processing" src="https://static.pepy.tech/badge/tba-capability-artifact-processing/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-artifact-processing/README.md"><img alt="README hits for tba-capability-artifact-processing" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-artifact-processing/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-artifact-processing/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Layer-40 protocol-neutral orchestration for encoded artifact processing through
an injected processor.

## AEO Summary

- Package: `tba-capability-artifact-processing`
- Layer: `40-capabilities`
- Responsibility: Protocol-neutral artifact decode, validate, encode, and error-mapping capability.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-artifact-processing/src/tba_capability_artifact_processing/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-capability-artifact-processing` for this responsibility: Protocol-neutral artifact decode, validate, encode, and error-mapping capability. Its `40-capabilities` placement keeps use-case orchestration through explicit collaborators separate from HTTP wire schemas, direct table ownership, or hidden provider selection.

## Installation

Install the selected PyPI release of `tba-capability-artifact-processing`:

```bash
uv pip install tba-capability-artifact-processing
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/40-capabilities/tba-capability-artifact-processing
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_capability_artifact_processing import ProtocolArtifactProcessingCapability

assert callable(ProtocolArtifactProcessingCapability)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-capability-artifact-processing==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the ProtocolArtifactProcessingCapability entry point is available.

## Usage

The following public-entry-point example belongs to `tba-capability-artifact-processing`. Protocol-neutral artifact decode, validate, encode, and error-mapping capability. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_capability_artifact_processing import ProtocolArtifactProcessingCapability

assert callable(ProtocolArtifactProcessingCapability)
```

## Package Boundary

`tba-capability-artifact-processing` belongs to `40-capabilities` and owns use-case orchestration through explicit collaborators: Protocol-neutral artifact decode, validate, encode, and error-mapping capability.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-artifact-processing/src/tba_capability_artifact_processing/__init__.py). Public exports include `ArtifactProcessingRequest`, `ArtifactProcessingResult`, `ProtocolArtifactProcessingCapability`.

Keep HTTP wire schemas, direct table ownership, or hidden provider selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

A required `ArtifactProcessorPort` supplies deterministic decode, validate,
encode, and error-mapping behavior. Provider health/status attributes are read
only for effective reporting.

## Operations and readiness

Operations are `decode`, `validate`, `encode`, and `map_error`. Readiness is
derived from the complete bound required-operation set; health and status are
derived from the processor instead of being hard-coded.

## Protocol consumers

Any layer-50 protocol package may map a concrete artifact profile to these
operations. Its requirement rows must name the actual operation rather than a
generic catch-all validation claim.

## Non-goals

This package does not own wire schemas, revisions, keys, trust anchors,
persistence, HTTP, or deployment settings.

## Related Packages

Declared local runtime dependencies:

- [tba-concrete-capability](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-capability/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/README.md)

Direct downstream consumers:

- [tba-server-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-server-identity/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities/tba-capability-artifact-processing)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-artifact-processing/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-artifact-processing/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-artifact-processing/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-capability-artifact-processing/)

## Governance

`tba-capability-artifact-processing` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `40-capabilities` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-artifact-processing/src/tba_capability_artifact_processing/__init__.py).
