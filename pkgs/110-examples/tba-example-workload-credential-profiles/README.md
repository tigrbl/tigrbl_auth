# tba-example-workload-credential-profiles

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-workload-credential-profiles/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-workload-credential-profiles/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/110-examples"><img alt="Layer: 110 examples" src="https://img.shields.io/badge/Layer-110%20examples-0a7f5a"></a>
<a href="https://pypi.org/project/tba-example-workload-credential-profiles/"><img alt="PyPI version for tba-example-workload-credential-profiles" src="https://img.shields.io/pypi/v/tba-example-workload-credential-profiles?label=tba-example-workload-credential-profiles%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-example-workload-credential-profiles"><img alt="Monthly PyPI downloads for tba-example-workload-credential-profiles" src="https://static.pepy.tech/badge/tba-example-workload-credential-profiles/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-workload-credential-profiles/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Runs structural WIT, WPT, and WIT-SVID validation. Production callers must additionally inject signature, key, trust, time, and replay verification.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from workload_credential_profiles_example import run_example

assert run_example() == ("wit", "wit-svid", "wpt")
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-example-workload-credential-profiles==0.4.0.dev2" python quickstart.py
```

The example validates the structural WIT, WIT-SVID, and WPT fixtures.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-workload-credential-profiles/src/workload_credential_profiles_example/__init__.py).
