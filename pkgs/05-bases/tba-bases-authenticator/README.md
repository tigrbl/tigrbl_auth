# tba-bases-authenticator

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authenticator/pyproject.toml"><img alt="Checkout: 0.1.0" src="https://img.shields.io/badge/Checkout-0.1.0-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authenticator/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authenticator/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/05-bases"><img alt="Layer: 05 bases" src="https://img.shields.io/badge/Layer-05%20bases-0a7f5a"></a>
<a href="https://pypi.org/project/tba-bases-authenticator/"><img alt="PyPI version for tba-bases-authenticator" src="https://img.shields.io/pypi/v/tba-bases-authenticator?label=tba-bases-authenticator%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-bases-authenticator"><img alt="Monthly PyPI downloads for tba-bases-authenticator" src="https://static.pepy.tech/badge/tba-bases-authenticator/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authenticator/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Build authenticator providers with shared metadata, evidence, and challenge interfaces.

## Quick start

Install the version used by this example.

```bash
python -m pip install "tba-bases-authenticator==0.1.0"
```

Save the following as `quickstart.py` and run `python quickstart.py`. The assertions should pass.

```python
from tba_bases_authenticator import AuthenticatorBase

base = AuthenticatorBase(
    kind="password_local", factor_class="knowledge", amr=("pwd",)
)
assert base.supported_amr() == ("pwd",)
assert base.metadata().challenge_based is False
```

## When to use it

Extend `AuthenticatorBase` for a single ceremony or `ChallengeAuthenticatorBase` for start/finish flows. Supply the actual authentication behavior in your provider implementation. Use a layer 20 provider if you need a ready-made authenticator.

## Verification

See the [related repository tests](https://github.com/tigrbl/tigrbl_auth/blob/master/tests/unit/test_authenticator_contracts_and_providers.py) for the implementation scope covered by this example.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [tba-provider-authenticator-password-local](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/20-providers/tba-provider-authenticator-password-local#readme) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)
