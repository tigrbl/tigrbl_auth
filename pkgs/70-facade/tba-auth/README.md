# tba-auth

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tba-auth/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tba-auth/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tba-auth/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/70-facade"><img alt="Layer: 70 facade" src="https://img.shields.io/badge/Layer-70%20facade-0a7f5a"></a>
<a href="https://pypi.org/project/tba-auth/"><img alt="PyPI version for tba-auth" src="https://img.shields.io/pypi/v/tba-auth?label=tba-auth%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-auth"><img alt="Monthly PyPI downloads for tba-auth" src="https://static.pepy.tech/badge/tba-auth/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tba-auth/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Keep existing applications working with the compatibility facade for the split TBA identity suite.

## Quick start

Install the version used by this example.

```bash
python -m pip install "tba-auth==0.4.0.dev2"
```

Save the following as `quickstart.py` and run `python quickstart.py`. The assertions should pass.

```python
from tba_auth.app import build_application_runtime_plan

plan = build_application_runtime_plan(runner="uvicorn", host="127.0.0.1", port=8000)
assert plan.runner == "uvicorn"
assert plan.port == 8000
```

## When to use it

Use this distribution when maintaining code with `tba_auth` imports. New integrations can use the focused public backend, server, or Tigrbl plugin packages directly. The example plans a local runner without starting it.

## Verification

See the [related repository tests](https://github.com/tigrbl/tigrbl_auth/blob/master/tests/unit/test_facade_compatibility_boundary.py) for the implementation scope covered by this example.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [tba-app-backend-public](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/90-backend-apps/tba-app-backend-public#readme) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)
