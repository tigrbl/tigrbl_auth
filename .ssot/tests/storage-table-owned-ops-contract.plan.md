# Storage Table Owned Operations Contract Test Plan

Planned tests will verify that durable table-specific operations are implemented on the owning `tigrbl_identity_storage.tables.*` modules and that protocol, REST route, server, runtime, operator, and facade modules only adapt and delegate.

The planned checks cover:

- storage table operation inventory by table type
- boundary enforcement for non-storage packages
- My Account table-owned operation placement
- OAuth table-owned operation placement
- facade import/export contract preservation
- delegation table-owned operation placement
