# tigrbl-policy-administration-capability

Composable RBAC, ABAC, delegated-administration, simulation, and policy control-plane behavior.

## Injected dependencies

- `tigrbl-policy-administration-memory-provider`
- `tigrbl-authorization-policy-durability`

## Operations and readiness

- `administer`
- `simulate`

## Protocol consumers

- Protocol-neutral; layer-50 packages may bind these operations.

## Non-goals

- No HTTP or protocol wire schemas.
- No direct layer-01 table access.
- No hidden mutable persistence or provider selection.
