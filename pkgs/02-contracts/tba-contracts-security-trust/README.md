# tba-contracts-security-trust

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-security-trust/pyproject.toml"><img alt="Checkout: 0.1.0" src="https://img.shields.io/badge/Checkout-0.1.0-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-security-trust/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-security-trust/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/02-contracts"><img alt="Layer: 02 contracts" src="https://img.shields.io/badge/Layer-02%20contracts-0a7f5a"></a>
<a href="https://pypi.org/project/tba-contracts-security-trust/"><img alt="PyPI version for tba-contracts-security-trust" src="https://img.shields.io/pypi/v/tba-contracts-security-trust?label=tba-contracts-security-trust%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-contracts-security-trust"><img alt="Monthly PyPI downloads for tba-contracts-security-trust" src="https://static.pepy.tech/badge/tba-contracts-security-trust/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-security-trust/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Draft standalone contract package for security/trust component analysis.

This package intentionally contains only small protocol contracts and dataclass DTOs. It does not implement signing, token issuance, certificate handling, cryptographic transforms, key storage, or cipher-suite policy.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_contracts_security_trust import AcrEvaluationRequest

assert callable(AcrEvaluationRequest)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-contracts-security-trust==0.1.0" python quickstart.py
```

The import and assertion succeed when the AcrEvaluationRequest entry point is available.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-security-trust/src/tba_contracts_security_trust/__init__.py).
