# tigrbl-token-exchange-capability

Layer-40 protocol-neutral orchestration for security-token exchange.

## Injected dependencies

A required exchange implementation receives a normalized exchange request and
trusted execution context. Runtime composition supplies verification, issuance,
durable lineage, and audit collaborators behind that implementation.

## Operations and readiness

The required operation is `exchange_token`. Construction fails when its target
is absent, so the bound required-operation set determines readiness.

## Protocol consumers

The layer-50 OAuth package maps RFC 8693 request/response fields and errors to
this capability. Other profiles must reuse the typed exchange operation rather
than fork its semantic identity.

## Non-goals

This package does not own RFC wire names, HTTP, deployment settings,
persistence, token signing, key/trust policy, or grant authorization.
