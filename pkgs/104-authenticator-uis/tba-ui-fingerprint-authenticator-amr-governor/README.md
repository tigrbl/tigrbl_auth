# @tbauth/ui-fingerprint-authenticator-amr-governor

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/104-authenticator-uis/tba-ui-fingerprint-authenticator-amr-governor/package.json"><img alt="Checkout: 0.0.0" src="https://img.shields.io/badge/Checkout-0.0.0-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/104-authenticator-uis/tba-ui-fingerprint-authenticator-amr-governor/package.json"><img alt="Node: not declared" src="https://img.shields.io/badge/Node-not%20declared-3776ab"></a>
<a href="LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/104-authenticator-uis"><img alt="Layer: 104 authenticator uis" src="https://img.shields.io/badge/Layer-104%20authenticator%20uis-0a7f5a"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/104-authenticator-uis/tba-ui-fingerprint-authenticator-amr-governor/package.json"><img alt="Distribution: private source" src="https://img.shields.io/badge/Distribution-private%20source-6e7781"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/104-authenticator-uis/tba-ui-fingerprint-authenticator-amr-governor"><img alt="Downloads: source checkout" src="https://img.shields.io/badge/Downloads-source%20checkout-0969da"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/104-authenticator-uis/tba-ui-fingerprint-authenticator-amr-governor/package.json"><img alt="Direct dependencies: 10" src="https://img.shields.io/badge/Direct%20dependencies-10-0969da"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/104-authenticator-uis/tba-ui-fingerprint-authenticator-amr-governor/README.md"><img alt="README hits for @tbauth/ui-fingerprint-authenticator-amr-governor" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/104-authenticator-uis/tba-ui-fingerprint-authenticator-amr-governor/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/104-authenticator-uis/tba-ui-fingerprint-authenticator-amr-governor/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Source prototype for Fingerprint AMR Governor.

## AEO Summary

- Package: `@tbauth/ui-fingerprint-authenticator-amr-governor`
- Layer: `104-authenticator-uis`
- Responsibility: Source prototype for Fingerprint AMR Governor.
- Public surface: [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/104-authenticator-uis/tba-ui-fingerprint-authenticator-amr-governor/package.json).
- Distribution: source checkout; npm publication is separate.

## When to use it

Choose `@tbauth/ui-fingerprint-authenticator-amr-governor` for this responsibility: Source prototype for Fingerprint AMR Governor. Its `104-authenticator-uis` placement keeps authenticator-facing UI integration separate from replacing server-side verification and authorization.

## Installation

Install `@tbauth/ui-fingerprint-authenticator-amr-governor` from this checkout; registry publication is separate from this source-only workflow:

```bash
npm --prefix pkgs/104-authenticator-uis/tba-ui-fingerprint-authenticator-amr-governor install
```

Use the package's declared npm scripts from the repository root.

## Quick start

Use Node 22 or newer and run these commands from the repository root.

```bash
cd pkgs/104-authenticator-uis/tba-ui-fingerprint-authenticator-amr-governor
npm install --no-package-lock --no-audit --no-fund
npm run build
```

Expect `dist/index.html` and bundled assets.

## Usage

Use the checked-in `@tbauth/ui-fingerprint-authenticator-amr-governor` package through its declared npm scripts:

```bash
npm --prefix pkgs/104-authenticator-uis/tba-ui-fingerprint-authenticator-amr-governor run dev
```

Source prototype for Fingerprint AMR Governor. The manifest is the authority for available scripts and entry points.

## Package Boundary

`@tbauth/ui-fingerprint-authenticator-amr-governor` belongs to `104-authenticator-uis` and owns authenticator-facing UI integration: Source prototype for Fingerprint AMR Governor.

Its implementation surface is the [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/104-authenticator-uis/tba-ui-fingerprint-authenticator-amr-governor/package.json).

Keep replacing server-side verification and authorization in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/104-authenticator-uis/tba-ui-fingerprint-authenticator-amr-governor/package.json) for `@tbauth/ui-fingerprint-authenticator-amr-governor` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`@tbauth/ui-fingerprint-authenticator-amr-governor` exposes authenticator-facing UI integration. Inspect the [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/104-authenticator-uis/tba-ui-fingerprint-authenticator-amr-governor/package.json) for the exported types and composition surface.

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `@tbauth/ui-fingerprint-authenticator-amr-governor`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`@tbauth/ui-fingerprint-authenticator-amr-governor` does not take ownership of replacing server-side verification and authorization.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

`@tbauth/ui-fingerprint-authenticator-amr-governor` declares no local runtime dependency and has no direct consumer in the active manifest graph. Browse the [104-authenticator-uis layer](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/104-authenticator-uis) for adjacent package responsibilities; adjacency does not imply a dependency.

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/104-authenticator-uis/tba-ui-fingerprint-authenticator-amr-governor)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/104-authenticator-uis/tba-ui-fingerprint-authenticator-amr-governor/package.json)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/104-authenticator-uis/tba-ui-fingerprint-authenticator-amr-governor/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/104-authenticator-uis/tba-ui-fingerprint-authenticator-amr-governor/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

## Governance

`@tbauth/ui-fingerprint-authenticator-amr-governor` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `104-authenticator-uis` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

The [build command](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/104-authenticator-uis/tba-ui-fingerprint-authenticator-amr-governor/package.json) completed in an isolated source checkout using Node 24. The check covers bundling.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)
