# @tba/client-oidc-relying-party

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/75-clients/tba-typescript-client-oidc-relying-party/package.json"><img alt="Checkout: 0.4.0-dev.2" src="https://img.shields.io/badge/Checkout-0.4.0--dev.2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/75-clients/tba-typescript-client-oidc-relying-party/package.json"><img alt="Node: &gt;=22" src="https://img.shields.io/badge/Node-%3E%3D22-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/75-clients/tba-typescript-client-oidc-relying-party/package.json"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/75-clients"><img alt="Layer: 75 clients" src="https://img.shields.io/badge/Layer-75%20clients-0a7f5a"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/75-clients/tba-typescript-client-oidc-relying-party/package.json"><img alt="Direct dependencies: 0" src="https://img.shields.io/badge/Direct%20dependencies-0-0969da"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/75-clients/tba-typescript-client-oidc-relying-party/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Browser-safe TypeScript relying-party SDK for OAuth 2.1 and OpenID Connect login flows.



## Quick start

Use Node 24 from the repository checkout. Save this as `quickstart.mjs` at the repository root.

```javascript
import assert from "node:assert/strict";
import { pkceS256 } from "./pkgs/75-clients/tba-typescript-client-oidc-relying-party/src/index.ts";

const verifier = "dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk";
assert.equal(await pkceS256(verifier), "E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM");
```

```bash
node --experimental-transform-types quickstart.mjs
```

The assertion passes using a local fixture.

## Usage

```ts
import { buildAuthorizationUrl, createLoginRequest } from "@tba/client-oidc-relying-party";

const config = {
  issuer: "https://issuer.example.test",
  clientId: "browser-rp",
  redirectUri: "https://app.example.test/callback",
  scopes: ["openid", "profile"],
};

const login = await createLoginRequest(config);
const url = await buildAuthorizationUrl(config, "https://issuer.example.test/authorize", login);
```

The package rejects browser-side client secrets and unsafe token storage policies.

## Verification

The [TypeScript entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/75-clients/tba-typescript-client-oidc-relying-party/src/index.ts) was exercised with Node 24. Build the workspace package with `npm ci` followed by `npm run build -w @tba/client-oidc-relying-party`.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)
