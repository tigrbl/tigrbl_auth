# tigrbl-table-durability

Protocol-neutral layer-30 authoring and activation primitives for attaching
durable operations to canonical Tigrbl tables.

This package owns operation construction, table-spec derivation, handler
invocation, and explicit activation. It does not own tables, engines, HTTP
bindings, protocol models, providers, or application composition.
