# tigrbl-protected-resource-authorization-capability

Layer-40 orchestration for a protected resource's normalized authorization
decision over validated access-token material.

## Injected dependencies

A required `ResourceServerVerifierPort` supplies token and claims verification.
The injected implementation may compose local signature validation,
introspection, sender constraints, and policy evaluation below this boundary.

## Operations and readiness

The required delegated operations are `verify_token` and `verify_claims`.
Construction fails when either operation is unavailable. The capability report
exposes both effective bindings and provider readiness.

## Protocol consumers

Layer-50 OAuth protected-resource profiles map bearer-token, JWT access-token,
introspection, DPoP, mTLS, and authorization requirements to this capability.

## Non-goals

This package does not parse HTTP, decode protocol wire formats, resolve keys,
open storage sessions, select trust anchors, or publish resource-server routes.
