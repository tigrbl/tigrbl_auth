# tba-certification-release

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-certification-release/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-certification-release/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-certification-release/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/60-runtime"><img alt="Layer: 60 runtime" src="https://img.shields.io/badge/Layer-60%20runtime-0a7f5a"></a>
<a href="https://pypi.org/project/tba-certification-release/"><img alt="PyPI version for tba-certification-release" src="https://img.shields.io/pypi/v/tba-certification-release?label=tba-certification-release%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-certification-release"><img alt="Monthly PyPI downloads for tba-certification-release" src="https://static.pepy.tech/badge/tba-certification-release/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-certification-release/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Executable release certification and release posture helpers for the TBA package suite.

This package owns runtime validation, release posture summaries, disclosure rules, provenance requirements, isolation checks, and certification assertions. It consumes contract DTOs from `tba-contracts-release`; it does not define those DTOs.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_certification_release import AlgorithmPolicy

assert callable(AlgorithmPolicy)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-certification-release==0.4.0.dev2" python quickstart.py
```

The import and assertion succeed when the AlgorithmPolicy entry point is available.

## Boundary

- Owns executable release and certification checks.
- Owns runtime capability truth manifests and capability attestations derived
  from resolved deployment state.
- May depend on runtime/concrete packages needed to evaluate release truth.
- Must not own authorization policy decisioning, admin control-plane workflows, storage tables, or protocol runtime behavior.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-certification-release/src/tba_certification_release/__init__.py).
