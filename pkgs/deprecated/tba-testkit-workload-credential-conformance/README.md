# tba-testkit-workload-credential-conformance (deprecated)

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/deprecated/tba-testkit-workload-credential-conformance/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/deprecated/tba-testkit-workload-credential-conformance/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-testkit-workload-credential-conformance%3D%3D0.4.0.dev4/pkgs/deprecated/tba-testkit-workload-credential-conformance/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-testkit-workload-credential-conformance%3D%3D0.4.0.dev4/pkgs/deprecated/tba-testkit-workload-credential-conformance/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/deprecated"><img alt="Layer: deprecated" src="https://img.shields.io/badge/Layer-deprecated-0a7f5a"></a>
<a href="https://pypi.org/project/tba-testkit-workload-credential-conformance/"><img alt="PyPI version for tba-testkit-workload-credential-conformance" src="https://img.shields.io/pypi/v/tba-testkit-workload-credential-conformance?label=tba-testkit-workload-credential-conformance%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-testkit-workload-credential-conformance"><img alt="Monthly PyPI downloads for tba-testkit-workload-credential-conformance" src="https://static.pepy.tech/badge/tba-testkit-workload-credential-conformance/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/deprecated/tba-testkit-workload-credential-conformance/README.md"><img alt="README hits for tba-testkit-workload-credential-conformance" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/deprecated/tba-testkit-workload-credential-conformance/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/deprecated/tba-testkit-workload-credential-conformance/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Install [`tba-tests-workload-credential-conformance`](https://pypi.org/project/tba-tests-workload-credential-conformance/) and replace `tba_testkit_workload_credential_conformance` imports with `tba_tests_workload_credential_conformance`. Use `tba-tests-workload-credential-conformance[runner]` if you installed the old `runner` extra.

Existing installations can upgrade to this release using the original package name. Imports continue to work and emit `DeprecationWarning`. Use `python -W default` to display it.

## Quick start

```bash
uv pip install "tba-testkit-workload-credential-conformance==0.4.0.dev4"
```

## Verification

Package metadata, legal files, and README fragments are checked with
`uv run python scripts/verify_package_standards.py`. Compatibility imports
and deprecation warnings retain the already-published migration behavior.
