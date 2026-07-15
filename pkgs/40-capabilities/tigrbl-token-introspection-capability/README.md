# tigrbl-token-introspection-capability

Layer-40 protocol-neutral orchestration for typed token-state introspection.

## Injected dependencies

A required synchronous or asynchronous lookup callable accepts a
`TokenIntrospectionRequest` and returns a typed result or normalized mapping.
It normally composes durable token state with profile validation below layer 40.

## Operations and readiness

The required operation is `introspect_token`. Construction fails without its
target and the capability report exposes the effective binding and state.

## Protocol consumers

The layer-50 OAuth package maps RFC 7662 to this capability; the layer-50
resource-server package may consume the normalized result for authorization.

## Non-goals

This package does not parse HTTP, authenticate callers, open sessions, verify
cryptography, choose protocol errors, or publish routes.
