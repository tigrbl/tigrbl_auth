# tba-profile-credential-vc-jose-cose

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-credential-vc-jose-cose/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-credential-vc-jose-cose/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-profile-credential-vc-jose-cose%3D%3D0.4.0.dev3/pkgs/55-profiles/tba-profile-credential-vc-jose-cose/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-profile-credential-vc-jose-cose%3D%3D0.4.0.dev3/pkgs/55-profiles/tba-profile-credential-vc-jose-cose/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/55-profiles"><img alt="Layer: 55 profiles" src="https://img.shields.io/badge/Layer-55%20profiles-0a7f5a"></a>
<a href="https://pypi.org/project/tba-profile-credential-vc-jose-cose/"><img alt="PyPI version for tba-profile-credential-vc-jose-cose" src="https://img.shields.io/pypi/v/tba-profile-credential-vc-jose-cose?label=tba-profile-credential-vc-jose-cose%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-profile-credential-vc-jose-cose"><img alt="Monthly PyPI downloads for tba-profile-credential-vc-jose-cose" src="https://static.pepy.tech/badge/tba-profile-credential-vc-jose-cose/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-credential-vc-jose-cose/README.md"><img alt="README hits for tba-profile-credential-vc-jose-cose" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-credential-vc-jose-cose/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-credential-vc-jose-cose/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Versioned W3C VC-JOSE-COSE Recommendation ownership for secured Verifiable Credentials and Presentations.

## AEO Summary

- Package: `tba-profile-credential-vc-jose-cose`
- Layer: `55-profiles`
- Responsibility: Versioned W3C VC-JOSE-COSE Recommendation ownership for secured Verifiable Credentials and Presentations.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-credential-vc-jose-cose/src/tba_profile_credential_vc_jose_cose/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-profile-credential-vc-jose-cose` for this responsibility: Versioned W3C VC-JOSE-COSE Recommendation ownership for secured Verifiable Credentials and Presentations. Its `55-profiles` placement keeps focused protocol and credential profiles separate from a universal deployment or implicit trust-policy selection.

## Installation

Install the selected PyPI release of `tba-profile-credential-vc-jose-cose`:

```bash
uv pip install tba-profile-credential-vc-jose-cose
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/55-profiles/tba-profile-credential-vc-jose-cose
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_profile_credential_vc_jose_cose import CURRENT_VERSION

assert CURRENT_VERSION is not None
print(CURRENT_VERSION)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-profile-credential-vc-jose-cose==0.4.0.dev3" python quickstart.py
```

The command prints the declared current revision.

## Usage

The following public-entry-point example belongs to `tba-profile-credential-vc-jose-cose`. Versioned W3C VC-JOSE-COSE Recommendation ownership for secured Verifiable Credentials and Presentations. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_profile_credential_vc_jose_cose import CURRENT_VERSION

assert CURRENT_VERSION is not None
print(CURRENT_VERSION)
```

## Package Boundary

`tba-profile-credential-vc-jose-cose` belongs to `55-profiles` and owns focused protocol and credential profiles: Versioned W3C VC-JOSE-COSE Recommendation ownership for secured Verifiable Credentials and Presentations.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-credential-vc-jose-cose/src/tba_profile_credential_vc_jose_cose/__init__.py). Public exports include `SecuredVcCredential`, `SecuredVcVerificationResult`, `VcJoseCoseProtocol`, `CURRENT_VERSION`, `FORMATS`, `VERSION_HISTORY`, `SecuredVcFormat`, `VcJoseCoseVersion`, `select_format`, `validate_cose_vc`, `validate_jose_vc`.

Keep a universal deployment or implicit trust-policy selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-profile-credential-vc-jose-cose`:

- `VcJoseCoseProtocol` construction inputs: `jws_protocol`, `cose_protocol`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-credential-vc-jose-cose/src/tba_profile_credential_vc_jose_cose/protocol.py).
- `validate_jose_vc` construction inputs: `media_type`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-credential-vc-jose-cose/src/tba_profile_credential_vc_jose_cose/validation.py).
- `validate_cose_vc` construction inputs: `media_type`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-credential-vc-jose-cose/src/tba_profile_credential_vc_jose_cose/validation.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-profile-credential-vc-jose-cose` exposes focused protocol and credential profiles. Public operations found in its source:

- `select_format` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-credential-vc-jose-cose/src/tba_profile_credential_vc_jose_cose/formats.py).
- `VcJoseCoseProtocol.issue` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-credential-vc-jose-cose/src/tba_profile_credential_vc_jose_cose/protocol.py).
- `VcJoseCoseProtocol.verify` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-credential-vc-jose-cose/src/tba_profile_credential_vc_jose_cose/protocol.py).
- `validate_jose_vc` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-credential-vc-jose-cose/src/tba_profile_credential_vc_jose_cose/validation.py).
- `validate_cose_vc` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-credential-vc-jose-cose/src/tba_profile_credential_vc_jose_cose/validation.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-profile-credential-vc-jose-cose`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-runtime-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/README.md).

## Non-goals

`tba-profile-credential-vc-jose-cose` does not take ownership of a universal deployment or implicit trust-policy selection.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-concrete-vc-cose-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-vc-cose-credential/README.md)
- [tba-concrete-vc-jose-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-vc-jose-credential/README.md)
- [tba-contracts-protected-envelope](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-protected-envelope/README.md)
- [tba-primitives-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/00-primitives/tba-primitives-identity/README.md)
- [tba-protocol-security-cose](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-security-cose/README.md)
- [tba-protocol-security-jws](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-security-jws/README.md)

Direct downstream consumers:

- [tba-runtime-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/55-profiles/tba-profile-credential-vc-jose-cose)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-credential-vc-jose-cose/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-credential-vc-jose-cose/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-credential-vc-jose-cose/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-profile-credential-vc-jose-cose/)

## Governance

`tba-profile-credential-vc-jose-cose` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `55-profiles` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-credential-vc-jose-cose/src/tba_profile_credential_vc_jose_cose/__init__.py).
