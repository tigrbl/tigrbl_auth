# tigrbl-account-self-service

Layer-40 current-account profile, password, session, and consent orchestration.

## Injected dependencies

The capability receives profile read/update, password change, session
list/revoke, consent list/revoke, and authorized-app revoke callables. Layer 60
normally adapts these callables to layer-30 table operations and hashing
providers. Every call is scoped by an authenticated `AccountPrincipal`.

## Operations and readiness

All nine operations are required. Construction rejects missing or non-callable
delegates, and returned records are checked against the protocol-neutral layer-2
contracts. The effective operation set is reported as `account.self-service`
version 1.0.

## Protocol consumers

This capability currently serves the layer-80 My Account HTTP carrier. A future
versioned account protocol can map to the same operations without acquiring
durable ownership.

## Non-goals

This package owns no tables, sessions, HTTP objects, hashing provider, request
authentication, or protocol binding.
