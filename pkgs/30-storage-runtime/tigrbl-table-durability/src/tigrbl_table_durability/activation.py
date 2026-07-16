"""Explicit activation of derived durable table behavior."""

from __future__ import annotations

from collections.abc import Iterable

from tigrbl import Hook, OpSpec, TableSpec, rebind


def runtimeOperations(spec: TableSpec) -> tuple[OpSpec, ...]:
    return tuple(
        operation
        for operation in spec.ops
        if operation.extra.get("owner_layer") == "30-storage-runtime"
    )


def activateRuntimeTableSpec(spec: TableSpec) -> tuple[OpSpec, ...]:
    table = spec.model
    if not isinstance(table, type):
        raise TypeError("runtime table specification requires a model class")
    existing = tuple(getattr(table, "__tigrbl_ops__", ()) or ())
    merged = {
        (operation.alias, operation.target): operation
        for operation in (*existing, *runtimeOperations(spec))
    }
    table.__tigrbl_ops__ = tuple(merged.values())
    hooks: dict[tuple[str | None, object, object], Hook] = {}
    for hook in (*tuple(getattr(table, "HOOKS", ()) or ()), *tuple(spec.hooks)):
        if isinstance(hook, Hook):
            hooks[(hook.name, hook.phase, hook.ops)] = hook
    table.HOOKS = tuple(hooks.values())
    return tuple(rebind(table))


def activateRuntimeTableSpecs(
    specs: Iterable[TableSpec],
) -> dict[str, tuple[OpSpec, ...]]:
    return {spec.model.__name__: activateRuntimeTableSpec(spec) for spec in specs}


activate_runtime_table_spec = activateRuntimeTableSpec
activate_runtime_table_specs = activateRuntimeTableSpecs
runtime_operations = runtimeOperations

__all__ = [
    "activateRuntimeTableSpec",
    "activateRuntimeTableSpecs",
    "activate_runtime_table_spec",
    "activate_runtime_table_specs",
    "runtimeOperations",
    "runtime_operations",
]
