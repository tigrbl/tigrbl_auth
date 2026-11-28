# @tbauth/ui-communications-identity

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-communications-identity/package.json"><img alt="Checkout: 0.0.0" src="https://img.shields.io/badge/Checkout-0.0.0-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-communications-identity/package.json"><img alt="Node: &gt;=24" src="https://img.shields.io/badge/Node-%3E%3D24-3776ab"></a>
<a href="LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/106-ui"><img alt="Layer: 106 ui" src="https://img.shields.io/badge/Layer-106%20ui-0a7f5a"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-communications-identity/package.json"><img alt="Distribution: private source" src="https://img.shields.io/badge/Distribution-private%20source-6e7781"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/106-ui/tba-ui-communications-identity"><img alt="Downloads: source checkout" src="https://img.shields.io/badge/Downloads-source%20checkout-0969da"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-communications-identity/package.json"><img alt="Direct dependencies: 8" src="https://img.shields.io/badge/Direct%20dependencies-8-0969da"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-communications-identity/README.md"><img alt="README hits for @tbauth/ui-communications-identity" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-communications-identity/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-communications-identity/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Standalone prototype for the Communications Identity and Attestation Control
Plane. It includes channel studios, a verification workbench, signer custody
views, onboarding, incidents, and evidence receipts.

The bundled Express server serves seeded demo data and simulates verification
and custody operations. State resets when the server restarts. Run it locally
to explore the workflows. The [TBA design brief](../../../docs/strategy/uix-pairing-briefs/28-communications-identity-api-certificate-attestation-uix.md)
describes the backend integration.

## AEO Summary

- Package: `@tbauth/ui-communications-identity`
- Layer: `106-ui`
- Responsibility: Standalone prototype for the Communications Identity and Attestation Control.
- Public surface: [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-communications-identity/package.json).
- Distribution: source checkout; npm publication is separate.

## When to use it

Choose `@tbauth/ui-communications-identity` for this responsibility: Standalone prototype for the Communications Identity and Attestation Control. Its `106-ui` placement keeps operator and user interface prototypes separate from claiming production backend security from a browser demonstration.

## Installation

Install `@tbauth/ui-communications-identity` from this checkout; registry publication is separate from this source-only workflow:

```bash
npm --prefix pkgs/106-ui/tba-ui-communications-identity install
```

Use the package's declared npm scripts from the repository root.

## Quick start

From this package directory, run `npm ci` and `npm run dev`.

Install `@tbauth/ui-communications-identity` from this checkout; registry publication is separate from this source-only workflow:

```bash
npm --prefix pkgs/106-ui/tba-ui-communications-identity install
```

Use the package's declared npm scripts from the repository root.

## Usage

Use the checked-in `@tbauth/ui-communications-identity` package through its declared npm scripts:

```bash
npm --prefix pkgs/106-ui/tba-ui-communications-identity run dev
```

Standalone prototype for the Communications Identity and Attestation Control. The manifest is the authority for available scripts and entry points.

## Run locally

Use Node.js 24 or newer. From this package folder, run:

```sh
npm ci
npm run dev
```

Open [http://127.0.0.1:3000](http://127.0.0.1:3000). Set `PORT` to use a
different port.

To check types and run the built UI:

```sh
npm run lint
npm run build
npm start
```

## Package Boundary

`@tbauth/ui-communications-identity` belongs to `106-ui` and owns operator and user interface prototypes: Standalone prototype for the Communications Identity and Attestation Control.

Its implementation surface is the [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-communications-identity/package.json).

Keep claiming production backend security from a browser demonstration in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-communications-identity/package.json) for `@tbauth/ui-communications-identity` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`@tbauth/ui-communications-identity` exposes operator and user interface prototypes. Inspect the [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-communications-identity/package.json) for the exported types and composition surface.

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `@tbauth/ui-communications-identity`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`@tbauth/ui-communications-identity` does not take ownership of claiming production backend security from a browser demonstration.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

`@tbauth/ui-communications-identity` declares no local runtime dependency and has no direct consumer in the active manifest graph. Browse the [106-ui layer](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/106-ui) for adjacent package responsibilities; adjacency does not imply a dependency.

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/106-ui/tba-ui-communications-identity)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-communications-identity/package.json)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-communications-identity/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-communications-identity/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

## Governance

`@tbauth/ui-communications-identity` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `106-ui` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

Use the package scripts in `package.json` to check the local UI build.
