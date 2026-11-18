# TbA interop matrix validation (`tba-tests-interop-wimse-matrix`)

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-wimse-matrix/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-wimse-matrix/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/120-tests"><img alt="Layer: 120 tests" src="https://img.shields.io/badge/Layer-120%20tests-0a7f5a"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/120-tests/tba-tests-interop-wimse-matrix"><img alt="Downloads: source checkout" src="https://img.shields.io/badge/Downloads-source%20checkout-0969da"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-wimse-matrix/README.md"><img alt="README hits for tba-tests-interop-wimse-matrix" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-wimse-matrix/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-wimse-matrix/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

T0–T2 checks for the [interop distribution](https://github.com/tigrbl/tba-tests-interop-wimse).

## AEO Summary

- Package: `tba-tests-interop-wimse-matrix`
- Layer: `120-tests`
- Responsibility: Offline WIMSE interoperability matrix and wheel validation for TbA.
- Public surface: [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-wimse-matrix/pyproject.toml).
- Distribution: repository development harness.

## When to use it

Choose `tba-tests-interop-wimse-matrix` for this responsibility: Offline WIMSE interoperability matrix and wheel validation for TbA. Its `120-tests` placement keeps test fixtures and executable verification separate from production identity services or deployable policy defaults.

## Installation

`tba-tests-interop-wimse-matrix` is a workspace-only harness (`tool.uv.package = false`), so install the repository development environment rather than a nonexistent wheel:

```bash
uv sync --group dev
```

Run the package's verification commands from the repository root.

## Quick start

Set `TBA_WIMSE_INTEROP_PACKAGE` to the package at the revision in
`interop-revision.txt` and `TBA_WIMSE_INTEROP_WHEEL` to its built wheel.
From the TbA checkout, run:

```sh
uv run --locked --extra test pytest pkgs/120-tests/tba-tests-interop-wimse-matrix/tests
```

## Usage

Use `tba-tests-interop-wimse-matrix` through its repository test harness rather than as a production runtime import:

```bash
uv run pytest pkgs/120-tests/tba-tests-interop-wimse-matrix
```

Its fixtures and checks support the integration workflow documented in Quick start.

## Package Boundary

`tba-tests-interop-wimse-matrix` belongs to `120-tests` and owns test fixtures and executable verification: Offline WIMSE interoperability matrix and wheel validation for TbA.

Its implementation surface is the [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-wimse-matrix/pyproject.toml).

Keep production identity services or deployable policy defaults in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-wimse-matrix/pyproject.toml) for `tba-tests-interop-wimse-matrix` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-tests-interop-wimse-matrix` exposes test fixtures and executable verification. Inspect the [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-wimse-matrix/pyproject.toml) for the exported types and composition surface.

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-tests-interop-wimse-matrix`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`tba-tests-interop-wimse-matrix` does not take ownership of production identity services or deployable policy defaults.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

`tba-tests-interop-wimse-matrix` declares no local runtime dependency and has no direct consumer in the active manifest graph. Browse the [120-tests layer](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/120-tests) for adjacent package responsibilities; adjacency does not imply a dependency.

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/120-tests/tba-tests-interop-wimse-matrix)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-wimse-matrix/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-wimse-matrix/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-wimse-matrix/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

## Governance

`tba-tests-interop-wimse-matrix` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `120-tests` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

The TbA WIMSE matrix validation workflow runs the catalog, inventory, evidence,
and installed-wheel checks against the pinned interop revision.
