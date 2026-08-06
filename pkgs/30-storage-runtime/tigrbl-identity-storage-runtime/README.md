# tigrbl-identity-storage-runtime

Aggregate runtime for the split layer-30 durability packages.

Table specifications use Tigrbl's public `makeOp`, `defineTableSpec`,
`deriveTableSpec`, `provideTableSpec`, and `activateTableSpec` functions.
Table-family operations remain in their standalone `*-durability` owner; this
aggregate package collects and activates them without defining factory aliases.

Layer 30 owns carrier-neutral Tigrbl operations, derived table specifications,
and durability hooks. It does not own tables or migrations (layer 01), semantic
contracts (layer 02), provider selection (layer 20), engine construction
(layer 60), HTTP routes, or protocol wire models.
