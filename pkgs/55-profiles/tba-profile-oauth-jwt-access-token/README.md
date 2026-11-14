# tba-profile-oauth-jwt-access-token

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-oauth-jwt-access-token/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-oauth-jwt-access-token/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/55-profiles"><img alt="Layer: 55 profiles" src="https://img.shields.io/badge/Layer-55%20profiles-0a7f5a"></a>
<a href="https://pypi.org/project/tba-profile-oauth-jwt-access-token/"><img alt="PyPI version for tba-profile-oauth-jwt-access-token" src="https://img.shields.io/pypi/v/tba-profile-oauth-jwt-access-token?label=tba-profile-oauth-jwt-access-token%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-profile-oauth-jwt-access-token"><img alt="Monthly PyPI downloads for tba-profile-oauth-jwt-access-token" src="https://static.pepy.tech/badge/tba-profile-oauth-jwt-access-token/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-oauth-jwt-access-token/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Check decoded JWT access-token fields against the RFC 9068 profile rules implemented here.

## Quick start

Install the version used by this example.

```bash
python -m pip install "tba-profile-oauth-jwt-access-token==0.4.0.dev2"
```

Save the following as `quickstart.py` and run `python quickstart.py`. The assertions should pass.

```python
from tba_profile_oauth_jwt_access_token import validate_access_token

issuer = "https://issuer.example"
audience = "https://api.example"
validate_access_token(
    {"typ": "at+jwt", "alg": "ES256"},
    {"iss": issuer, "sub": "alice", "aud": audience, "exp": 1000,
     "iat": 900, "jti": "token-1", "client_id": "demo"},
    expected_issuer=issuer,
    expected_audience=audience,
)
```

## When to use it

Call this helper as part of an access-token verification pipeline. Pair it with cryptographic signature and algorithm verification, trusted issuer key resolution, and expiry checks. The helper checks token type, signing-algorithm presence, required fields, issuer, and audience.

## Verification

See the [related repository tests](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-oidc/tests/unit/test_oidc_id_and_jwt_access_token_profiles.py) for the implementation scope covered by this example.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [tba-app-backend-public](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/90-backend-apps/tba-app-backend-public#readme) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)
