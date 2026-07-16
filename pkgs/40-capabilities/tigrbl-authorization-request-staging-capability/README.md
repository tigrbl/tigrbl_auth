# tigrbl-pushed-authorization-capability

Layer-40 orchestration for persisting an already normalized and authenticated
pushed authorization request.

## Injected dependencies

A durable request-URI creation callable is required. A durable audit callable
is optional. Both may be synchronous or asynchronous.

## Operations and readiness

`push_authorization_request` is required; `record_audit_event` is optional.
Readiness follows the persistence binding, and the report exposes audit
availability separately.

## Protocol consumers

The layer-50 OAuth package maps RFC 9126 PAR to this capability. OIDC and HAIP
consume it through their configured OAuth/FAPI compositions where applicable.

## Non-goals

This package does not parse HTTP, authenticate clients, validate request
objects/DPoP, choose FAPI policy or RFC errors, open sessions, or own state.
