# tigrbl-mfa-challenge-capability

Coordinates begin and complete operations for a multi-factor challenge ceremony.

## Injected dependencies

- No package-mandated runtime dependency; callables are constructor-injected.

## Operations and readiness

- `begin_mfa_challenge`
- `complete_mfa_challenge`

## Protocol consumers

- Protocol-neutral; layer-50 packages may bind these operations.

## Non-goals

- No HTTP or protocol wire schemas.
- No direct layer-01 table access.
- No hidden mutable persistence or provider selection.
