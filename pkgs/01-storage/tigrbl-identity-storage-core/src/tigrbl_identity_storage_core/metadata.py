"""Selected-component metadata helpers."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any


def tables_for_models(models: Iterable[type[Any]]) -> tuple[Any, ...]:
    """Return mapped tables for an explicit model inventory."""

    return tuple(model.__table__ for model in models)


def table_names_for_models(models: Iterable[type[Any]]) -> tuple[str, ...]:
    """Return deterministic schema-qualified names for selected models."""

    names = []
    for table in tables_for_models(models):
        names.append(f"{table.schema}.{table.name}" if table.schema else table.name)
    return tuple(sorted(names))


__all__ = ["table_names_for_models", "tables_for_models"]
