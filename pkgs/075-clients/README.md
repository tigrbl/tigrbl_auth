# API clients

Layer 75 contains Python and TypeScript clients that call APIs or injected
transports. It does not contain ASGI middleware or router implementations.

Python packages:

- `tba-client-authorization-administration`
- `tba-client-policy-decision`
- `tba-client-relying-party-session`

TypeScript packages:

- `@tbauth/client-oidc-relying-party`
- `@tbauth/client-relying-party-session`
- `@tbauth/client-policy-decision`
- `@tbauth/client-platform-administration`
- `@tbauth/client-tenant-administration`

ASGI policy enforcement lives in layer 85. Backend applications in layer 90
compose clients, middleware, and routers.
