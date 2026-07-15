# tigrbl-token-issuance-capability

Layer-40 orchestration for token-pair issuance and refresh rotation.

## Injected dependencies

Required callables issue a token pair and redeem/rotate a refresh token. An
optional audit callable records lifecycle events. Runtime composition supplies
signing providers and durable layer-30 state behind these callables.

## Operations and readiness

Required operations are `issue_token_pair` and `redeem_refresh_token`; optional
`record_audit_event` reports unavailable when unbound. Readiness requires both
issuance targets.

## Protocol consumers

Layer-50 OAuth grant/token bindings and OIDC token flows consume these
operations with explicit token profiles.

## Non-goals

This package does not parse requests, authenticate clients, select grants,
sign tokens, choose token profiles, open sessions, or own lifecycle state.
