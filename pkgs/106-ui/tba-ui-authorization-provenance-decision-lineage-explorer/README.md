# @tbauth/ui-authorization-provenance-decision-lineage-explorer

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-authorization-provenance-decision-lineage-explorer/package.json"><img alt="Checkout: 0.0.0" src="https://img.shields.io/badge/Checkout-0.0.0-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-authorization-provenance-decision-lineage-explorer/package.json"><img alt="Node: not declared" src="https://img.shields.io/badge/Node-not%20declared-3776ab"></a>
<a href="LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/106-ui"><img alt="Layer: 106 ui" src="https://img.shields.io/badge/Layer-106%20ui-0a7f5a"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-authorization-provenance-decision-lineage-explorer/package.json"><img alt="Distribution: private source" src="https://img.shields.io/badge/Distribution-private%20source-6e7781"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/106-ui/tba-ui-authorization-provenance-decision-lineage-explorer"><img alt="Downloads: source checkout" src="https://img.shields.io/badge/Downloads-source%20checkout-0969da"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-authorization-provenance-decision-lineage-explorer/package.json"><img alt="Direct dependencies: 10" src="https://img.shields.io/badge/Direct%20dependencies-10-0969da"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-authorization-provenance-decision-lineage-explorer/README.md"><img alt="README hits for @tbauth/ui-authorization-provenance-decision-lineage-explorer" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-authorization-provenance-decision-lineage-explorer/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-authorization-provenance-decision-lineage-explorer/README.md#verification"><img alt="Evidence: browser verified" src="https://img.shields.io/badge/Evidence-browser%20verified-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Explore seeded decision records and replay a sample trace against a deterministic demo policy.

## AEO Summary

- Package: `@tbauth/ui-authorization-provenance-decision-lineage-explorer`
- Layer: `106-ui`
- Responsibility: Explore seeded decision records and replay a sample trace against a deterministic demo policy.
- Public surface: [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-authorization-provenance-decision-lineage-explorer/package.json).
- Distribution: source checkout; npm publication is separate.

## When to use it

Choose `@tbauth/ui-authorization-provenance-decision-lineage-explorer` for this responsibility: Explore seeded decision records and replay a sample trace against a deterministic demo policy. Its `106-ui` placement keeps operator and user interface prototypes separate from claiming production backend security from a browser demonstration.

## Installation

Install `@tbauth/ui-authorization-provenance-decision-lineage-explorer` from this checkout; registry publication is separate from this source-only workflow:

```bash
npm --prefix pkgs/106-ui/tba-ui-authorization-provenance-decision-lineage-explorer install
```

Use the package's declared npm scripts from the repository root.

## Quick start

<!-- TBA QUICK START: browser-verified -->
Use Node 24. Run these commands from the repository root:

```bash
cd pkgs/106-ui/tba-ui-authorization-provenance-decision-lineage-explorer
npm install --no-package-lock --no-audit --no-fund
npm run build
npm start
```

Open [http://127.0.0.1:3000](http://127.0.0.1:3000). Click **Replay latest decision** to compare the outcomes. Choose Replays in the View menu to see the completed job.

## Usage

Use the checked-in `@tbauth/ui-authorization-provenance-decision-lineage-explorer` package through its declared npm scripts:

```bash
npm --prefix pkgs/106-ui/tba-ui-authorization-provenance-decision-lineage-explorer run dev
```

Explore seeded decision records and replay a sample trace against a deterministic demo policy. The manifest is the authority for available scripts and entry points.

## Package Boundary

`@tbauth/ui-authorization-provenance-decision-lineage-explorer` belongs to `106-ui` and owns operator and user interface prototypes: Explore seeded decision records and replay a sample trace against a deterministic demo policy.

Its implementation surface is the [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-authorization-provenance-decision-lineage-explorer/package.json).

Keep claiming production backend security from a browser demonstration in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-authorization-provenance-decision-lineage-explorer/package.json) for `@tbauth/ui-authorization-provenance-decision-lineage-explorer` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`@tbauth/ui-authorization-provenance-decision-lineage-explorer` exposes operator and user interface prototypes. Inspect the [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-authorization-provenance-decision-lineage-explorer/package.json) for the exported types and composition surface.

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `@tbauth/ui-authorization-provenance-decision-lineage-explorer`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`@tbauth/ui-authorization-provenance-decision-lineage-explorer` does not take ownership of claiming production backend security from a browser demonstration.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

`@tbauth/ui-authorization-provenance-decision-lineage-explorer` declares no local runtime dependency and has no direct consumer in the active manifest graph. Browse the [106-ui layer](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/106-ui) for adjacent package responsibilities; adjacency does not imply a dependency.

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/106-ui/tba-ui-authorization-provenance-decision-lineage-explorer)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-authorization-provenance-decision-lineage-explorer/package.json)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-authorization-provenance-decision-lineage-explorer/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-authorization-provenance-decision-lineage-explorer/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

## Governance

`@tbauth/ui-authorization-provenance-decision-lineage-explorer` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `106-ui` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

The documented install, build, and launch ran against the bundled server and its local API. The prototype passed `npm run lint` and browser checks at 390 px and 1280 px. See the [verification record](https://github.com/tigrbl/tigrbl_auth/blob/master/docs/packaging/readme-verification.md#restored-ui-prototypes).

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)
