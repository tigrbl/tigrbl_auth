# tba-concrete-eat-evidence

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-eat-evidence/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-eat-evidence/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-eat-evidence/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/10-concrete"><img alt="Layer: 10 concrete" src="https://img.shields.io/badge/Layer-10%20concrete-0a7f5a"></a>
<a href="https://pypi.org/project/tba-concrete-eat-evidence/"><img alt="PyPI version for tba-concrete-eat-evidence" src="https://img.shields.io/pypi/v/tba-concrete-eat-evidence?label=tba-concrete-eat-evidence%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-concrete-eat-evidence"><img alt="Monthly PyPI downloads for tba-concrete-eat-evidence" src="https://static.pepy.tech/badge/tba-concrete-eat-evidence/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-eat-evidence/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Owns the deterministic EAT specialization of neutral attestation evidence.
Token-envelope verification, EAT profile versions, and appraisal are outside this package.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_concrete_eat_evidence import EatEvidence

assert callable(EatEvidence)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-concrete-eat-evidence==0.4.0.dev2" python quickstart.py
```

The import and assertion succeed when the EatEvidence entry point is available.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-eat-evidence/src/tba_concrete_eat_evidence/__init__.py).
