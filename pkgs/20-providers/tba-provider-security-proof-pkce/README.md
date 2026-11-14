# tba-provider-security-proof-pkce

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-proof-pkce/pyproject.toml"><img alt="Checkout: 0.1.0" src="https://img.shields.io/badge/Checkout-0.1.0-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-proof-pkce/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-proof-pkce/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/20-providers"><img alt="Layer: 20 providers" src="https://img.shields.io/badge/Layer-20%20providers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-provider-security-proof-pkce/"><img alt="PyPI version for tba-provider-security-proof-pkce" src="https://img.shields.io/pypi/v/tba-provider-security-proof-pkce?label=tba-provider-security-proof-pkce%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-provider-security-proof-pkce"><img alt="Monthly PyPI downloads for tba-provider-security-proof-pkce" src="https://static.pepy.tech/badge/tba-provider-security-proof-pkce/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-proof-pkce/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Standalone RFC 7636 PKCE proof helper and verifier provider for the TBA package suite.

- Owns dependency-light verifier generation, S256 challenge derivation, and challenge verification.
- Exposes `PkceProofProvider` for the security trust domain provider surface.
- Protocol packages such as `tba-protocol-oidc-relying-party` and `tba-protocol-oauth` should import this package instead of duplicating PKCE primitives.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_provider_security_proof_pkce import PkceProofProvider

assert callable(PkceProofProvider)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-provider-security-proof-pkce==0.1.0" python quickstart.py
```

The import and assertion succeed when the PkceProofProvider entry point is available.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-proof-pkce/src/tba_provider_security_proof_pkce/__init__.py).
