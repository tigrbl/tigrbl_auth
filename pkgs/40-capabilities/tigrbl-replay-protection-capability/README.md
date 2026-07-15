# tigrbl-replay-protection-capability

Layer-40 orchestration for protocol-neutral atomic replay reservations.

## Injected dependencies

A required `ReplayReservationPort` performs the reservation. Layer 60 selects
an ephemeral layer-20 provider or durable layer-30 operation and supplies the
allowed normalized namespaces.

## Operations and readiness

The required operation is `check_and_reserve`. Readiness, health, status,
provider identity, persistence mode, and namespaces are derived from the
effective provider binding and included in the capability report.

## Protocol consumers

OAuth, OIDC, OID4VCI, OID4VP, SET, EAT, GNAP, and HAIP layer-50 packages may
map their nonce/JTI/proof replay requirements to this operation.

## Non-goals

This package does not interpret protocol wire fields, choose retention windows,
own tables, open sessions, or silently claim durable persistence.
