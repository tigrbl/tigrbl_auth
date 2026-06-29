"""Concrete DPoP replay and nonce table variants."""

from __future__ import annotations

from typing import Any, Sequence, Type, TypeVar

from tigrbl.factories.engine import mem
from tigrbl.factories.table import defineTableSpec
from tigrbl_identity_storage.tables import DpopNonce, DpopReplay

_T = TypeVar("_T", bound=type)


def _derive_table(model: _T, *, class_name: str, spec: type) -> _T:
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


def defineDpopNonceTableSpec(
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


def deriveDpopNonceTable(
    model: Type[DpopNonce] = DpopNonce,
    *,
    class_name: str | None = None,
    engine: Any = None,
    ops: Sequence[Any] = (),
    columns: Sequence[Any] = (),
    schemas: Sequence[Any] = (),
    hooks: Sequence[Any] = (),
    security_deps: Sequence[Any] = (),
    deps: Sequence[Any] = (),
) -> Type[DpopNonce]:
    spec = defineDpopNonceTableSpec(
        engine=engine,
        ops=ops,
        columns=columns,
        schemas=schemas,
        hooks=hooks,
        security_deps=security_deps,
        deps=deps,
    )
    return _derive_table(model, class_name=class_name or f"{model.__name__}WithSpec", spec=spec)


def makeDpopNonceTable(
    *,
    class_name: str = "DpopNonceWithEngine",
    engine: Any = None,
    model: Type[DpopNonce] = DpopNonce,
    ops: Sequence[Any] = (),
    columns: Sequence[Any] = (),
    schemas: Sequence[Any] = (),
    hooks: Sequence[Any] = (),
    security_deps: Sequence[Any] = (),
    deps: Sequence[Any] = (),
) -> Type[DpopNonce]:
    return deriveDpopNonceTable(
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


def makeInMemoryDpopNonceTable(
    *,
    class_name: str = "InMemoryDpopNonce",
    async_: bool = True,
    model: Type[DpopNonce] = DpopNonce,
) -> Type[DpopNonce]:
    return makeDpopNonceTable(class_name=class_name, engine=mem(async_=async_), model=model)


__all__ = [
    "defineDpopNonceTableSpec",
    "defineDpopReplayTableSpec",
    "deriveDpopNonceTable",
    "deriveDpopReplayTable",
    "makeDpopNonceTable",
    "makeDpopReplayTable",
    "makeInMemoryDpopNonceTable",
    "makeInMemoryDpopReplayTable",
]
