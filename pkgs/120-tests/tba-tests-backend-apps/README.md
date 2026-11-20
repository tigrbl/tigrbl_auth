# tba-tests-backend-apps

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-backend-apps/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-backend-apps/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/120-tests"><img alt="Layer: 120 tests" src="https://img.shields.io/badge/Layer-120%20tests-0a7f5a"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/120-tests/tba-tests-backend-apps"><img alt="Downloads: source checkout" src="https://img.shields.io/badge/Downloads-source%20checkout-0969da"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-backend-apps/README.md"><img alt="README hits for tba-tests-backend-apps" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-backend-apps/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-backend-apps/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Each directory under `tests/packages/` uses the distribution name of the
backend application under test. Package and realm tests run against the local
workspace or an isolated wheel installed by the package test matrix. Live
deployment proofs keep their existing environment settings and readiness checks.

Run all backend application tests from the repository root with
`uv run --extra test pytest --certification-lane all pkgs/120-tests/tba-tests-backend-apps/tests`.

## AEO Summary

- Package: `tba-tests-backend-apps`
- Layer: `120-tests`
- Responsibility: Package, realm, and deployment tests for TBA backend applications.
- Public surface: [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-backend-apps/pyproject.toml).
- Distribution: repository development harness.

## When to use it

Choose `tba-tests-backend-apps` for this responsibility: Package, realm, and deployment tests for TBA backend applications. Its `120-tests` placement keeps test fixtures and executable verification separate from production identity services or deployable policy defaults.

## Installation

`tba-tests-backend-apps` is a workspace-only harness (`tool.uv.package = false`), so install the repository development environment rather than a nonexistent wheel:

```bash
uv sync --group dev
```

Run the package's verification commands from the repository root.

## Quick start

`tba-tests-backend-apps` is a workspace-only harness (`tool.uv.package = false`), so install the repository development environment rather than a nonexistent wheel:

```bash
uv sync --group dev
```

Run the package's verification commands from the repository root.

## Usage

Use `tba-tests-backend-apps` through its repository test harness rather than as a production runtime import:

```bash
uv run pytest pkgs/120-tests/tba-tests-backend-apps
```

Its fixtures and checks support the integration workflow documented in Quick start.

## Package Boundary

`tba-tests-backend-apps` belongs to `120-tests` and owns test fixtures and executable verification: Package, realm, and deployment tests for TBA backend applications.

Its implementation surface is the [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-backend-apps/pyproject.toml).

Keep production identity services or deployable policy defaults in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-backend-apps/pyproject.toml) for `tba-tests-backend-apps` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-tests-backend-apps` exposes test fixtures and executable verification. Inspect the [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-backend-apps/pyproject.toml) for the exported types and composition surface.

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-tests-backend-apps`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`tba-tests-backend-apps` does not take ownership of production identity services or deployable policy defaults.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

`tba-tests-backend-apps` declares no local runtime dependency and has no direct consumer in the active manifest graph. Browse the [120-tests layer](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/120-tests) for adjacent package responsibilities; adjacency does not imply a dependency.

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/120-tests/tba-tests-backend-apps)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-backend-apps/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-backend-apps/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-backend-apps/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

## Governance

`tba-tests-backend-apps` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `120-tests` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

Run the README and package-standard checks from the repository root:

```bash
uv run --no-project python scripts/verify_readme_standards.py
uv run --no-project python scripts/verify_package_standards.py
```

These checks validate documentation structure, metadata, and branding for `tba-tests-backend-apps`. Behavioral and integration assertions require the package's own tests and their recorded evidence.
