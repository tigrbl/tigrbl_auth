# tigrbl-grant-negotiation-capability

Layer-40 protocol-neutral composition for requesting, continuing, and rotating
negotiated grants.

## Injected dependencies

A grant-request target is required. Continuation and access-token rotation
targets are optional. Layer-60 composition may build these targets from
layer-20 key/token providers and the layer-30 GNAP grant-state operations.

## Operations and readiness

`request_grant` is required. `continue_grant` and `rotate_access_token` are
optional and report unavailable when unbound. Readiness follows the required
request target; no grant or token state is retained in this package.

## Protocol consumers

The layer-50 GNAP package maps RFC 9635 grant request, continuation, and token
rotation semantics to these operations. Other grant-negotiation protocols may
reuse the normalized contracts through their own mappings.

## Non-goals

This package does not parse GNAP messages, validate key proofs, mint tokens,
generate continuation secrets, open database sessions, or mount routes.
