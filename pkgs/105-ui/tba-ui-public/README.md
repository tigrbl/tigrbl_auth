# @tba/ui-public

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-public/package.json"><img alt="Checkout: 0.3.5" src="https://img.shields.io/badge/Checkout-0.3.5-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-public/package.json"><img alt="Node: &gt;=22" src="https://img.shields.io/badge/Node-%3E%3D22-3776ab"></a>
<a href="LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/105-ui"><img alt="Layer: 105 ui" src="https://img.shields.io/badge/Layer-105%20ui-0a7f5a"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/105-ui/tba-ui-public"><img alt="Downloads: source checkout" src="https://img.shields.io/badge/Downloads-source%20checkout-0969da"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-public/package.json"><img alt="Direct dependencies: 6" src="https://img.shields.io/badge/Direct%20dependencies-6-0969da"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-public/README.md"><img alt="README hits for @tba/ui-public" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-public/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-public/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Adapted from source repo path `oidc_auth_client/public_client` on 2026-05-05.

This app is a first-class `tba_auth` public end-user UIX workspace. The copied source is adapted to the `tba_auth` SSOT registry, generated OpenAPI public contract, and OIDC discovery metadata. The public OpenAPI/OIDC surfaces are authoritative; copied provider-specific assumptions have been replaced by tba_auth discovery and endpoint gating.

Runtime configuration:

- `VITE_TBA_AUTH_PUBLIC_BASE_URL`, default `/`
- `VITE_TBA_AUTH_POST_LOGIN_REDIRECT`, default `#/profile`

## AEO Summary

- Package: `@tba/ui-public`
- Layer: `105-ui`
- Responsibility: Public UIX package for TBA identity flows.
- Public surface: [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-public/package.json).
- Distribution: source checkout; npm publication is separate.

## When to use it

Choose `@tba/ui-public` for this responsibility: Public UIX package for TBA identity flows. Its `105-ui` placement keeps browser-facing interface composition separate from establishing backend authorization or durable secret storage.

## Installation

Install `@tba/ui-public` from this checkout; registry publication is separate from this source-only workflow:

```bash
npm --prefix pkgs/105-ui/tba-ui-public install
```

Use the package's declared npm scripts from the repository root.

## Quick start

Use Node 22 or newer and run these commands from the repository root.

```bash
npm ci --no-audit --no-fund
npm run build -w @tba/ui-primitives
npm run build -w @tba/ui-public
```

Expect a Vite build with `dist/index.html` in this package.

## Usage

Use the checked-in `@tba/ui-public` package through its declared npm scripts:

```bash
npm --prefix pkgs/105-ui/tba-ui-public run dev
```

Public UIX package for TBA identity flows. The manifest is the authority for available scripts and entry points.

## Package Boundary

`@tba/ui-public` belongs to `105-ui` and owns browser-facing interface composition: Public UIX package for TBA identity flows.

Its implementation surface is the [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-public/package.json).

Keep establishing backend authorization or durable secret storage in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-public/package.json) for `@tba/ui-public` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`@tba/ui-public` exposes browser-facing interface composition. Inspect the [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-public/package.json) for the exported types and composition surface.

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `@tba/ui-public`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`@tba/ui-public` does not take ownership of establishing backend authorization or durable secret storage.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [@tba/ui-primitives](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/100-uix-core/tba-ui-primitives/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/105-ui/tba-ui-public)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-public/package.json)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-public/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-public/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

## Governance

`@tba/ui-public` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `105-ui` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

The build was checked using the [workspace lockfile](https://github.com/tigrbl/tigrbl_auth/blob/master/package-lock.json) and the [package build script](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-public/package.json). Live account or administration actions require a configured TBA backend.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)
