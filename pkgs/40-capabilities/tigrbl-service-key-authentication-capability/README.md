# tigrbl-service-key-authentication-capability

Mountable service-key authentication over injected durable operations.

## Injected dependencies

- `tigrbl-authenticator-service-key-local`
- `tigrbl-api-key-authentication-capability`

## Operations and readiness

- `authenticate_service_key`

## Protocol consumers

- Protocol-neutral; layer-50 packages may bind these operations.

## Non-goals

- No HTTP or protocol wire schemas.
- No direct layer-01 table access.
- No hidden mutable persistence or provider selection.
