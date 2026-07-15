# tigrbl-public-key-authentication-capability

Protocol-neutral orchestration for beginning and completing verified public-key assertions.

## Injected dependencies

Begin and completion callables backed by ceremony state, credential lookup, signature verification, and evidence handling.

## Operations and readiness

`begin_public_key_authentication` and `complete_public_key_authentication` are required; readiness is false until both are bound.

## Protocol consumers

WebAuthn and FIDO2 server profiles reuse these semantic operations.

## Non-goals

This package does not own browser, HTTP, CBOR, COSE, database, or session implementations.
