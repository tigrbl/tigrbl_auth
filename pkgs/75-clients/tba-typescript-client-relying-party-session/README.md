# @tba/client-relying-party-session

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/75-clients/tba-typescript-client-relying-party-session/package.json"><img alt="Checkout: 0.4.0-dev.3" src="https://img.shields.io/badge/Checkout-0.4.0--dev.3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/75-clients/tba-typescript-client-relying-party-session/package.json"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/75-clients"><img alt="Layer: 75 clients" src="https://img.shields.io/badge/Layer-75%20clients-0a7f5a"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/75-clients/tba-typescript-client-relying-party-session/package.json"><img alt="Direct dependencies: 0" src="https://img.shields.io/badge/Direct%20dependencies-0-0969da"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/75-clients/tba-typescript-client-relying-party-session/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Browser client for server-owned relying-party login, session lookup, and logout APIs.

## Quick start

Use Node 24 from the repository checkout. Save this as `quickstart.mjs` at the repository root.

```javascript
import assert from "node:assert/strict";
import { RelyingPartySessionClient } from "./pkgs/75-clients/tba-typescript-client-relying-party-session/src/index.ts";

const client = new RelyingPartySessionClient(async (url, options) => {
  assert.equal(url, "https://app.example/v1/rp/session");
  assert.equal(options.credentials, "include");
  return Response.json({ authenticated: true });
});
assert.equal((await client.current("https://app.example")).authenticated, true);
```

```bash
node --experimental-transform-types quickstart.mjs
```

The assertion passes using a local fixture.

## Verification

The [TypeScript entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/75-clients/tba-typescript-client-relying-party-session/src/index.ts) was exercised with Node 24.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)
