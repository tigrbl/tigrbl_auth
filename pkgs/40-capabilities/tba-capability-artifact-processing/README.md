# tba-capability-artifact-processing

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-artifact-processing/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-artifact-processing/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-artifact-processing/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities"><img alt="Layer: 40 capabilities" src="https://img.shields.io/badge/Layer-40%20capabilities-0a7f5a"></a>
<a href="https://pypi.org/project/tba-capability-artifact-processing/"><img alt="PyPI version for tba-capability-artifact-processing" src="https://img.shields.io/pypi/v/tba-capability-artifact-processing?label=tba-capability-artifact-processing%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-capability-artifact-processing"><img alt="Monthly PyPI downloads for tba-capability-artifact-processing" src="https://static.pepy.tech/badge/tba-capability-artifact-processing/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-artifact-processing/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Layer-40 protocol-neutral orchestration for encoded artifact processing through
an injected processor.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_capability_artifact_processing import ProtocolArtifactProcessingCapability

assert callable(ProtocolArtifactProcessingCapability)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-capability-artifact-processing==0.4.0.dev2" python quickstart.py
```

The import and assertion succeed when the ProtocolArtifactProcessingCapability entry point is available.

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

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-artifact-processing/src/tba_capability_artifact_processing/__init__.py).
