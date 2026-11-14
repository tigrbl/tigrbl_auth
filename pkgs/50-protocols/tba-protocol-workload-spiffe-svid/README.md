# tba-protocol-workload-spiffe-svid

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-workload-spiffe-svid/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-workload-spiffe-svid/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/50-protocols"><img alt="Layer: 50 protocols" src="https://img.shields.io/badge/Layer-50%20protocols-0a7f5a"></a>
<a href="https://pypi.org/project/tba-protocol-workload-spiffe-svid/"><img alt="PyPI version for tba-protocol-workload-spiffe-svid" src="https://img.shields.io/pypi/v/tba-protocol-workload-spiffe-svid?label=tba-protocol-workload-spiffe-svid%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-protocol-workload-spiffe-svid"><img alt="Monthly PyPI downloads for tba-protocol-workload-spiffe-svid" src="https://static.pepy.tech/badge/tba-protocol-workload-spiffe-svid/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-workload-spiffe-svid/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Stable SPIFFE ID, X.509-SVID, and JWT-SVID profile ownership. WIT-SVID and the experimental CWT-SVID extension are separate packages.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_protocol_workload_spiffe_svid import CURRENT_VERSION

assert CURRENT_VERSION is not None
print(CURRENT_VERSION)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-protocol-workload-spiffe-svid==0.4.0.dev2" python quickstart.py
```

The command prints the declared current revision.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-workload-spiffe-svid/src/tba_protocol_workload_spiffe_svid/__init__.py).
