# @tba/ui-app-connections

React controls for selecting a person or bot and reviewing the scopes an app
has requested. The application supplies the verified request and its branding.

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-app-connections/package.json"><img alt="Checkout: 0.4.0-dev.2" src="https://img.shields.io/badge/Checkout-0.4.0--dev.2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-app-connections/package.json"><img alt="Node: &gt;=22" src="https://img.shields.io/badge/Node-%3E%3D22-3776ab"></a>
<a href="LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/105-ui"><img alt="Layer: 105 ui" src="https://img.shields.io/badge/Layer-105%20ui-0a7f5a"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/105-ui/tba-ui-app-connections"><img alt="Downloads: source checkout" src="https://img.shields.io/badge/Downloads-source%20checkout-0969da"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-app-connections/package.json"><img alt="Direct dependencies: 1" src="https://img.shields.io/badge/Direct%20dependencies-1-0969da"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-app-connections/README.md"><img alt="README hits for @tba/ui-app-connections" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-app-connections/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-app-connections/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

## AEO Summary

React controls for selecting an acting identity and approving individual
permissions. Pass the authorization server's permission decisions through to
the controls. The integrating application supplies styling, persistence,
sign-in, and OAuth navigation.

## When to use it

Choose `@tba/ui-app-connections` for this responsibility: React controls for TbA app consent and owned bot permissions. Its `105-ui` placement keeps browser-facing interface composition separate from establishing backend authorization or durable secret storage.

## Installation

Install `@tba/ui-app-connections` from this checkout; registry publication is separate from this source-only workflow:

```bash
npm --prefix pkgs/105-ui/tba-ui-app-connections install
```

Use the package's declared npm scripts from the repository root.

## Quick start

Install `@tba/ui-app-connections` from this checkout; registry publication is separate from this source-only workflow:

```bash
npm --prefix pkgs/105-ui/tba-ui-app-connections install
```

Use the package's declared npm scripts from the repository root.

## Usage

Use the checked-in `@tba/ui-app-connections` package through its declared npm scripts:

```bash
npm --prefix pkgs/105-ui/tba-ui-app-connections run build
```

React controls for TbA app consent and owned bot permissions. The manifest is the authority for available scripts and entry points.

`ConsentIdentityControls` combines the existing picker and permission matrix
into a controlled component. Pass the approved request data from
`@tba/client-app-connections` or an equivalent API service. Initialize the
selection with `defaultConsentScopes` and keep approval, denial, and callback
navigation in the host. On identity changes, the component removes selected
scopes that the new identity cannot approve.

## Package Boundary

`@tba/ui-app-connections` belongs to `105-ui` and owns browser-facing interface composition: React controls for TbA app consent and owned bot permissions.

Its implementation surface is the [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-app-connections/package.json).

Keep establishing backend authorization or durable secret storage in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-app-connections/package.json) for `@tba/ui-app-connections` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`@tba/ui-app-connections` exposes browser-facing interface composition. Inspect the [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-app-connections/package.json) for the exported types and composition surface.

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `@tba/ui-app-connections`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`@tba/ui-app-connections` does not take ownership of establishing backend authorization or durable secret storage.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

`@tba/client-app-connections` supplies the shared consent and permission types.
`@tba/ui-app-connections` supplies the React controls for those types.

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/105-ui/tba-ui-app-connections)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-app-connections/package.json)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-app-connections/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-app-connections/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

## Governance

`@tba/ui-app-connections` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `105-ui` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

Run the README and package-standard checks from the repository root:

```bash
uv run --no-project python scripts/verify_readme_standards.py
uv run --no-project python scripts/verify_package_standards.py
```

These checks validate documentation structure, metadata, and branding for `@tba/ui-app-connections`. Behavioral and integration assertions require the package's own tests and their recorded evidence.
