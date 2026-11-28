# @tbauth/ui-developer

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-developer/package.json"><img alt="Checkout: 0.3.5" src="https://img.shields.io/badge/Checkout-0.3.5-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-developer/package.json"><img alt="Node: &gt;=22" src="https://img.shields.io/badge/Node-%3E%3D22-3776ab"></a>
<a href="LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/105-ui"><img alt="Layer: 105 ui" src="https://img.shields.io/badge/Layer-105%20ui-0a7f5a"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/105-ui/tba-ui-developer"><img alt="Downloads: source checkout" src="https://img.shields.io/badge/Downloads-source%20checkout-0969da"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-developer/package.json"><img alt="Direct dependencies: 6" src="https://img.shields.io/badge/Direct%20dependencies-6-0969da"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-developer/README.md"><img alt="README hits for @tbauth/ui-developer" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-developer/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-developer/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Developer UIX for OIDC/OAuth client registration, redirect URI management, client metadata, secrets, and client JWKS.

## AEO Summary

- Package: `@tbauth/ui-developer`
- Layer: `105-ui`
- Responsibility: Developer self-service UIX for OAuth/OIDC app registration.
- Public surface: [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-developer/package.json).
- Distribution: source checkout; npm publication is separate.

## When to use it

Choose `@tbauth/ui-developer` for this responsibility: Developer self-service UIX for OAuth/OIDC app registration. Its `105-ui` placement keeps browser-facing interface composition separate from establishing backend authorization or durable secret storage.

## Installation

Install `@tbauth/ui-developer` from this checkout; registry publication is separate from this source-only workflow:

```bash
npm --prefix pkgs/105-ui/tba-ui-developer install
```

Use the package's declared npm scripts from the repository root.

## Quick start

Use Node 22 or newer and run these commands from the repository root.

```bash
npm ci --no-audit --no-fund
npm run build -w @tbauth/ui-primitives
npm run build -w @tbauth/ui-developer
```

Expect a Vite build with `dist/index.html` in this package.

## Usage

Use the checked-in `@tbauth/ui-developer` package through its declared npm scripts:

```bash
npm --prefix pkgs/105-ui/tba-ui-developer run dev
```

Developer self-service UIX for OAuth/OIDC app registration. The manifest is the authority for available scripts and entry points.

## API Boundary

- Consumes `tba-app-backend-developer`.
- Uses exactly one configured base URL: `VITE_TBA_AUTH_DEVELOPER_BACKEND_APP_BASE_URL`.
- Allows client registration and developer-scoped RPC paths.
- Blocks tenant lifecycle and service identity administration.

## Package Boundary

`@tbauth/ui-developer` belongs to `105-ui` and owns browser-facing interface composition: Developer self-service UIX for OAuth/OIDC app registration.

Its implementation surface is the [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-developer/package.json).

Keep establishing backend authorization or durable secret storage in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-developer/package.json) for `@tbauth/ui-developer` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`@tbauth/ui-developer` exposes browser-facing interface composition. Inspect the [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-developer/package.json) for the exported types and composition surface.

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `@tbauth/ui-developer`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`@tbauth/ui-developer` does not take ownership of establishing backend authorization or durable secret storage.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [@tbauth/ui-primitives](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/100-uix-core/tba-ui-primitives/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/105-ui/tba-ui-developer)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-developer/package.json)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-developer/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-developer/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

## Governance

`@tbauth/ui-developer` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `105-ui` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

The build was checked using the [workspace lockfile](https://github.com/tigrbl/tigrbl_auth/blob/master/package-lock.json) and the [package build script](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-developer/package.json). Live account or administration actions require a configured TBA backend.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)
