"""Collected runtime specifications for canonical identity tables."""

from __future__ import annotations

from tigrbl_identity_storage.tables import TABLE_MODELS

from .derive import deriveRuntimeTableSpec


RUNTIME_TABLES = tuple(TABLE_MODELS)
RUNTIME_TABLE_BY_NAME = {table.__name__: table for table in RUNTIME_TABLES}
RUNTIME_TABLE_SPECS = tuple(deriveRuntimeTableSpec(table) for table in RUNTIME_TABLES)
RUNTIME_TABLE_SPEC_BY_NAME = {
    table.__name__: spec for table, spec in zip(RUNTIME_TABLES, RUNTIME_TABLE_SPECS)
}
RUNTIME_OPERATION_BY_ALIAS = {
    (table.__name__, operation.alias): operation
    for table, spec in zip(RUNTIME_TABLES, RUNTIME_TABLE_SPECS)
    for operation in spec.ops
}

__all__ = [
    "RUNTIME_OPERATION_BY_ALIAS",
    "RUNTIME_TABLE_BY_NAME",
    "RUNTIME_TABLE_SPEC_BY_NAME",
    "RUNTIME_TABLE_SPECS",
    "RUNTIME_TABLES",
]
