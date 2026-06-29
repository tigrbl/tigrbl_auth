"""Factory helpers for DPoP replay table variants."""

from __future__ import annotations

from typing import Any, Sequence, Type

from tigrbl.factories.engine import mem
from tigrbl.factories.table import defineTableSpec

from ._table import DpopReplay


def _derive_table(model: Type[DpopReplay], *, class_name: str, spec: type) -> Type[DpopReplay]:
    return type(
        class_name,
        (spec, model),
        {
            "__module__": __name__,
            "__table__": model.__table__,
            "__doc__": model.__doc__,
        },
    )


def defineDpopReplayTableSpec(
    *,
    engine: Any = None,
    ops: Sequence[Any] = (),
    columns: Sequence[Any] = (),
    schemas: Sequence[Any] = (),
    hooks: Sequence[Any] = (),
    security_deps: Sequence[Any] = (),
    deps: Sequence[Any] = (),
) -> type:
    return defineTableSpec(
        engine=engine,
        ops=ops,
        columns=columns,
        schemas=schemas,
        hooks=hooks,
        security_deps=security_deps,
        deps=deps,
    )


def deriveDpopReplayTable(
    model: Type[DpopReplay] = DpopReplay,
    *,
    class_name: str | None = None,
    engine: Any = None,
    ops: Sequence[Any] = (),
    columns: Sequence[Any] = (),
    schemas: Sequence[Any] = (),
    hooks: Sequence[Any] = (),
    security_deps: Sequence[Any] = (),
    deps: Sequence[Any] = (),
) -> Type[DpopReplay]:
    spec = defineDpopReplayTableSpec(
        engine=engine,
        ops=ops,
        columns=columns,
        schemas=schemas,
        hooks=hooks,
        security_deps=security_deps,
        deps=deps,
    )
    return _derive_table(model, class_name=class_name or f"{model.__name__}WithSpec", spec=spec)


def makeDpopReplayTable(
    *,
    class_name: str = "DpopReplayWithEngine",
    engine: Any = None,
    model: Type[DpopReplay] = DpopReplay,
    ops: Sequence[Any] = (),
    columns: Sequence[Any] = (),
    schemas: Sequence[Any] = (),
    hooks: Sequence[Any] = (),
    security_deps: Sequence[Any] = (),
    deps: Sequence[Any] = (),
) -> Type[DpopReplay]:
    return deriveDpopReplayTable(
        model,
        class_name=class_name,
        engine=engine,
        ops=ops,
        columns=columns,
        schemas=schemas,
        hooks=hooks,
        security_deps=security_deps,
        deps=deps,
    )


def makeInMemoryDpopReplayTable(
    *,
    class_name: str = "InMemoryDpopReplay",
    async_: bool = True,
    model: Type[DpopReplay] = DpopReplay,
) -> Type[DpopReplay]:
    return makeDpopReplayTable(class_name=class_name, engine=mem(async_=async_), model=model)


__all__ = [
    "defineDpopReplayTableSpec",
    "deriveDpopReplayTable",
    "makeDpopReplayTable",
    "makeInMemoryDpopReplayTable",
]
