# tba-profile-workload-credential-cwt-svid-extension

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-cwt-svid-extension/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-cwt-svid-extension/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-profile-workload-credential-cwt-svid-extension%3D%3D0.4.0.dev3/pkgs/055-profiles/tba-profile-workload-credential-cwt-svid-extension/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-profile-workload-credential-cwt-svid-extension%3D%3D0.4.0.dev3/pkgs/055-profiles/tba-profile-workload-credential-cwt-svid-extension/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/055-profiles"><img alt="Layer: 055 profiles" src="https://img.shields.io/badge/Layer-055%20profiles-0a7f5a"></a>
<a href="https://pypi.org/project/tba-profile-workload-credential-cwt-svid-extension/"><img alt="PyPI version for tba-profile-workload-credential-cwt-svid-extension" src="https://img.shields.io/pypi/v/tba-profile-workload-credential-cwt-svid-extension?label=tba-profile-workload-credential-cwt-svid-extension%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-profile-workload-credential-cwt-svid-extension"><img alt="Monthly PyPI downloads for tba-profile-workload-credential-cwt-svid-extension" src="https://static.pepy.tech/badge/tba-profile-workload-credential-cwt-svid-extension/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-cwt-svid-extension/README.md"><img alt="README hits for tba-profile-workload-credential-cwt-svid-extension" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-cwt-svid-extension/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-cwt-svid-extension/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Experimental Tigrbl CWT/COSE workload credential using SPIFFE IDs. This is not a SPIFFE SVID and makes no SPIFFE conformance claim. Disabled by default.

## AEO Summary

- Package: `tba-profile-workload-credential-cwt-svid-extension`
- Layer: `055-profiles`
- Responsibility: Experimental Tigrbl CWT/COSE workload credential using SPIFFE IDs.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-cwt-svid-extension/src/tba_profile_workload_credential_cwt_svid_extension/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-profile-workload-credential-cwt-svid-extension` for this responsibility: Experimental Tigrbl CWT/COSE workload credential using SPIFFE IDs. Its `055-profiles` placement keeps focused protocol and credential profiles separate from a universal deployment or implicit trust-policy selection.

## Installation

Install the selected PyPI release of `tba-profile-workload-credential-cwt-svid-extension`:

```bash
uv pip install tba-profile-workload-credential-cwt-svid-extension
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/055-profiles/tba-profile-workload-credential-cwt-svid-extension
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_profile_workload_credential_cwt_svid_extension import CURRENT_VERSION

assert CURRENT_VERSION is not None
print(CURRENT_VERSION)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-profile-workload-credential-cwt-svid-extension==0.4.0.dev3" python quickstart.py
```

The command prints the declared current revision.

## Usage

The following public-entry-point example belongs to `tba-profile-workload-credential-cwt-svid-extension`. Experimental Tigrbl CWT/COSE workload credential using SPIFFE IDs. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_profile_workload_credential_cwt_svid_extension import CURRENT_VERSION

assert CURRENT_VERSION is not None
print(CURRENT_VERSION)
```

## Package Boundary

`tba-profile-workload-credential-cwt-svid-extension` belongs to `055-profiles` and owns focused protocol and credential profiles: Experimental Tigrbl CWT/COSE workload credential using SPIFFE IDs.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-cwt-svid-extension/src/tba_profile_workload_credential_cwt_svid_extension/__init__.py). Public exports include `CwtSvidExtensionVerifier`, `CURRENT_VERSION`, `EXPERIMENTAL_EXTENSION`, `REQUIRED_CWT_LABELS`, `SPIFFE_CONFORMANT`, `VERSION_HISTORY`, `CwtSvidExtensionVersion`, `validate_cwt_svid_extension`.

Keep a universal deployment or implicit trust-policy selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-profile-workload-credential-cwt-svid-extension`:

- `validate_cwt_svid_extension` construction inputs: `proof_result`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-cwt-svid-extension/src/tba_profile_workload_credential_cwt_svid_extension/validation.py).
- `CwtSvidExtensionVerifier` construction inputs: `cwt_protocol`, `proof_verifier`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-cwt-svid-extension/src/tba_profile_workload_credential_cwt_svid_extension/verification.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-profile-workload-credential-cwt-svid-extension` exposes focused protocol and credential profiles. Public operations found in its source:

- `validate_cwt_svid_extension` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-cwt-svid-extension/src/tba_profile_workload_credential_cwt_svid_extension/validation.py).
- `CwtSvidExtensionVerifier.verify` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-cwt-svid-extension/src/tba_profile_workload_credential_cwt_svid_extension/verification.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-profile-workload-credential-cwt-svid-extension`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-runtime-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/README.md).

## Non-goals

`tba-profile-workload-credential-cwt-svid-extension` does not take ownership of a universal deployment or implicit trust-policy selection.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-contracts-proof-of-possession](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-proof-of-possession/README.md)
- [tba-protocol-cwt](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-cwt/README.md)
- [tba-protocol-security-cose](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-cose/README.md)
- [tba-protocol-workload-spiffe-svid](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-svid/README.md)

Direct downstream consumers:

- [tba-runtime-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/055-profiles/tba-profile-workload-credential-cwt-svid-extension)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-cwt-svid-extension/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-cwt-svid-extension/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-cwt-svid-extension/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-profile-workload-credential-cwt-svid-extension/)

## Governance

`tba-profile-workload-credential-cwt-svid-extension` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `055-profiles` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-cwt-svid-extension/src/tba_profile_workload_credential_cwt_svid_extension/__init__.py).
