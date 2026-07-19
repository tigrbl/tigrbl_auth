# tigrbl-protected-envelope-capability

Independently mountable, carrier-neutral capability. Layer 50 maps its operations into versioned protocols.

## Injected dependencies

- No package-mandated runtime dependency; callables are constructor-injected.

## Operations and readiness

- `protect_envelope`
- `verify_envelope`

## Protocol consumers

- Protocol-neutral; layer-50 packages may bind these operations.

## Non-goals

- No HTTP or protocol wire schemas.
- No direct layer-01 table access.
- No hidden mutable persistence or provider selection.
