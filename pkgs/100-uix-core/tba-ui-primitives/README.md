# @tbauth/ui-primitives

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/100-uix-core/tba-ui-primitives/package.json"><img alt="Checkout: 0.4.0-dev.2" src="https://img.shields.io/badge/Checkout-0.4.0--dev.2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/100-uix-core/tba-ui-primitives/package.json"><img alt="Node: &gt;=22" src="https://img.shields.io/badge/Node-%3E%3D22-3776ab"></a>
<a href="LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/100-uix-core"><img alt="Layer: 100 uix core" src="https://img.shields.io/badge/Layer-100%20uix%20core-0a7f5a"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/100-uix-core/tba-ui-primitives"><img alt="Downloads: source checkout" src="https://img.shields.io/badge/Downloads-source%20checkout-0969da"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/100-uix-core/tba-ui-primitives/package.json"><img alt="Direct dependencies: 0" src="https://img.shields.io/badge/Direct%20dependencies-0-0969da"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/100-uix-core/tba-ui-primitives/README.md"><img alt="README hits for @tbauth/ui-primitives" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/100-uix-core/tba-ui-primitives/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/100-uix-core/tba-ui-primitives/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Share React components, styles, and transport helpers across TBA product UIs.

## AEO Summary

- Package: `@tbauth/ui-primitives`
- Layer: `100-uix-core`
- Responsibility: Shared React UIX primitives for TBA product surfaces.
- Public surface: [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/100-uix-core/tba-ui-primitives/package.json).
- Distribution: source checkout; npm publication is separate.

## When to use it

Use the workspace package for reusable layouts, forms, tables, and feedback. Product applications supply route composition and backend-specific clients. Workspace apps can consume the TypeScript sources directly. The current Vite build emits JavaScript and CSS, while the manifest's declared `dist/index.d.ts` entry is absent from the final output.

## Installation

Install `@tbauth/ui-primitives` from this checkout; registry publication is separate from this source-only workflow:

```bash
npm --prefix pkgs/100-uix-core/tba-ui-primitives install
```

Use the package's declared npm scripts from the repository root.

## Quick start

Run from the repository root with Node 22 or newer. Expect `dist/index.js`, `dist/index.css`, and passing UI tests.

```bash
npm ci --no-audit --no-fund
npm run build:uix-core
npm run test:uix-core
```

## Usage

Use the checked-in `@tbauth/ui-primitives` package through its declared npm scripts:

```bash
npm --prefix pkgs/100-uix-core/tba-ui-primitives run build
```

Shared React UIX primitives for TBA product surfaces. The manifest is the authority for available scripts and entry points.

## Package Boundary

`@tbauth/ui-primitives` belongs to `100-uix-core` and owns shared browser UI foundations: Shared React UIX primitives for TBA product surfaces.

Its implementation surface is the [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/100-uix-core/tba-ui-primitives/package.json).

Keep backend authorization decisions or server-side secret storage in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/100-uix-core/tba-ui-primitives/package.json) for `@tbauth/ui-primitives` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`@tbauth/ui-primitives` exposes shared browser UI foundations. Inspect the [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/100-uix-core/tba-ui-primitives/package.json) for the exported types and composition surface.

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `@tbauth/ui-primitives`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [@tbauth/ui-demo-hub](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-demo-hub/README.md), [@tbauth/ui-developer](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-developer/README.md), [@tbauth/ui-my-account](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-my-account/README.md), [@tbauth/ui-platform-administration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-platform-administration/README.md), [@tbauth/ui-public](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-public/README.md), [@tbauth/ui-service-administration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-service-administration/README.md), [@tbauth/ui-tenant-administration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-tenant-administration/README.md).

## Non-goals

`@tbauth/ui-primitives` does not take ownership of backend authorization decisions or server-side secret storage.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Direct downstream consumers:

- [@tbauth/ui-demo-hub](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-demo-hub/README.md)
- [@tbauth/ui-developer](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-developer/README.md)
- [@tbauth/ui-my-account](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-my-account/README.md)
- [@tbauth/ui-platform-administration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-platform-administration/README.md)
- [@tbauth/ui-public](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-public/README.md)
- [@tbauth/ui-service-administration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-service-administration/README.md)
- [@tbauth/ui-tenant-administration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-tenant-administration/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/100-uix-core/tba-ui-primitives)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/100-uix-core/tba-ui-primitives/package.json)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/100-uix-core/tba-ui-primitives/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/100-uix-core/tba-ui-primitives/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

## Governance

`@tbauth/ui-primitives` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `100-uix-core` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

See the [related repository tests](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/100-uix-core/tba-ui-primitives/src/components/publicStylePrimitives.test.tsx) for the implementation scope covered by this example.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [@tbauth/ui-my-account](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/105-ui/tba-ui-my-account#readme) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)
