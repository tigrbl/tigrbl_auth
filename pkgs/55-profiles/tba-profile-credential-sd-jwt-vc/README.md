# tba-profile-credential-sd-jwt-vc

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-credential-sd-jwt-vc/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-credential-sd-jwt-vc/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-profile-credential-sd-jwt-vc%3D%3D0.4.0.dev3/pkgs/55-profiles/tba-profile-credential-sd-jwt-vc/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-profile-credential-sd-jwt-vc%3D%3D0.4.0.dev3/pkgs/55-profiles/tba-profile-credential-sd-jwt-vc/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/55-profiles"><img alt="Layer: 55 profiles" src="https://img.shields.io/badge/Layer-55%20profiles-0a7f5a"></a>
<a href="https://pypi.org/project/tba-profile-credential-sd-jwt-vc/"><img alt="PyPI version for tba-profile-credential-sd-jwt-vc" src="https://img.shields.io/pypi/v/tba-profile-credential-sd-jwt-vc?label=tba-profile-credential-sd-jwt-vc%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-profile-credential-sd-jwt-vc"><img alt="Monthly PyPI downloads for tba-profile-credential-sd-jwt-vc" src="https://static.pepy.tech/badge/tba-profile-credential-sd-jwt-vc/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-credential-sd-jwt-vc/README.md"><img alt="README hits for tba-profile-credential-sd-jwt-vc" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-credential-sd-jwt-vc/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-credential-sd-jwt-vc/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Owns versioned protocol composition and compatibility.

## AEO Summary

- Package: `tba-profile-credential-sd-jwt-vc`
- Layer: `55-profiles`
- Responsibility: Selective Disclosure JWT Verifiable Credential profile.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-credential-sd-jwt-vc/src/tba_profile_credential_sd_jwt_vc/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-profile-credential-sd-jwt-vc` for this responsibility: Selective Disclosure JWT Verifiable Credential profile. Its `55-profiles` placement keeps focused protocol and credential profiles separate from a universal deployment or implicit trust-policy selection.

## Installation

Install the selected PyPI release of `tba-profile-credential-sd-jwt-vc`:

```bash
uv pip install tba-profile-credential-sd-jwt-vc
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/55-profiles/tba-profile-credential-sd-jwt-vc
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_profile_credential_sd_jwt_vc import CURRENT_VERSION

assert CURRENT_VERSION is not None
print(CURRENT_VERSION)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-profile-credential-sd-jwt-vc==0.4.0.dev3" python quickstart.py
```

The command prints the declared current revision.

## Usage

The following public-entry-point example belongs to `tba-profile-credential-sd-jwt-vc`. Selective Disclosure JWT Verifiable Credential profile. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_profile_credential_sd_jwt_vc import CURRENT_VERSION

assert CURRENT_VERSION is not None
print(CURRENT_VERSION)
```

## Package Boundary

`tba-profile-credential-sd-jwt-vc` belongs to `55-profiles` and owns focused protocol and credential profiles: Selective Disclosure JWT Verifiable Credential profile.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-credential-sd-jwt-vc/src/tba_profile_credential_sd_jwt_vc/__init__.py). Public exports include `CAPABILITY_REQUIREMENTS`, `COMPATIBILITY_PATHS`, `CURRENT_VERSION`, `DRAFT_REVISION`, `FEATURES_BY_VERSION`, `LEGACY_SD_JWT_VC_TYP`, `MEDIA_TYPE`, `SD_JWT_VC_CARRIER`, `SD_JWT_VC_CLAIM_CLASSES`, `SdJwtVcClaimSetPayload`, `SdJwtVcCredential`, `SdJwtVcStatusReference`.

Keep a universal deployment or implicit trust-policy selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-profile-credential-sd-jwt-vc`:

- `migrate_claims` construction inputs: `source`, `target`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-credential-sd-jwt-vc/src/tba_profile_credential_sd_jwt_vc/migrations.py).
- `validate_sd_jwt_vc` construction inputs: `accept_legacy_typ`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-credential-sd-jwt-vc/src/tba_profile_credential_sd_jwt_vc/validation.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-profile-credential-sd-jwt-vc` exposes focused protocol and credential profiles. Public operations found in its source:

- `capability_report` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-credential-sd-jwt-vc/src/tba_profile_credential_sd_jwt_vc/__init__.py).
- `parse_sd_jwt_vc` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-credential-sd-jwt-vc/src/tba_profile_credential_sd_jwt_vc/artifact.py).
- `parse_sd_jwt_vc_claims` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-credential-sd-jwt-vc/src/tba_profile_credential_sd_jwt_vc/claims.py).
- `compose_sd_jwt_vc_claim_set` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-credential-sd-jwt-vc/src/tba_profile_credential_sd_jwt_vc/claims.py).
- `compatibility` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-credential-sd-jwt-vc/src/tba_profile_credential_sd_jwt_vc/compatibility.py).
- `supports` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-credential-sd-jwt-vc/src/tba_profile_credential_sd_jwt_vc/features.py).
- `parse_type_metadata` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-credential-sd-jwt-vc/src/tba_profile_credential_sd_jwt_vc/metadata.py).
- `migrate_claims` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-credential-sd-jwt-vc/src/tba_profile_credential_sd_jwt_vc/migrations.py).
- `select_carrier` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-credential-sd-jwt-vc/src/tba_profile_credential_sd_jwt_vc/schemas.py).
- `parse_status_reference` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-credential-sd-jwt-vc/src/tba_profile_credential_sd_jwt_vc/status.py).
- `validate_sd_jwt_vc` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-credential-sd-jwt-vc/src/tba_profile_credential_sd_jwt_vc/validation.py).
- `select_version` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-credential-sd-jwt-vc/src/tba_profile_credential_sd_jwt_vc/versions.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-profile-credential-sd-jwt-vc`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

Higher-layer orchestration, lower-layer persistence, and protocol behavior outside this package's declared layer are not owned here.

## Related Packages

Declared local runtime dependencies:

- [tba-concrete-claim-credential-status](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-claim-credential-status/README.md)
- [tba-concrete-claim-credential-type](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-claim-credential-type/README.md)
- [tba-concrete-sd-jwt](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-sd-jwt/README.md)
- [tba-concrete-sd-jwt-vc-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-sd-jwt-vc-credential/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/55-profiles/tba-profile-credential-sd-jwt-vc)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-credential-sd-jwt-vc/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-credential-sd-jwt-vc/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-credential-sd-jwt-vc/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-profile-credential-sd-jwt-vc/)

## Governance

`tba-profile-credential-sd-jwt-vc` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `55-profiles` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-credential-sd-jwt-vc/src/tba_profile_credential_sd_jwt_vc/__init__.py).
