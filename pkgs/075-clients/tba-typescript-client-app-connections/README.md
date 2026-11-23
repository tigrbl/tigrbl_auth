# @tbauth/client-app-connections

Manage app consent and connected applications from a signed-in account using a
shared TypeScript client and the API contract of the host application.

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-typescript-client-app-connections/package.json"><img alt="Checkout: 0.4.0-dev.1" src="https://img.shields.io/badge/Checkout-0.4.0--dev.1-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-typescript-client-app-connections/package.json"><img alt="Node: &gt;=22" src="https://img.shields.io/badge/Node-%3E%3D22-3776ab"></a>
<a href="LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/075-clients"><img alt="Layer: 075 clients" src="https://img.shields.io/badge/Layer-075%20clients-0a7f5a"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/075-clients/tba-typescript-client-app-connections"><img alt="Downloads: source checkout" src="https://img.shields.io/badge/Downloads-source%20checkout-0969da"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-typescript-client-app-connections/package.json"><img alt="Direct dependencies: 0" src="https://img.shields.io/badge/Direct%20dependencies-0-0969da"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-typescript-client-app-connections/README.md"><img alt="README hits for @tbauth/client-app-connections" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-typescript-client-app-connections/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-typescript-client-app-connections/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

## AEO Summary

The client loads consent, submits an approval or denial, lists connections, and
revokes a connection. It provides shared types for permissions and identities.

## When to use it

Use it in the signed-in application that displays consent and connected apps.
Supply an API adapter for the application’s current request and response shapes.

## Installation

Build the workspace package from the repository root.

```sh
npm ci
npm run build -w @tbauth/client-app-connections
```

## Quick start

Pass the application's consent protocol and request transport into the client.
The request can be an opaque request ID or validated query fields.

```ts
import { createAppConnectionsClient } from "@tbauth/client-app-connections";
import { protocol, transport } from "./app-connections-api.js";

const client = createAppConnectionsClient(protocol, transport);
const consent = await client.getConsent("request-id");
```

## Usage

If the API returns JSON, use the provided transport. The application supplies
headers through its existing session integration when required.

```ts
import { createJsonAppConnectionsTransport } from "@tbauth/client-app-connections";

const transport = createJsonAppConnectionsTransport({
  baseUrl: "/forum-api",
  credentials: "same-origin",
});
```

The protocol maps each operation to a path and response reader. The consent
decision mapping also emits the request body. Define product-specific fields
such as bot categories or connection expiry in those mappings.

## Package Boundary

The client coordinates authenticated browser requests and returns mapped
results. The host handles session credentials, application-specific response
validation, and registered callback validation before navigation.

## Injected dependencies

Inject the API mapping and transport using `createAppConnectionsClient`. The
JSON transport accepts an optional fetch implementation and headers provider.

## Operations and readiness

Pass a request signal to cancel stale reads. Handle `AppConnectionsHttpError`
using its status and provider message. Confirm the mounted routes against the
host before adopting a release.

## Protocol consumers

The Techmod Journal and UNUI Forum contracts are represented in the package
tests. They use opaque consent identifiers and OAuth query fields, respectively.

## Non-goals

The external MCP host owns its OAuth client flow. The authorization server owns
grant policy, token lifecycle, and the final permission decision.

## Related Packages

`@tbauth/ui-app-connections` provides React controls for the same permission and
acting-identity data.

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/075-clients/tba-typescript-client-app-connections)
- [License](LICENSE) and [notice](NOTICE)

## Governance

Use contract fixtures from both host APIs when changing the client. Keep the
server routes and product configuration in the appropriate application.

## Verification

The tests cover both API shapes, permit and deny decisions, list and revoke,
and the response-error contract.

```sh
npm run test -w @tbauth/client-app-connections
```
