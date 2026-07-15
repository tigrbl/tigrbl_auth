# tigrbl-client-registration-capability

Layer-40 orchestration for the protocol-neutral lifecycle of a registered
client.

## Injected dependencies

Create, read, update, and disable callables are required and normally adapt
layer-30 table operations. A durable audit callable is optional. Every
collaborator may be synchronous or asynchronous.

## Operations and readiness

Operations are `register_client`, `get_registration`, `update_registration`,
`disable_registration`, and optional `record_audit_event`. Readiness is true
only when all four lifecycle targets are bound; the report separately exposes
whether audit recording is available.

## Protocol consumers

The layer-50 OAuth package maps RFC 7591/7592 behavior to this capability; OIDC
uses that OAuth registration mapping where enabled.

## Non-goals

This package does not parse HTTP, generate/hash secrets, validate OAuth
metadata, select protocol errors, open storage sessions, or own registration
state.
