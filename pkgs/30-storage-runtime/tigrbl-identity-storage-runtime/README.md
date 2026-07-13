# tigrbl-identity-storage-runtime

Layer-30 executable durability for the canonical tables owned by
`tigrbl-identity-storage`.

The package authors carrier-neutral Tigrbl operations and derives collected
table specifications. Persistence is executed by the table handler with an
engine/session-bearing context; constructing an operation or specification
does not itself perform durable work.

Public authoring surfaces:

- `makeRuntimeOperation` / `runtime_operation`
- `defineRuntimeTableSpec` / `runtime_table_spec`
- `deriveRuntimeTableSpec` / `derive_runtime_table_spec`
- `RUNTIME_TABLES`, `RUNTIME_TABLE_SPECS`, and indexed inventories

Layer 30 does not own HTTP routes, OAuth/OIDC wire models, engine selection,
or application mounting. Repository and store compatibility surfaces remain
temporarily while their callers are migrated to table handlers.

Runtime execution helpers for Tigrbl identity storage.

This package composes the durable table and migration definitions from
`tigrbl-identity-storage` with runtime engine/provider resolution from
`tigrbl-identity-runtime`. Durable schemas, table classes, migration version
files, and storage helpers remain owned by `tigrbl-identity-storage`.
