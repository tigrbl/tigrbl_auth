# tigrbl-policy-assurance-capability

Authorization correctness, isolation, determinism, attenuation, liveness, and residency assurance.

## Injected dependencies

- `tigrbl-authorization-policy-durability`

## Operations and readiness

- `evaluate`
- `report`

## Protocol consumers

- Protocol-neutral; layer-50 packages may bind these operations.

## Non-goals

- No HTTP or protocol wire schemas.
- No direct layer-01 table access.
- No hidden mutable persistence or provider selection.
