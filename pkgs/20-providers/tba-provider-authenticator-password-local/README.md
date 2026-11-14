# tba-provider-authenticator-password-local

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-password-local/pyproject.toml"><img alt="Checkout: 0.1.0" src="https://img.shields.io/badge/Checkout-0.1.0-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-password-local/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-password-local/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/20-providers"><img alt="Layer: 20 providers" src="https://img.shields.io/badge/Layer-20%20providers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-provider-authenticator-password-local/"><img alt="PyPI version for tba-provider-authenticator-password-local" src="https://img.shields.io/pypi/v/tba-provider-authenticator-password-local?label=tba-provider-authenticator-password-local%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-provider-authenticator-password-local"><img alt="Monthly PyPI downloads for tba-provider-authenticator-password-local" src="https://static.pepy.tech/badge/tba-provider-authenticator-password-local/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-password-local/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Verify a presented password against an existing stored hash using the local authenticator.

## Quick start

Install the version used by this example.

```bash
python -m pip install "tba-provider-authenticator-password-local==0.1.0"
```

Save the following as `quickstart.py` and run `python quickstart.py`. The assertions should pass.

```python
from tba_provider_authenticator_password_local import PasswordLocalAuthenticator
from tba_provider_secret_hashing_bcrypt import BcryptSecretHasher

verifier = BcryptSecretHasher()
stored = verifier.hash_secret("example-password")
authenticator = PasswordLocalAuthenticator(secret_verifier=verifier)
assert authenticator.verify_secret("example-password", stored)
assert not authenticator.verify_secret("incorrect-password", stored)
```

## When to use it

`PasswordLocalAuthenticator` uses bcrypt by default and accepts an injected `SecretVerificationPort`. The caller supplies the stored hash and owns account lookup, rate limits, and session creation. The example uses a demonstration password.

## Verification

See the [related repository tests](https://github.com/tigrbl/tigrbl_auth/blob/master/tests/unit/test_authenticator_contracts_and_providers.py) for the implementation scope covered by this example.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [tba-bases-authenticator](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/05-bases/tba-bases-authenticator#readme) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)
