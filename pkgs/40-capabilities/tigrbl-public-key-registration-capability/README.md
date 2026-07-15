# tigrbl-public-key-registration-capability

Protocol-neutral orchestration for beginning and completing verified public-key credential registration.

## Injected dependencies

Begin and completion callables backed by durable ceremony operations, protocol verification, and credential insertion.

## Operations and readiness

`begin_public_key_registration` and `complete_public_key_registration` are required; readiness is false until both are bound.

## Protocol consumers

WebAuthn and versioned FIDO2 server profiles map their registration messages to these operations.

## Non-goals

This package owns neither WebAuthn wire parsing nor database tables, HTTP routes, keys, or trust anchors.
