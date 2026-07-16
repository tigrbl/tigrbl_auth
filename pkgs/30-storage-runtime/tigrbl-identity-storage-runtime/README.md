# tigrbl-identity-storage-runtime

Compatibility facade for the split layer-30 durability packages.

New code should import the neutral authoring substrate from
`tigrbl-table-durability` and table-family operations from their standalone
`*-durability` owner. This aggregate package preserves the previous imports
while callers migrate.

Layer 30 owns carrier-neutral Tigrbl operations, derived table specifications,
and durability hooks. It does not own tables or migrations (layer 01), semantic
contracts (layer 02), provider selection (layer 20), engine construction
(layer 60), HTTP routes, or protocol wire models.
