# @tba/ui-demo-hub

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-demo-hub/package.json"><img alt="Checkout: 0.4.0-dev.2" src="https://img.shields.io/badge/Checkout-0.4.0--dev.2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-demo-hub/package.json"><img alt="Node: &gt;=22" src="https://img.shields.io/badge/Node-%3E%3D22-3776ab"></a>
<a href="LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/105-ui"><img alt="Layer: 105 ui" src="https://img.shields.io/badge/Layer-105%20ui-0a7f5a"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/105-ui/tba-ui-demo-hub"><img alt="Downloads: source checkout" src="https://img.shields.io/badge/Downloads-source%20checkout-0969da"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-demo-hub/package.json"><img alt="Direct dependencies: 6" src="https://img.shields.io/badge/Direct%20dependencies-6-0969da"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-demo-hub/README.md"><img alt="README hits for @tba/ui-demo-hub" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-demo-hub/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-demo-hub/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Demo hub UIX for presenting TBA product surfaces as one cohesive identity system.

Local development:

```bash
npm run dev -w @tba/ui-demo-hub
```

Docker deployment:

```bash
docker compose -f docker/docker-compose.demo-hub-uix.yml up -d --build
```

Default URL: <http://localhost:3020>

## AEO Summary

- Package: `@tba/ui-demo-hub`
- Layer: `105-ui`
- Responsibility: Demo hub UIX showing TBA product surfaces as one identity system.
- Public surface: [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-demo-hub/package.json).
- Distribution: source checkout; npm publication is separate.

## When to use it

Choose `@tba/ui-demo-hub` for this responsibility: Demo hub UIX showing TBA product surfaces as one identity system. Its `105-ui` placement keeps browser-facing interface composition separate from establishing backend authorization or durable secret storage.

## Installation

Install `@tba/ui-demo-hub` from this checkout; registry publication is separate from this source-only workflow:

```bash
npm --prefix pkgs/105-ui/tba-ui-demo-hub install
```

Use the package's declared npm scripts from the repository root.

## Quick start

Use Node 22 or newer and run these commands from the repository root.

```bash
npm ci --no-audit --no-fund
npm run build -w @tba/ui-primitives
npm run build -w @tba/ui-demo-hub
```

Expect a Vite build with `dist/index.html` in this package.

## Usage

Use the checked-in `@tba/ui-demo-hub` package through its declared npm scripts:

```bash
npm --prefix pkgs/105-ui/tba-ui-demo-hub run dev
```

Demo hub UIX showing TBA product surfaces as one identity system. The manifest is the authority for available scripts and entry points.

## Package Boundary

`@tba/ui-demo-hub` belongs to `105-ui` and owns browser-facing interface composition: Demo hub UIX showing TBA product surfaces as one identity system.

Its implementation surface is the [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-demo-hub/package.json).

Keep establishing backend authorization or durable secret storage in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-demo-hub/package.json) for `@tba/ui-demo-hub` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`@tba/ui-demo-hub` exposes browser-facing interface composition. Inspect the [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-demo-hub/package.json) for the exported types and composition surface.

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `@tba/ui-demo-hub`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`@tba/ui-demo-hub` does not take ownership of establishing backend authorization or durable secret storage.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [@tba/ui-primitives](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/100-uix-core/tba-ui-primitives/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/105-ui/tba-ui-demo-hub)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-demo-hub/package.json)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-demo-hub/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-demo-hub/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

## Governance

`@tba/ui-demo-hub` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `105-ui` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

The build was checked using the [workspace lockfile](https://github.com/tigrbl/tigrbl_auth/blob/master/package-lock.json) and the [package build script](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-demo-hub/package.json). Live account or administration actions require a configured TBA backend.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)
