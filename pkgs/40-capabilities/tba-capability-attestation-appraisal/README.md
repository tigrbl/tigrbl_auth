# tba-capability-attestation-appraisal

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-attestation-appraisal/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-attestation-appraisal/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-attestation-appraisal/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities"><img alt="Layer: 40 capabilities" src="https://img.shields.io/badge/Layer-40%20capabilities-0a7f5a"></a>
<a href="https://pypi.org/project/tba-capability-attestation-appraisal/"><img alt="PyPI version for tba-capability-attestation-appraisal" src="https://img.shields.io/pypi/v/tba-capability-attestation-appraisal?label=tba-capability-attestation-appraisal%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-capability-attestation-appraisal"><img alt="Monthly PyPI downloads for tba-capability-attestation-appraisal" src="https://static.pepy.tech/badge/tba-capability-attestation-appraisal/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-attestation-appraisal/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Layer-40 orchestration for verifying attestation evidence, resolving reference
material, appraising verified evidence, and recording appraisal results.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_capability_attestation_appraisal import AttestationAppraisalCapability

assert callable(AttestationAppraisalCapability)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-capability-attestation-appraisal==0.4.0.dev2" python quickstart.py
```

The import and assertion succeed when the AttestationAppraisalCapability entry point is available.

## Injected dependencies

Required: `EvidenceVerifierPort` and `AttestationAppraiserPort`. Optional:
`ReferenceMaterialProviderPort` and a durable result-recorder callable.

## Operations and readiness

Required operations are `verify_evidence` and `appraise`. Optional operations
are `resolve_reference_material` and `record_result`; the capability report
marks either unavailable when its collaborator is absent. Raw evidence is
never passed to the appraiser before successful verification.

## Protocol consumers

Layer-50 EAT, CoRIM, and HAIP packages consume these operations when their
selected profiles require evidence appraisal or reference material.

## Non-goals

This package does not parse EAT/CoRIM wire artifacts, choose trust anchors,
store evidence/results, open sessions, or expose transports.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-attestation-appraisal/src/tba_capability_attestation_appraisal/__init__.py).
