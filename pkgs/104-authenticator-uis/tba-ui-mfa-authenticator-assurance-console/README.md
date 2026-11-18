# @tba/ui-mfa-authenticator-assurance-console

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/104-authenticator-uis/tba-ui-mfa-authenticator-assurance-console/package.json"><img alt="Checkout: 0.0.0" src="https://img.shields.io/badge/Checkout-0.0.0-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/104-authenticator-uis/tba-ui-mfa-authenticator-assurance-console/package.json"><img alt="Node: not declared" src="https://img.shields.io/badge/Node-not%20declared-3776ab"></a>
<a href="LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/104-authenticator-uis"><img alt="Layer: 104 authenticator uis" src="https://img.shields.io/badge/Layer-104%20authenticator%20uis-0a7f5a"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/104-authenticator-uis/tba-ui-mfa-authenticator-assurance-console/package.json"><img alt="Distribution: private source" src="https://img.shields.io/badge/Distribution-private%20source-6e7781"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/104-authenticator-uis/tba-ui-mfa-authenticator-assurance-console"><img alt="Downloads: source checkout" src="https://img.shields.io/badge/Downloads-source%20checkout-0969da"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/104-authenticator-uis/tba-ui-mfa-authenticator-assurance-console/package.json"><img alt="Direct dependencies: 10" src="https://img.shields.io/badge/Direct%20dependencies-10-0969da"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/104-authenticator-uis/tba-ui-mfa-authenticator-assurance-console/README.md"><img alt="README hits for @tba/ui-mfa-authenticator-assurance-console" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/104-authenticator-uis/tba-ui-mfa-authenticator-assurance-console/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/104-authenticator-uis/tba-ui-mfa-authenticator-assurance-console/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Explore MFA factors, policy, user posture, and authenticator assurance in a private prototype.

## AEO Summary

- Package: `@tba/ui-mfa-authenticator-assurance-console`
- Layer: `104-authenticator-uis`
- Responsibility: Explore MFA factors, policy, user posture, and authenticator assurance in a private prototype.
- Public surface: [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/104-authenticator-uis/tba-ui-mfa-authenticator-assurance-console/package.json).
- Distribution: source checkout; npm publication is separate.

## When to use it

Use this console to review UI flows against seeded demo data. It is a standalone source prototype. The build runs locally without a backend or an API key.

## Installation

Install `@tba/ui-mfa-authenticator-assurance-console` from this checkout; registry publication is separate from this source-only workflow:

```bash
npm --prefix pkgs/104-authenticator-uis/tba-ui-mfa-authenticator-assurance-console install
```

Use the package's declared npm scripts from the repository root.

## Quick start

Run from the repository root with Node 22 or newer. A successful build produces `dist/index.html` and bundled assets. Use `npm run preview` to inspect the build locally.

```bash
cd pkgs/104-authenticator-uis/tba-ui-mfa-authenticator-assurance-console
npm install --no-package-lock --no-audit --no-fund
npm run build
```

## Usage

Use the checked-in `@tba/ui-mfa-authenticator-assurance-console` package through its declared npm scripts:

```bash
npm --prefix pkgs/104-authenticator-uis/tba-ui-mfa-authenticator-assurance-console run dev
```

Explore MFA factors, policy, user posture, and authenticator assurance in a private prototype. The manifest is the authority for available scripts and entry points.

## Package Boundary

`@tba/ui-mfa-authenticator-assurance-console` belongs to `104-authenticator-uis` and owns authenticator-facing UI integration: Explore MFA factors, policy, user posture, and authenticator assurance in a private prototype.

Its implementation surface is the [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/104-authenticator-uis/tba-ui-mfa-authenticator-assurance-console/package.json).

Keep replacing server-side verification and authorization in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/104-authenticator-uis/tba-ui-mfa-authenticator-assurance-console/package.json) for `@tba/ui-mfa-authenticator-assurance-console` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`@tba/ui-mfa-authenticator-assurance-console` exposes authenticator-facing UI integration. Inspect the [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/104-authenticator-uis/tba-ui-mfa-authenticator-assurance-console/package.json) for the exported types and composition surface.

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `@tba/ui-mfa-authenticator-assurance-console`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`@tba/ui-mfa-authenticator-assurance-console` does not take ownership of replacing server-side verification and authorization.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

`@tba/ui-mfa-authenticator-assurance-console` declares no local runtime dependency and has no direct consumer in the active manifest graph. Browse the [104-authenticator-uis layer](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/104-authenticator-uis) for adjacent package responsibilities; adjacency does not imply a dependency.

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/104-authenticator-uis/tba-ui-mfa-authenticator-assurance-console)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/104-authenticator-uis/tba-ui-mfa-authenticator-assurance-console/package.json)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/104-authenticator-uis/tba-ui-mfa-authenticator-assurance-console/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/104-authenticator-uis/tba-ui-mfa-authenticator-assurance-console/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

## Governance

`@tba/ui-mfa-authenticator-assurance-console` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `104-authenticator-uis` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

See the [declared build command](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/104-authenticator-uis/tba-ui-mfa-authenticator-assurance-console/package.json) for the implementation scope covered by this example.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [tba-bases-authenticator](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/05-bases/tba-bases-authenticator#readme) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)
