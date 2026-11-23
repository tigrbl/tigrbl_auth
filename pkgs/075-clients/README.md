# API clients

Layer 75 contains Python and TypeScript clients that call APIs or injected
transports. It does not contain ASGI middleware or router implementations.

Python packages:

- `tba-client-authorization-administration`
- `tba-client-policy-decision`
- `tba-client-relying-party-session`

TypeScript packages:

- `@tba/client-oidc-relying-party`
- `@tba/client-relying-party-session`
- `@tba/client-policy-decision`
- `@tba/client-platform-administration`
- `@tba/client-tenant-administration`

ASGI policy enforcement lives in layer 85. Backend applications in layer 90
compose clients, middleware, and routers.
