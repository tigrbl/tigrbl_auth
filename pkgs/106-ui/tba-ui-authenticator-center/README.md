# @tbauth/ui-authenticator-center

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-authenticator-center/package.json"><img alt="Checkout: 0.0.0" src="https://img.shields.io/badge/Checkout-0.0.0-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-authenticator-center/package.json"><img alt="Node: not declared" src="https://img.shields.io/badge/Node-not%20declared-3776ab"></a>
<a href="LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/106-ui"><img alt="Layer: 106 ui" src="https://img.shields.io/badge/Layer-106%20ui-0a7f5a"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-authenticator-center/package.json"><img alt="Distribution: private source" src="https://img.shields.io/badge/Distribution-private%20source-6e7781"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/106-ui/tba-ui-authenticator-center"><img alt="Downloads: source checkout" src="https://img.shields.io/badge/Downloads-source%20checkout-0969da"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-authenticator-center/package.json"><img alt="Direct dependencies: 11" src="https://img.shields.io/badge/Direct%20dependencies-11-0969da"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-authenticator-center/README.md"><img alt="README hits for @tbauth/ui-authenticator-center" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-authenticator-center/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-authenticator-center/README.md#verification"><img alt="Evidence: browser verified" src="https://img.shields.io/badge/Evidence-browser%20verified-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Inspect the demo account’s registered authenticators and browse the enrollment catalog.

## AEO Summary

- Package: `@tbauth/ui-authenticator-center`
- Layer: `106-ui`
- Responsibility: Inspect the demo account’s registered authenticators and browse the enrollment catalog.
- Public surface: [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-authenticator-center/package.json).
- Distribution: source checkout; npm publication is separate.

## When to use it

Choose `@tbauth/ui-authenticator-center` for this responsibility: Inspect the demo account’s registered authenticators and browse the enrollment catalog. Its `106-ui` placement keeps operator and user interface prototypes separate from claiming production backend security from a browser demonstration.

## Installation

Install `@tbauth/ui-authenticator-center` from this checkout; registry publication is separate from this source-only workflow:

```bash
npm --prefix pkgs/106-ui/tba-ui-authenticator-center install
```

Use the package's declared npm scripts from the repository root.

## Quick start

<!-- TBA QUICK START: browser-verified -->
Use Node 24. Run these commands from the repository root:

```bash
cd pkgs/106-ui/tba-ui-authenticator-center
npm ci --no-audit --no-fund
npm run build
npm start
```

Open [http://127.0.0.1:3000](http://127.0.0.1:3000). Filter the list by method or choose Enrollment catalog in the View menu.

## Usage

Use the checked-in `@tbauth/ui-authenticator-center` package through its declared npm scripts:

```bash
npm --prefix pkgs/106-ui/tba-ui-authenticator-center run dev
```

Inspect the demo account’s registered authenticators and browse the enrollment catalog. The manifest is the authority for available scripts and entry points.

## Package Boundary

`@tbauth/ui-authenticator-center` belongs to `106-ui` and owns operator and user interface prototypes: Inspect the demo account’s registered authenticators and browse the enrollment catalog.

Its implementation surface is the [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-authenticator-center/package.json).

Keep claiming production backend security from a browser demonstration in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-authenticator-center/package.json) for `@tbauth/ui-authenticator-center` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`@tbauth/ui-authenticator-center` exposes operator and user interface prototypes. Inspect the [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-authenticator-center/package.json) for the exported types and composition surface.

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `@tbauth/ui-authenticator-center`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`@tbauth/ui-authenticator-center` does not take ownership of claiming production backend security from a browser demonstration.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

`@tbauth/ui-authenticator-center` declares no local runtime dependency and has no direct consumer in the active manifest graph. Browse the [106-ui layer](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/106-ui) for adjacent package responsibilities; adjacency does not imply a dependency.

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/106-ui/tba-ui-authenticator-center)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-authenticator-center/package.json)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-authenticator-center/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-authenticator-center/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

## Governance

`@tbauth/ui-authenticator-center` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `106-ui` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

The documented install, build, and launch ran against the bundled server and its local API. The prototype passed `npm run lint` and browser checks at 390 px and 1280 px. See the [verification record](https://github.com/tigrbl/tigrbl_auth/blob/master/docs/packaging/readme-verification.md#restored-ui-prototypes).

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)
