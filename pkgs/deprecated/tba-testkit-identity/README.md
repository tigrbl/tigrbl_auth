# tba-testkit-identity (deprecated)

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/deprecated/tba-testkit-identity/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/deprecated/tba-testkit-identity/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-testkit-identity%3D%3D0.4.0.dev4/pkgs/deprecated/tba-testkit-identity/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-testkit-identity%3D%3D0.4.0.dev4/pkgs/deprecated/tba-testkit-identity/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/deprecated"><img alt="Layer: deprecated" src="https://img.shields.io/badge/Layer-deprecated-0a7f5a"></a>
<a href="https://pypi.org/project/tba-testkit-identity/"><img alt="PyPI version for tba-testkit-identity" src="https://img.shields.io/pypi/v/tba-testkit-identity?label=tba-testkit-identity%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-testkit-identity"><img alt="Monthly PyPI downloads for tba-testkit-identity" src="https://static.pepy.tech/badge/tba-testkit-identity/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/deprecated/tba-testkit-identity/README.md"><img alt="README hits for tba-testkit-identity" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/deprecated/tba-testkit-identity/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/deprecated/tba-testkit-identity/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Install [`tba-tests-identity`](https://pypi.org/project/tba-tests-identity/) and replace `tba_testkit_identity` imports with `tba_tests_identity`.

Existing installations can upgrade to this release using the original package name. Imports continue to work and emit `DeprecationWarning`. Use `python -W default` to display it.

## AEO Summary

- Package: `tba-testkit-identity`
- Layer: `deprecated`
- Responsibility: Deprecated compatibility package. Use tba-tests-identity.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/deprecated/tba-testkit-identity/src/tba_testkit_identity/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-testkit-identity` for this responsibility: Deprecated compatibility package. Use tba-tests-identity. Its `deprecated` placement keeps maintained compatibility imports separate from new implementation ownership or silently reversing deprecation.

## Installation

Install the selected PyPI release of `tba-testkit-identity`:

```bash
uv pip install tba-testkit-identity
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/deprecated/tba-testkit-identity
```

## Quick start

```bash
uv pip install "tba-testkit-identity==0.4.0.dev4"
```

## Usage

The following public-entry-point example belongs to `tba-testkit-identity`. Deprecated compatibility package. Use tba-tests-identity. Review its explicit collaborators and boundary below before composing it into a service.

```python
import tba_testkit_identity

print(tba_testkit_identity.__name__)
```

## Package Boundary

`tba-testkit-identity` belongs to `deprecated` and owns maintained compatibility imports: Deprecated compatibility package. Use tba-tests-identity.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/deprecated/tba-testkit-identity/src/tba_testkit_identity/__init__.py). Public exports include `AuthorizationCode`, `FakeIdentityProvider`, `FakeRelyingParty`, `FakeResourceServer`, `MatrixCellStatus`, `PackageMatrixCell`, `PackageMatrixHarness`, `SeededClient`, `SeededTenant`, `SeededUser`, `TestkitError`, `TestkitProviderRuntimeProfile`.

Keep new implementation ownership or silently reversing deprecation in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-testkit-identity`:

- `FakeIdentityProvider` construction inputs: `seeds`, `profile`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/deprecated/tba-testkit-identity/src/tba_testkit_identity/cross_cutting.py).
- `PackageMatrixHarness` construction inputs: `python_versions`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/deprecated/tba-testkit-identity/src/tba_testkit_identity/cross_cutting.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-testkit-identity` exposes maintained compatibility imports. Public operations found in its source:

- `pkce_s256` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/deprecated/tba-testkit-identity/src/tba_testkit_identity/cross_cutting.py).
- `TestkitSeedSet.client` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/deprecated/tba-testkit-identity/src/tba_testkit_identity/cross_cutting.py).
- `TestkitSeedSet.user` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/deprecated/tba-testkit-identity/src/tba_testkit_identity/cross_cutting.py).
- `TestkitProviderRuntimeProfile.require_route` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/deprecated/tba-testkit-identity/src/tba_testkit_identity/cross_cutting.py).
- `TestkitProviderRuntimeProfile.require_feature` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/deprecated/tba-testkit-identity/src/tba_testkit_identity/cross_cutting.py).
- `FakeIdentityProvider.discovery_document` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/deprecated/tba-testkit-identity/src/tba_testkit_identity/cross_cutting.py).
- `FakeIdentityProvider.jwks` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/deprecated/tba-testkit-identity/src/tba_testkit_identity/cross_cutting.py).
- `FakeIdentityProvider.authorize` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/deprecated/tba-testkit-identity/src/tba_testkit_identity/cross_cutting.py).
- `FakeIdentityProvider.token` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/deprecated/tba-testkit-identity/src/tba_testkit_identity/cross_cutting.py).
- `FakeIdentityProvider.introspect` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/deprecated/tba-testkit-identity/src/tba_testkit_identity/cross_cutting.py).
- `FakeIdentityProvider.userinfo` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/deprecated/tba-testkit-identity/src/tba_testkit_identity/cross_cutting.py).
- `FakeRelyingParty.authorization_url` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/deprecated/tba-testkit-identity/src/tba_testkit_identity/cross_cutting.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-testkit-identity`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`tba-testkit-identity` does not take ownership of new implementation ownership or silently reversing deprecation.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

`tba-testkit-identity` declares no local runtime dependency and has no direct consumer in the active manifest graph. Browse the [deprecated layer](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/deprecated) for adjacent package responsibilities; adjacency does not imply a dependency.

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/deprecated/tba-testkit-identity)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/deprecated/tba-testkit-identity/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/deprecated/tba-testkit-identity/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/deprecated/tba-testkit-identity/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-testkit-identity/)

## Governance

`tba-testkit-identity` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `deprecated` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

This maintained alias retains its deprecation policy and compatibility imports; new implementation work belongs to its active replacement.

## Verification

Package metadata, legal files, and README fragments are checked with
`uv run python scripts/verify_package_standards.py`. Compatibility imports
and deprecation warnings retain the already-published migration behavior.
