# tigrbl-identity-admin-control-plane

Layer-40 orchestration for tenant-scoped administrative resource lifecycle and
audit use cases.

## Injected dependencies

Create, read, list, update, delete, audit-record, and audit-list callables are
required. They are normally adapters over layer-30 table operations and may be
synchronous or asynchronous. The capability owns no in-memory backing store.

## Operations and readiness

Operations cover creation of principals, credentials, apps, service identities,
resource servers, and policies plus `get`, `metadata`, `list`, `update`,
`delete`, and `list_audit_events`. Every operation is required and construction
fails when a target is absent.

`OperatorAdministrationCapability` is the policy-gated operator surface used by
layer-60 command runtimes. It receives an authorization callable and the
layer-30 resource, identity-secret, and key-lifecycle operations. Authorization
runs before every delegated operation. Its effective operation set is available
through the standard capability report.

## Protocol consumers

No layer-50 protocol currently consumes this administrative capability. Layer
60 composes it for layer-80 administrative APIs; future versioned admin
protocols must map to these operations rather than bypassing them.

## Non-goals

This package does not own tables, sessions, HTTP/RPC, authorization policy,
credential verification, secret handling, or protocol-specific schemas.
