# tigrbl-token-revocation-capability

Layer-40 orchestration for protocol-neutral durable token revocation.

## Injected dependencies

A required revocation callable mutates durable token state; an optional audit
callable records the lifecycle event. Both may be synchronous or asynchronous.

## Operations and readiness

`revoke_token` is required and `record_audit_event` is optional. Readiness
follows the revocation binding, while the report separately exposes audit
availability.

## Protocol consumers

The layer-50 OAuth package maps RFC 7009 behavior to this capability. Other
protocol profiles reuse the normalized revocation result where applicable.

## Non-goals

This package does not parse HTTP, authenticate callers, select RFC responses,
open sessions, resolve token profiles, or own revocation storage.
