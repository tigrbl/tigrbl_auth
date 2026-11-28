# @tbauth/client-platform-administration

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-typescript-client-platform-administration/package.json"><img alt="Checkout: 0.4.0-dev.3" src="https://img.shields.io/badge/Checkout-0.4.0--dev.3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-typescript-client-platform-administration/package.json"><img alt="Node: not declared" src="https://img.shields.io/badge/Node-not%20declared-3776ab"></a>
<a href="LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/075-clients"><img alt="Layer: 075 clients" src="https://img.shields.io/badge/Layer-075%20clients-0a7f5a"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/075-clients/tba-typescript-client-platform-administration"><img alt="Downloads: source checkout" src="https://img.shields.io/badge/Downloads-source%20checkout-0969da"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-typescript-client-platform-administration/package.json"><img alt="Direct dependencies: 0" src="https://img.shields.io/badge/Direct%20dependencies-0-0969da"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-typescript-client-platform-administration/README.md"><img alt="README hits for @tbauth/client-platform-administration" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-typescript-client-platform-administration/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-typescript-client-platform-administration/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Transport-injected TypeScript client for platform policy administration, decision audit, and identity-provider clients.

## AEO Summary

- Package: `@tbauth/client-platform-administration`
- Layer: `075-clients`
- Responsibility: Transport-injected TypeScript client for platform policy administration, decision audit, and identity-provider clients.
- Public surface: [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-typescript-client-platform-administration/package.json).
- Distribution: source checkout; npm publication is separate.

## When to use it

Choose `@tbauth/client-platform-administration` for this responsibility: Transport-injected TypeScript client for platform policy administration, decision audit, and identity-provider clients. Its `075-clients` placement keeps relying-party and client integration separate from authority-side policy decisions or server-owned persistence.

## Installation

Install `@tbauth/client-platform-administration` from this checkout; registry publication is separate from this source-only workflow:

```bash
npm --prefix pkgs/075-clients/tba-typescript-client-platform-administration install
```

Use the package's declared npm scripts from the repository root.

## Quick start

Use Node 24 from the repository checkout. Save this as `quickstart.mjs` at the repository root.

```javascript
import assert from "node:assert/strict";
import { PlatformAdminClient } from "./pkgs/075-clients/tba-typescript-client-platform-administration/src/index.ts";

const client = new PlatformAdminClient(async (method, path) => ({ method, path }));
assert.deepEqual(await client.listPolicies(), {
  method: "GET",
  path: "/v1/platform/authorization/policies",
});
```

```bash
node --experimental-transform-types quickstart.mjs
```

The assertion passes using a local fixture.

## Usage

Use the checked-in `@tbauth/client-platform-administration` package through its declared npm scripts:

```bash
npm --prefix pkgs/075-clients/tba-typescript-client-platform-administration run
```

Transport-injected TypeScript client for platform policy administration, decision audit, and identity-provider clients. The manifest is the authority for available scripts and entry points.

## Package Boundary

`@tbauth/client-platform-administration` belongs to `075-clients` and owns relying-party and client integration: Transport-injected TypeScript client for platform policy administration, decision audit, and identity-provider clients.

Its implementation surface is the [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-typescript-client-platform-administration/package.json).

Keep authority-side policy decisions or server-owned persistence in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-typescript-client-platform-administration/package.json) for `@tbauth/client-platform-administration` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`@tbauth/client-platform-administration` exposes relying-party and client integration. Inspect the [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-typescript-client-platform-administration/package.json) for the exported types and composition surface.

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `@tbauth/client-platform-administration`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [@tbauth/ui-platform-administration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-platform-administration/README.md).

## Non-goals

`@tbauth/client-platform-administration` does not take ownership of authority-side policy decisions or server-owned persistence.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Direct downstream consumers:

- [@tbauth/ui-platform-administration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-platform-administration/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/075-clients/tba-typescript-client-platform-administration)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-typescript-client-platform-administration/package.json)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-typescript-client-platform-administration/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-typescript-client-platform-administration/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

## Governance

`@tbauth/client-platform-administration` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `075-clients` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

The [TypeScript entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-typescript-client-platform-administration/src/index.ts) was exercised with Node 24.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)
