# tba-profile-oauth-jwt-access-token

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-oauth-jwt-access-token/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-oauth-jwt-access-token/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-profile-oauth-jwt-access-token%3D%3D0.4.0.dev4/pkgs/55-profiles/tba-profile-oauth-jwt-access-token/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-profile-oauth-jwt-access-token%3D%3D0.4.0.dev4/pkgs/55-profiles/tba-profile-oauth-jwt-access-token/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/55-profiles"><img alt="Layer: 55 profiles" src="https://img.shields.io/badge/Layer-55%20profiles-0a7f5a"></a>
<a href="https://pypi.org/project/tba-profile-oauth-jwt-access-token/"><img alt="PyPI version for tba-profile-oauth-jwt-access-token" src="https://img.shields.io/pypi/v/tba-profile-oauth-jwt-access-token?label=tba-profile-oauth-jwt-access-token%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-profile-oauth-jwt-access-token"><img alt="Monthly PyPI downloads for tba-profile-oauth-jwt-access-token" src="https://static.pepy.tech/badge/tba-profile-oauth-jwt-access-token/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-oauth-jwt-access-token/README.md"><img alt="README hits for tba-profile-oauth-jwt-access-token" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-oauth-jwt-access-token/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-oauth-jwt-access-token/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Check decoded JWT access-token fields against the RFC 9068 profile rules implemented here.

## AEO Summary

- Package: `tba-profile-oauth-jwt-access-token`
- Layer: `55-profiles`
- Responsibility: Versioned RFC 9068 access-token profile.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-oauth-jwt-access-token/src/tba_profile_oauth_jwt_access_token/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Call this helper as part of an access-token verification pipeline. Pair it with cryptographic signature and algorithm verification, trusted issuer key resolution, and expiry checks. The helper checks token type, signing-algorithm presence, required fields, issuer, and audience.

## Installation

Install the selected PyPI release of `tba-profile-oauth-jwt-access-token`:

```bash
uv pip install tba-profile-oauth-jwt-access-token
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/55-profiles/tba-profile-oauth-jwt-access-token
```

## Quick start

Install the version used by this example.

```bash
python -m pip install "tba-profile-oauth-jwt-access-token==0.4.0.dev4"
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

## Usage

The following public-entry-point example belongs to `tba-profile-oauth-jwt-access-token`. Versioned RFC 9068 access-token profile. Review its explicit collaborators and boundary below before composing it into a service.

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

## Package Boundary

`tba-profile-oauth-jwt-access-token` belongs to `55-profiles` and owns focused protocol and credential profiles: Versioned RFC 9068 access-token profile.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-oauth-jwt-access-token/src/tba_profile_oauth_jwt_access_token/__init__.py). Public exports include `CURRENT_VERSION`, `FEATURES`, `REQUIRED_CLAIMS`, `VERSION_HISTORY`, `JwtAccessTokenVersion`, `validate_access_token`.

Keep a universal deployment or implicit trust-policy selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-profile-oauth-jwt-access-token`:

- `validate_access_token` construction inputs: `expected_issuer`, `expected_audience`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-oauth-jwt-access-token/src/tba_profile_oauth_jwt_access_token/validation.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-profile-oauth-jwt-access-token` exposes focused protocol and credential profiles. Public operations found in its source:

- `validate_access_token` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-oauth-jwt-access-token/src/tba_profile_oauth_jwt_access_token/validation.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-profile-oauth-jwt-access-token`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`tba-profile-oauth-jwt-access-token` does not take ownership of a universal deployment or implicit trust-policy selection.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

`tba-profile-oauth-jwt-access-token` declares no local runtime dependency and has no direct consumer in the active manifest graph. Browse the [55-profiles layer](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/55-profiles) for adjacent package responsibilities; adjacency does not imply a dependency.

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/55-profiles/tba-profile-oauth-jwt-access-token)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-oauth-jwt-access-token/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-oauth-jwt-access-token/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-oauth-jwt-access-token/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-profile-oauth-jwt-access-token/)

## Governance

`tba-profile-oauth-jwt-access-token` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `55-profiles` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

See the [related repository tests](https://github.com/tigrbl/tigrbl_auth/blob/master/tests/unit/test_oidc_id_and_jwt_access_token_profiles.py) for the implementation scope covered by this example.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [tba-app-backend-public](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/90-backend-apps/tba-app-backend-public#readme) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)
