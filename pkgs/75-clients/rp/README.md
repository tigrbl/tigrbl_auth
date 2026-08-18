# @tigrbl-auth/rp

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

Browser-safe TypeScript relying-party SDK for OAuth 2.1 and OpenID Connect login flows.

## Install

```bash
npm install @tigrbl-auth/rp
```

## Usage

```ts
import { buildAuthorizationUrl, createLoginRequest } from "@tigrbl-auth/rp";

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
