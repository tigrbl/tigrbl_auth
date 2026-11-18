# tba-profile-workload-authentication-wimse-mtls

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-authentication-wimse-mtls/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-authentication-wimse-mtls/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-profile-workload-authentication-wimse-mtls%3D%3D0.4.0.dev3/pkgs/55-profiles/tba-profile-workload-authentication-wimse-mtls/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-profile-workload-authentication-wimse-mtls%3D%3D0.4.0.dev3/pkgs/55-profiles/tba-profile-workload-authentication-wimse-mtls/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/55-profiles"><img alt="Layer: 55 profiles" src="https://img.shields.io/badge/Layer-55%20profiles-0a7f5a"></a>
<a href="https://pypi.org/project/tba-profile-workload-authentication-wimse-mtls/"><img alt="PyPI version for tba-profile-workload-authentication-wimse-mtls" src="https://img.shields.io/pypi/v/tba-profile-workload-authentication-wimse-mtls?label=tba-profile-workload-authentication-wimse-mtls%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-profile-workload-authentication-wimse-mtls"><img alt="Monthly PyPI downloads for tba-profile-workload-authentication-wimse-mtls" src="https://static.pepy.tech/badge/tba-profile-workload-authentication-wimse-mtls/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-authentication-wimse-mtls/README.md"><img alt="README hits for tba-profile-workload-authentication-wimse-mtls" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-authentication-wimse-mtls/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-authentication-wimse-mtls/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Verify workload identity from a trusted mTLS peer and configured domain trust.

## AEO Summary

- Package: `tba-profile-workload-authentication-wimse-mtls`
- Layer: `55-profiles`
- Responsibility: WIMSE mutual TLS workload authentication profile.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-authentication-wimse-mtls/src/tba_profile_workload_authentication_wimse_mtls/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-profile-workload-authentication-wimse-mtls` for this responsibility: WIMSE mutual TLS workload authentication profile. Its `55-profiles` placement keeps focused protocol and credential profiles separate from a universal deployment or implicit trust-policy selection.

## Installation

Install the selected PyPI release of `tba-profile-workload-authentication-wimse-mtls`:

```bash
uv pip install tba-profile-workload-authentication-wimse-mtls
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/55-profiles/tba-profile-workload-authentication-wimse-mtls
```

## Quick start

Build the package from the repository root.

```bash
uv build --wheel pkgs/55-profiles/tba-profile-workload-authentication-wimse-mtls
```

## Usage

The following public-entry-point example belongs to `tba-profile-workload-authentication-wimse-mtls`. WIMSE mutual TLS workload authentication profile. Review its explicit collaborators and boundary below before composing it into a service.

```python
import tba_profile_workload_authentication_wimse_mtls

print(tba_profile_workload_authentication_wimse_mtls.__name__)
```

## Package Boundary

`tba-profile-workload-authentication-wimse-mtls` belongs to `55-profiles` and owns focused protocol and credential profiles: WIMSE mutual TLS workload authentication profile.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-authentication-wimse-mtls/src/tba_profile_workload_authentication_wimse_mtls/__init__.py). Public exports include `TLSPeer`, `verify_wimse_peer`, `SPECIFICATION_URI`, `SPECIFICATION_VERSION`.

Keep a universal deployment or implicit trust-policy selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-profile-workload-authentication-wimse-mtls`:

- `verify_wimse_peer` construction inputs: `expected_identity`, `validators_by_domain`, `status_provider`, `now`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-authentication-wimse-mtls/src/tba_profile_workload_authentication_wimse_mtls/verification.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-profile-workload-authentication-wimse-mtls` exposes focused protocol and credential profiles. Public operations found in its source:

- `verify_wimse_peer` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-authentication-wimse-mtls/src/tba_profile_workload_authentication_wimse_mtls/verification.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-profile-workload-authentication-wimse-mtls`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-runtime-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/README.md).

## Non-goals

`tba-profile-workload-authentication-wimse-mtls` does not take ownership of a universal deployment or implicit trust-policy selection.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-concrete-certificate-x509](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-certificate-x509/README.md)
- [tba-concrete-wic](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-wic/README.md)
- [tba-contracts-security-trust](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-security-trust/README.md)
- [tba-profile-workload-credential-wimse-wic](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-credential-wimse-wic/README.md)
- [tba-protocol-workload-wimse-identifier](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-workload-wimse-identifier/README.md)

Direct downstream consumers:

- [tba-runtime-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/55-profiles/tba-profile-workload-authentication-wimse-mtls)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-authentication-wimse-mtls/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-authentication-wimse-mtls/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-authentication-wimse-mtls/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-profile-workload-authentication-wimse-mtls/)

## Governance

`tba-profile-workload-authentication-wimse-mtls` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `55-profiles` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

Check that the build produces a wheel with the package version declared in `pyproject.toml`.
