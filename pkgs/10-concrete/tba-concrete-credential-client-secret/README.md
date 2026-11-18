# tba-concrete-credential-client-secret

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-credential-client-secret/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-credential-client-secret/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-credential-client-secret%3D%3D0.4.0.dev3/pkgs/10-concrete/tba-concrete-credential-client-secret/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-credential-client-secret%3D%3D0.4.0.dev3/pkgs/10-concrete/tba-concrete-credential-client-secret/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/10-concrete"><img alt="Layer: 10 concrete" src="https://img.shields.io/badge/Layer-10%20concrete-0a7f5a"></a>
<a href="https://pypi.org/project/tba-concrete-credential-client-secret/"><img alt="PyPI version for tba-concrete-credential-client-secret" src="https://img.shields.io/pypi/v/tba-concrete-credential-client-secret?label=tba-concrete-credential-client-secret%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-concrete-credential-client-secret"><img alt="Monthly PyPI downloads for tba-concrete-credential-client-secret" src="https://static.pepy.tech/badge/tba-concrete-credential-client-secret/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-credential-client-secret/README.md"><img alt="README hits for tba-concrete-credential-client-secret" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-credential-client-secret/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-credential-client-secret/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Owns deterministic concrete value semantics.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_concrete_credential_client_secret import ClientSecretCredential

assert callable(ClientSecretCredential)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-concrete-credential-client-secret==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the ClientSecretCredential entry point is available.

## Non-goals

Higher-layer orchestration, lower-layer persistence, and protocol behavior outside this package's declared layer are not owned here.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-credential-client-secret/src/tba_concrete_credential_client_secret/__init__.py).
