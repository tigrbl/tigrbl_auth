# tba-testkit-workload-credential-conformance

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-testkit-workload-credential-conformance/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-testkit-workload-credential-conformance/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/120-tests"><img alt="Layer: 120 tests" src="https://img.shields.io/badge/Layer-120%20tests-0a7f5a"></a>
<a href="https://pypi.org/project/tba-testkit-workload-credential-conformance/"><img alt="PyPI version for tba-testkit-workload-credential-conformance" src="https://img.shields.io/pypi/v/tba-testkit-workload-credential-conformance?label=tba-testkit-workload-credential-conformance%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-testkit-workload-credential-conformance"><img alt="Monthly PyPI downloads for tba-testkit-workload-credential-conformance" src="https://static.pepy.tech/badge/tba-testkit-workload-credential-conformance/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-testkit-workload-credential-conformance/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Reusable structural and negative vectors. Passing these vectors is not an independent interoperability or certification claim.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_testkit_workload_credential_conformance import VECTORS

assert any(vector.expected_valid for vector in VECTORS)
assert any(not vector.expected_valid for vector in VECTORS)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-testkit-workload-credential-conformance==0.4.0.dev2" python quickstart.py
```

The fixture inventory contains both accepted and rejected cases.

The workload suites also import certificate and TLS fixtures from `fixtures`,
profile exercises from `profiles`, and the clean-wheel runner from `wheels`.
The `runner` extra supplies their test tooling. The root test environment
supplies the protocol packages exercised by each suite.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-testkit-workload-credential-conformance/src/tba_testkit_workload_credential_conformance/__init__.py).
