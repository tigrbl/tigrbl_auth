# tba-capability-policy-administration

Composable RBAC, ABAC, delegated-administration, simulation, and policy control-plane behavior.

## Injected dependencies

- `tba-provider-policy-administration-memory`
- `tba-durability-authorization-policy`

## Operations and readiness

- `administer`
- `simulate`

## Protocol consumers

- Protocol-neutral; layer-50 packages may bind these operations.

## Non-goals

- No HTTP or protocol wire schemas.
- No direct layer-01 table access.
- No hidden mutable persistence or provider selection.
