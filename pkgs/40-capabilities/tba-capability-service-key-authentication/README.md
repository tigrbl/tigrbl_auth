# tba-capability-service-key-authentication

Mountable service-key authentication over injected durable operations.

## Injected dependencies

- `tba-provider-authenticator-service-key-local`
- `tba-capability-api-key-authentication`

## Operations and readiness

- `authenticate_service_key`

## Protocol consumers

- Protocol-neutral; layer-50 packages may bind these operations.

## Non-goals

- No HTTP or protocol wire schemas.
- No direct layer-01 table access.
- No hidden mutable persistence or provider selection.
