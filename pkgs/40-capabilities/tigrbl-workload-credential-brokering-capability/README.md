# tigrbl-workload-credential-brokering-capability

Independently mountable, carrier-neutral capability. Layer 50 maps its operations into versioned protocols.

## Injected dependencies

- No package-mandated runtime dependency; callables are constructor-injected.

## Operations and readiness

- `authorize_delegated_credential_access`
- `obtain_delegated_workload_credentials`
- `resolve_delegated_workload_trust`
- `resolve_workload_reference`
- `watch_delegated_workload_credentials`

## Protocol consumers

- Protocol-neutral; layer-50 packages may bind these operations.

## Non-goals

- No HTTP or protocol wire schemas.
- No direct layer-01 table access.
- No hidden mutable persistence or provider selection.
