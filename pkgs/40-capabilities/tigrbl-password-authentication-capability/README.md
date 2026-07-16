# tigrbl-password-authentication-capability

Mountable password authentication over injected identity lookup and a password authenticator provider.

## Injected dependencies

- `tigrbl-authenticator-password-local`

## Operations and readiness

- `authenticate_password`

## Protocol consumers

- Protocol-neutral; layer-50 packages may bind these operations.

## Non-goals

- No HTTP or protocol wire schemas.
- No direct layer-01 table access.
- No hidden mutable persistence or provider selection.
