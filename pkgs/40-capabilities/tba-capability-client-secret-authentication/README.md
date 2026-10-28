# tba-capability-client-secret-authentication

Mountable client-secret authentication over injected client lookup.

## Injected dependencies

- `tba-provider-authenticator-client-secret-local`

## Operations and readiness

- `authenticate_client_secret`
- `verify_client_record`

## Protocol consumers

- Protocol-neutral; layer-50 packages may bind these operations.

## Non-goals

- No HTTP or protocol wire schemas.
- No direct layer-01 table access.
- No hidden mutable persistence or provider selection.
