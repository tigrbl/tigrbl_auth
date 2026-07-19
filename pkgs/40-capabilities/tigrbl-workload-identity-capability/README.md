# tigrbl-workload-identity-capability

Protocol-neutral workload credential acquisition, verification, trust resolution, and refresh capability. SPIFFE and WIMSE mappings belong in layer 50.

## Injected dependencies

- No package-mandated runtime dependency; callables are constructor-injected.

## Operations and readiness

- `obtain_workload_credential`
- `refresh_workload_credentials`
- `resolve_workload_trust`
- `verify_workload_credential`

## Protocol consumers

- Protocol-neutral; layer-50 packages may bind these operations.

## Non-goals

- No HTTP or protocol wire schemas.
- No direct layer-01 table access.
- No hidden mutable persistence or provider selection.
