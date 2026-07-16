"""Define reusable specifications for durable table behavior."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from tigrbl.factories.table import defineTableSpec


def defineRuntimeTableSpec(
    *,
    operations: Sequence[Any] = (),
    hooks: Sequence[Any] = (),
    schemas: Sequence[Any] = (),
    dependencies: Sequence[Any] = (),
    security_dependencies: Sequence[Any] = (),
) -> type:
    return defineTableSpec(
        ops=tuple(operations),
        hooks=tuple(hooks),
        schemas=tuple(schemas),
        deps=tuple(dependencies),
        security_deps=tuple(security_dependencies),
    )


runtime_table_spec = defineRuntimeTableSpec

__all__ = ["defineRuntimeTableSpec", "runtime_table_spec"]
