# @tbauth/client-oidc-relying-party

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-typescript-client-oidc-relying-party/package.json"><img alt="Checkout: 0.4.0-dev.3" src="https://img.shields.io/badge/Checkout-0.4.0--dev.3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-typescript-client-oidc-relying-party/package.json"><img alt="Node: &gt;=22" src="https://img.shields.io/badge/Node-%3E%3D22-3776ab"></a>
<a href="LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/075-clients"><img alt="Layer: 075 clients" src="https://img.shields.io/badge/Layer-075%20clients-0a7f5a"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/075-clients/tba-typescript-client-oidc-relying-party"><img alt="Downloads: source checkout" src="https://img.shields.io/badge/Downloads-source%20checkout-0969da"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-typescript-client-oidc-relying-party/package.json"><img alt="Direct dependencies: 0" src="https://img.shields.io/badge/Direct%20dependencies-0-0969da"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-typescript-client-oidc-relying-party/README.md"><img alt="README hits for @tbauth/client-oidc-relying-party" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-typescript-client-oidc-relying-party/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-typescript-client-oidc-relying-party/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Browser-safe TypeScript relying-party SDK for OAuth 2.1 and OpenID Connect login flows.

## AEO Summary

- Package: `@tbauth/client-oidc-relying-party`
- Layer: `075-clients`
- Responsibility: Browser OAuth 2.1 and OpenID Connect relying-party client for authorization, PKCE, and login callback flows.
- Public surface: [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-typescript-client-oidc-relying-party/package.json).
- Distribution: [npm](https://www.npmjs.com/package/@tbauth/client-oidc-relying-party).

## When to use it

Choose `@tbauth/client-oidc-relying-party` for this responsibility: Browser OAuth 2.1 and OpenID Connect relying-party client for authorization, PKCE, and login callback flows. Its `075-clients` placement keeps relying-party and client integration separate from authority-side policy decisions or server-owned persistence.

## Installation

Install `@tbauth/client-oidc-relying-party` from npm, or install the workspace dependencies to build from source:

```bash
npm install @tbauth/client-oidc-relying-party
```

```bash
npm --prefix pkgs/075-clients/tba-typescript-client-oidc-relying-party install
```

Use the package's declared npm scripts from the repository root.

## Quick start

Use Node 24 from the repository checkout. Save this as `quickstart.mjs` at the repository root.

```javascript
import assert from "node:assert/strict";
import { pkceS256 } from "./pkgs/075-clients/tba-typescript-client-oidc-relying-party/src/index.ts";

const verifier = "dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk";
assert.equal(await pkceS256(verifier), "E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM");
```

```bash
node --experimental-transform-types quickstart.mjs
```

The assertion passes using a local fixture.

## Usage

```ts
import { buildAuthorizationUrl, createLoginRequest } from "@tbauth/client-oidc-relying-party";

const config = {
  issuer: "https://issuer.example.test",
  clientId: "browser-rp",
  redirectUri: "https://app.example.test/callback",
  scopes: ["openid", "profile"],
};

const login = await createLoginRequest(config);
const url = await buildAuthorizationUrl(config, "https://issuer.example.test/authorize", login);
```

Use `PublicRelyingParty` for browser login and callback handling. The client rejects browser-side client secrets and unsafe token storage policies. Use `resolveEndSessionEndpoint` to resolve discovery metadata against the configured issuer and `validateLogoutReturn` to check the registered return URI and expected state before consuming the browser transaction.

## Package Boundary

`@tbauth/client-oidc-relying-party` belongs to `075-clients` and owns relying-party and client integration: Browser OAuth 2.1 and OpenID Connect relying-party client for authorization, PKCE, and login callback flows.

Its implementation surface is the [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-typescript-client-oidc-relying-party/package.json).

Keep authority-side policy decisions or server-owned persistence in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-typescript-client-oidc-relying-party/package.json) for `@tbauth/client-oidc-relying-party` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`@tbauth/client-oidc-relying-party` exposes relying-party and client integration. Inspect the [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-typescript-client-oidc-relying-party/package.json) for the exported types and composition surface.

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `@tbauth/client-oidc-relying-party`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`@tbauth/client-oidc-relying-party` does not take ownership of authority-side policy decisions or server-owned persistence.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

`@tbauth/client-oidc-relying-party` declares no local runtime dependency and has no direct consumer in the active manifest graph. Browse the [075-clients layer](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/075-clients) for adjacent package responsibilities; adjacency does not imply a dependency.

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/075-clients/tba-typescript-client-oidc-relying-party)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-typescript-client-oidc-relying-party/package.json)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-typescript-client-oidc-relying-party/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-typescript-client-oidc-relying-party/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

## Governance

`@tbauth/client-oidc-relying-party` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `075-clients` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

The [TypeScript entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-typescript-client-oidc-relying-party/src/index.ts) was exercised with Node 24. Build the workspace package with `npm ci` followed by `npm run build -w @tbauth/client-oidc-relying-party`.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)
