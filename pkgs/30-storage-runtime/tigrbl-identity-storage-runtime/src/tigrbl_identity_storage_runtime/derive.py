"""Derive executable specifications from canonical layer-01 tables."""

from __future__ import annotations

from dataclasses import replace
from typing import Any, Iterable

from tigrbl import OpSpec, TableSpec


def _merge_operations(
    existing: Iterable[Any], incoming: Iterable[Any]
) -> tuple[Any, ...]:
    merged: dict[tuple[str, str], Any] = {}
    for operation in (*tuple(existing), *tuple(incoming)):
        key = (operation.alias, operation.target)
        merged[key] = operation
    return tuple(merged.values())


def deriveRuntimeTableSpec(
    table: type,
    *,
    operations: Iterable[OpSpec] = (),
    hooks: Iterable[Any] = (),
    schemas: Iterable[Any] = (),
    dependencies: Iterable[Any] = (),
    security_dependencies: Iterable[Any] = (),
) -> TableSpec:
    """Overlay runtime behavior without subclassing an already-mapped ORM table.

    Tigrbl's generic ``deriveTable`` factory is appropriate while authoring an
    unmapped table class.  Layer-01 identity tables are already SQLAlchemy
    mapped, so layer 30 derives their collected specification instead of
    creating an invalid joined-inheritance mapping of the same table.
    """

    collected = TableSpec.collect(table)
    return replace(
        collected,
        ops=_merge_operations(collected.ops, operations),
        hooks=(*tuple(collected.hooks), *tuple(hooks)),
        schemas=(*tuple(collected.schemas), *tuple(schemas)),
        deps=(*tuple(collected.deps), *tuple(dependencies)),
        security_deps=(
            *tuple(collected.security_deps),
            *tuple(security_dependencies),
        ),
    )


derive_runtime_table_spec = deriveRuntimeTableSpec

__all__ = ["deriveRuntimeTableSpec", "derive_runtime_table_spec"]
