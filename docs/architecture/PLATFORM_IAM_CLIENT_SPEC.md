# Layer 75 client contract

## Normative requirements

`75-clients` owns typed remote SDKs and consumer-side enforcement adapters.
Client packages may depend on layer-02 contracts, layer-50 protocol wire models,
and external transport libraries. They must not depend on storage, capabilities,
runtime composition, routers, backend applications, facades, or UI packages.
Server packages must not depend on client packages.

Python packages are `tba-client-authorization-admin`,
`tba-client-policy-decision`, `tba-client-relying-party-session`, and
`tba-middleware-policy-enforcement-asgi`. TypeScript packages are
`@tba/client-oidc-relying-party`, `@tba/client-relying-party-session`,
`@tba/client-tenant-admin`, `@tba/client-platform-admin`, and
`@tba/client-policy-decision`.

Clients provide typed errors, timeouts and cancellation, correlation propagation,
CSRF support for cookie-authenticated mutations, revision and idempotency headers,
and conservative retry rules. Browser clients never persist bearer or refresh
tokens in local storage. UIX packages consume clients but do not redefine their
wire contracts.

The existing `@tba/client-oidc-relying-party` package moves from layer 105 to layer 75 without a
published-name change. Compatibility is verified through build, import, shared
vector, and workspace-layer tests.
