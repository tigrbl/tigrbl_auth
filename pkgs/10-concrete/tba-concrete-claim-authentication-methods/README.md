# tba-concrete-claim-authentication-methods

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-claim-authentication-methods/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-claim-authentication-methods/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/10-concrete"><img alt="Layer: 10 concrete" src="https://img.shields.io/badge/Layer-10%20concrete-0a7f5a"></a>
<a href="https://pypi.org/project/tba-concrete-claim-authentication-methods/"><img alt="PyPI version for tba-concrete-claim-authentication-methods" src="https://img.shields.io/pypi/v/tba-concrete-claim-authentication-methods?label=tba-concrete-claim-authentication-methods%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-concrete-claim-authentication-methods"><img alt="Monthly PyPI downloads for tba-concrete-claim-authentication-methods" src="https://static.pepy.tech/badge/tba-concrete-claim-authentication-methods/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-claim-authentication-methods/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Owns `AuthenticationMethodsClaim` as protocol-neutral layer-10 value semantics.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_concrete_claim_authentication_methods import AuthenticationMethodsClaim

claim = AuthenticationMethodsClaim(('pwd', 'otp'))
assert claim.name == 'amr'
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-concrete-claim-authentication-methods==0.4.0.dev2" python quickstart.py
```

The example constructs a claim named `amr`.

## Non-goals

Protocol claim-set composition, version selection, persistence, trust resolution, and environment-backed claim retrieval are not owned here.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-claim-authentication-methods/src/tba_concrete_claim_authentication_methods/__init__.py).
