# tba-tests-identity

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-tests-identity%3D%3D0.4.0.dev3/pkgs/120-tests/tba-tests-identity/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-tests-identity%3D%3D0.4.0.dev3/pkgs/120-tests/tba-tests-identity/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/120-tests"><img alt="Layer: 120 tests" src="https://img.shields.io/badge/Layer-120%20tests-0a7f5a"></a>
<a href="https://pypi.org/project/tba-tests-identity/"><img alt="PyPI version for tba-tests-identity" src="https://img.shields.io/pypi/v/tba-tests-identity?label=tba-tests-identity%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-tests-identity"><img alt="Monthly PyPI downloads for tba-tests-identity" src="https://static.pepy.tech/badge/tba-tests-identity/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/README.md"><img alt="README hits for tba-tests-identity" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Reuse deterministic identity fixtures, fake flows, and cross-language vectors in tests.

## AEO Summary

- Package: `tba-tests-identity`
- Layer: `120-tests`
- Responsibility: Test fixtures, fake identity components, conformance vectors, integration harnesses, and cross-cutting verification helpers.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/src/tba_tests_identity/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Use the testkit for repeatable protocol and integration tests. Its fake providers and sample credentials are test fixtures. Real identity deployment and credential handling belong to the runtime and provider packages.

## Installation

Install the selected PyPI release of `tba-tests-identity`:

```bash
uv pip install tba-tests-identity
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/120-tests/tba-tests-identity
```

## Quick start

Install the version used by this example.

```bash
python -m pip install "tba-tests-identity==0.4.0.dev3"
```

Save the following as `quickstart.py` and run `python quickstart.py`. The assertions should pass.

```python
from tba_tests_identity import pkce_s256

verifier = "dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk"
assert pkce_s256(verifier) == "E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM"
```

## Usage

The following public-entry-point example belongs to `tba-tests-identity`. Test fixtures, fake identity components, conformance vectors, integration harnesses, and cross-cutting verification helpers. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_tests_identity import pkce_s256

verifier = "dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk"
assert pkce_s256(verifier) == "E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM"
```

## Package Boundary

`tba-tests-identity` belongs to `120-tests` and owns test fixtures and executable verification: Test fixtures, fake identity components, conformance vectors, integration harnesses, and cross-cutting verification helpers.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/src/tba_tests_identity/__init__.py). Public exports include `AuthorizationCode`, `FakeIdentityProvider`, `FakeRelyingParty`, `FakeResourceServer`, `MatrixCellStatus`, `PackageMatrixCell`, `PackageMatrixHarness`, `SeededClient`, `SeededTenant`, `SeededUser`, `TestkitError`, `TestkitProviderRuntimeProfile`.

Keep production identity services or deployable policy defaults in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-tests-identity`:

- `FakeIdentityProvider` construction inputs: `seeds`, `profile`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/src/tba_tests_identity/cross_cutting.py).
- `PackageMatrixHarness` construction inputs: `python_versions`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/src/tba_tests_identity/cross_cutting.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-tests-identity` exposes test fixtures and executable verification. Public operations found in its source:

- `pkce_s256` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/src/tba_tests_identity/cross_cutting.py).
- `TestkitSeedSet.client` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/src/tba_tests_identity/cross_cutting.py).
- `TestkitSeedSet.user` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/src/tba_tests_identity/cross_cutting.py).
- `TestkitProviderRuntimeProfile.require_route` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/src/tba_tests_identity/cross_cutting.py).
- `TestkitProviderRuntimeProfile.require_feature` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/src/tba_tests_identity/cross_cutting.py).
- `FakeIdentityProvider.discovery_document` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/src/tba_tests_identity/cross_cutting.py).
- `FakeIdentityProvider.jwks` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/src/tba_tests_identity/cross_cutting.py).
- `FakeIdentityProvider.authorize` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/src/tba_tests_identity/cross_cutting.py).
- `FakeIdentityProvider.token` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/src/tba_tests_identity/cross_cutting.py).
- `FakeIdentityProvider.introspect` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/src/tba_tests_identity/cross_cutting.py).
- `FakeIdentityProvider.userinfo` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/src/tba_tests_identity/cross_cutting.py).
- `FakeRelyingParty.authorization_url` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/src/tba_tests_identity/cross_cutting.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-tests-identity`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`tba-tests-identity` does not take ownership of production identity services or deployable policy defaults.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

`tba-tests-identity` declares no local runtime dependency and has no direct consumer in the active manifest graph. Browse the [120-tests layer](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/120-tests) for adjacent package responsibilities; adjacency does not imply a dependency.

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/120-tests/tba-tests-identity)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-tests-identity/)

## Governance

`tba-tests-identity` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `120-tests` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

See the [related repository tests](https://github.com/tigrbl/tigrbl_auth/blob/master/tests/unit/test_testkit_cross_cutting_boundary.py) for the implementation scope covered by this example.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [tba-protocol-cwt](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/50-protocols/tba-protocol-cwt#readme) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)
