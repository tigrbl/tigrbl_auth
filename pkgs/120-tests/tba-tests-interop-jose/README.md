# tba-tests-interop-jose

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-jose/pyproject.toml"><img alt="Checkout: 0.1.0" src="https://img.shields.io/badge/Checkout-0.1.0-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-jose/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-tests-interop-jose%3D%3D0.1.0/pkgs/120-tests/tba-tests-interop-jose/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-tests-interop-jose%3D%3D0.1.0/pkgs/120-tests/tba-tests-interop-jose/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/120-tests"><img alt="Layer: 120 tests" src="https://img.shields.io/badge/Layer-120%20tests-0a7f5a"></a>
<a href="https://pypi.org/project/tba-tests-interop-jose/"><img alt="PyPI version for tba-tests-interop-jose" src="https://img.shields.io/pypi/v/tba-tests-interop-jose?label=tba-tests-interop-jose%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-tests-interop-jose"><img alt="Monthly PyPI downloads for tba-tests-interop-jose" src="https://static.pepy.tech/badge/tba-tests-interop-jose/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-jose/README.md"><img alt="README hits for tba-tests-interop-jose" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-jose/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-jose/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Bidirectional compact JWE interoperability tests for TbA and Swarmauri.

## AEO Summary

- Package: `tba-tests-interop-jose`
- Layer: `120-tests`
- Responsibility: Bidirectional compact JWE interoperability tests for TbA and Swarmauri.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-jose/src/tba_tests_interop_jose/__init__.py).
- Distribution: test-only Python wheel with a pytest plugin.

## When to use it

Choose `tba-tests-interop-jose` for this responsibility: Bidirectional compact JWE interoperability tests for TbA and Swarmauri. Its `120-tests` placement keeps test fixtures and executable verification separate from production identity services or deployable policy defaults.

## Installation

Install the selected PyPI release of `tba-tests-interop-jose`:

```bash
uv pip install tba-tests-interop-jose
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/120-tests/tba-tests-interop-jose
```

## Quick start

Run both source-checkout directions from the TbA checkout with `SWARMAURI_SDK_ROOT` set to the Swarmauri checkout.

```bash
uv run --extra test pytest --tba-suite tba-tests-interop-jose --jose-interop-mode source
```

## Usage

For release verification, install this test wheel and pin the peer wheels in
a clean environment. The peer entry points are `swarmauri-crypto-jwe`,
`tba-concrete-jose`, `tba-capability-protected-envelope`,
`tba-protocol-security-jwe`, and `tba-provider-jose-cryptography`.
Run from outside both source checkouts. Installed mode verifies that both
peers resolve to their distribution records.

```bash
python -m pytest --pyargs tba_tests_interop_jose.tests --jose-interop-mode installed
```

## Package Boundary

`tba-tests-interop-jose` belongs to `120-tests` and owns test fixtures and executable verification: Bidirectional compact JWE interoperability tests for TbA and Swarmauri.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-jose/src/tba_tests_interop_jose/__init__.py).

Keep production identity services or deployable policy defaults in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-jose/src/tba_tests_interop_jose/__init__.py) for `tba-tests-interop-jose` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-tests-interop-jose` exposes test fixtures and executable verification. Inspect the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-jose/src/tba_tests_interop_jose/__init__.py) for the exported types and composition surface.

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-tests-interop-jose`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`tba-tests-interop-jose` does not take ownership of production identity services or deployable policy defaults.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

`tba-tests-interop-jose` declares no local runtime dependency and has no direct consumer in the active manifest graph. Browse the [120-tests layer](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/120-tests) for adjacent package responsibilities; adjacency does not imply a dependency.

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/120-tests/tba-tests-interop-jose)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-jose/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-jose/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-jose/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-tests-interop-jose/)

## Governance

`tba-tests-interop-jose` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `120-tests` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

Run the README and package-standard checks from the repository root:

```bash
uv run --no-project python scripts/verify_readme_standards.py
uv run --no-project python scripts/verify_package_standards.py
```

These checks validate documentation structure, metadata, and branding for `tba-tests-interop-jose`. Behavioral and integration assertions require the package's own tests and their recorded evidence.
