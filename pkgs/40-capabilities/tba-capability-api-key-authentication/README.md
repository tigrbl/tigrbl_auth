# tba-capability-api-key-authentication

Mountable user API-key authentication over injected durable operations.

## Injected dependencies

- `tba-provider-authenticator-api-key-local`

## Operations and readiness

- `authenticate_api_key`

## Protocol consumers

- Protocol-neutral; layer-50 packages may bind these operations.

## Non-goals

- No HTTP or protocol wire schemas.
- No direct layer-01 table access.
- No hidden mutable persistence or provider selection.
