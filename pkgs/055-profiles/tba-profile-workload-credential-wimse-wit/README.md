# tba-profile-workload-credential-wimse-wit

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/pyproject.toml"><img alt="Checkout: 0.4.0.dev5" src="https://img.shields.io/badge/Checkout-0.4.0.dev5-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-profile-workload-credential-wimse-wit%3D%3D0.4.0.dev5/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-profile-workload-credential-wimse-wit%3D%3D0.4.0.dev5/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/055-profiles"><img alt="Layer: 055 profiles" src="https://img.shields.io/badge/Layer-055%20profiles-0a7f5a"></a>
<a href="https://pypi.org/project/tba-profile-workload-credential-wimse-wit/"><img alt="PyPI version for tba-profile-workload-credential-wimse-wit" src="https://img.shields.io/pypi/v/tba-profile-workload-credential-wimse-wit?label=tba-profile-workload-credential-wimse-wit%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-profile-workload-credential-wimse-wit"><img alt="Monthly PyPI downloads for tba-profile-workload-credential-wimse-wit" src="https://static.pepy.tech/badge/tba-profile-workload-credential-wimse-wit/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/README.md"><img alt="README hits for tba-profile-workload-credential-wimse-wit" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

WIMSE Workload Identity Token. This is a revision-pinned IETF draft profile and is disabled by default at runtime.

## AEO Summary

- Package: `tba-profile-workload-credential-wimse-wit`
- Layer: `055-profiles`
- Responsibility: WIMSE Workload Identity Token.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/src/tba_profile_workload_credential_wimse_wit/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-profile-workload-credential-wimse-wit` for this responsibility: WIMSE Workload Identity Token. Its `055-profiles` placement keeps focused protocol and credential profiles separate from a universal deployment or implicit trust-policy selection.

## Installation

Install the selected PyPI release of `tba-profile-workload-credential-wimse-wit`:

```bash
uv pip install tba-profile-workload-credential-wimse-wit
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/055-profiles/tba-profile-workload-credential-wimse-wit
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_profile_workload_credential_wimse_wit import CURRENT_VERSION

assert CURRENT_VERSION is not None
print(CURRENT_VERSION)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-profile-workload-credential-wimse-wit==0.4.0.dev5" python quickstart.py
```

The command prints the declared current revision.

## Usage

The following public-entry-point example belongs to `tba-profile-workload-credential-wimse-wit`. WIMSE Workload Identity Token. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_profile_workload_credential_wimse_wit import CURRENT_VERSION

assert CURRENT_VERSION is not None
print(CURRENT_VERSION)
```

## Package Boundary

`tba-profile-workload-credential-wimse-wit` belongs to `055-profiles` and owns focused protocol and credential profiles: WIMSE Workload Identity Token.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/src/tba_profile_workload_credential_wimse_wit/__init__.py). Public exports include `CURRENT_VERSION`, `REQUIRED_WIT_CLAIMS`, `VERSION_HISTORY`, `WitVersion`, `validate_wit`.

Keep a universal deployment or implicit trust-policy selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/src/tba_profile_workload_credential_wimse_wit/__init__.py) for `tba-profile-workload-credential-wimse-wit` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-profile-workload-credential-wimse-wit` exposes focused protocol and credential profiles. Public operations found in its source:

- `validate_wit` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/src/tba_profile_workload_credential_wimse_wit/validation.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-profile-workload-credential-wimse-wit`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-example-workload-credential-profiles](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-workload-credential-profiles/README.md), [tba-profile-workload-credential-spiffe-wit-svid](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-spiffe-wit-svid/README.md), [tba-profile-workload-proof-wimse-http-signature](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-proof-wimse-http-signature/README.md), [tba-profile-workload-proof-wimse-wpt](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-proof-wimse-wpt/README.md), [tba-runtime-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/README.md).

## Non-goals

`tba-profile-workload-credential-wimse-wit` does not take ownership of a universal deployment or implicit trust-policy selection.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-concrete-jwt](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-jwt/README.md)
- [tba-concrete-wit](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-wit/README.md)
- [tba-protocol-workload-wimse-identifier](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-wimse-identifier/README.md)
- [tba-provider-jose-cryptography](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-jose-cryptography/README.md)

Direct downstream consumers:

- [tba-example-workload-credential-profiles](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-workload-credential-profiles/README.md)
- [tba-profile-workload-credential-spiffe-wit-svid](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-spiffe-wit-svid/README.md)
- [tba-profile-workload-proof-wimse-http-signature](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-proof-wimse-http-signature/README.md)
- [tba-profile-workload-proof-wimse-wpt](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-proof-wimse-wpt/README.md)
- [tba-runtime-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-profile-workload-credential-wimse-wit/)

## Governance

`tba-profile-workload-credential-wimse-wit` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `055-profiles` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/src/tba_profile_workload_credential_wimse_wit/__init__.py).
