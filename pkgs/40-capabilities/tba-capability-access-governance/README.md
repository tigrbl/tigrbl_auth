# tba-capability-access-governance

Access reviews, entitlement management, provisioning governance, and service-identity registration.

## Injected dependencies

- `tba-provider-access-governance-memory`

## Operations and readiness

- `manage_entitlements`
- `run_access_review`

## Protocol consumers

- Protocol-neutral; layer-50 packages may bind these operations.

## Non-goals

- No HTTP or protocol wire schemas.
- No direct layer-01 table access.
- No hidden mutable persistence or provider selection.
