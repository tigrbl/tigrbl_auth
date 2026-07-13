"""Explicit activation of derived runtime behavior on canonical tables."""

from __future__ import annotations

from collections.abc import Iterable

from tigrbl import Hook, OpSpec, TableSpec, rebind


def runtimeOperations(spec: TableSpec) -> tuple[OpSpec, ...]:
    """Return only operations authored by this layer-30 runtime."""

    return tuple(
        operation
        for operation in spec.ops
        if operation.extra.get("owner_layer") == "30-storage-runtime"
    )


def activateRuntimeTableSpec(spec: TableSpec) -> tuple[OpSpec, ...]:
    """Attach derived operations and ask Tigrbl to rematerialize the table."""

    table = spec.model
    if not isinstance(table, type):
        raise TypeError("runtime table specification requires a model class")
    existing = tuple(getattr(table, "__tigrbl_ops__", ()) or ())
    merged = {
        (operation.alias, operation.target): operation
        for operation in (*existing, *runtimeOperations(spec))
    }
    table.__tigrbl_ops__ = tuple(merged.values())
    existing_hooks = tuple(getattr(table, "HOOKS", ()) or ())
    merged_hooks: dict[tuple[str | None, object, object], Hook] = {}
    for hook in (*existing_hooks, *tuple(spec.hooks)):
        if not isinstance(hook, Hook):
            continue
        merged_hooks[(hook.name, hook.phase, hook.ops)] = hook
    table.HOOKS = tuple(merged_hooks.values())
    return tuple(rebind(table))


def initializeIdentityRuntimeTables(
    specs: Iterable[TableSpec] | None = None,
) -> dict[str, tuple[OpSpec, ...]]:
    """Activate the durable table families selected by the runtime composer."""

    if specs is None:
        from .tables import DURABLE_RUNTIME_TABLE_SPECS

        specs = DURABLE_RUNTIME_TABLE_SPECS
    activated: dict[str, tuple[OpSpec, ...]] = {}
    for spec in specs:
        table = spec.model
        activated[table.__name__] = activateRuntimeTableSpec(spec)
    return activated


activate_runtime_table_spec = activateRuntimeTableSpec
initialize_identity_runtime_tables = initializeIdentityRuntimeTables
runtime_operations = runtimeOperations

__all__ = [
    "activateRuntimeTableSpec",
    "activate_runtime_table_spec",
    "initializeIdentityRuntimeTables",
    "initialize_identity_runtime_tables",
    "runtimeOperations",
    "runtime_operations",
]
