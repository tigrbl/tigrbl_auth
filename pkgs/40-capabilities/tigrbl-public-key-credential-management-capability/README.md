# tigrbl-public-key-credential-management-capability

Mountable listing, renaming, and revocation of registered public-key credentials.

## Injected dependencies

Authenticated list, rename, and revoke callables supplied by durable runtime composition.

## Operations and readiness

All three declared operations are required and readiness is false when any target is absent.

## Protocol consumers

Account-management and WebAuthn application surfaces consume these operations.

## Non-goals

This package does not own tables, authorization policy, routes, or WebAuthn wire structures.
