"""Compatibility activation facade over :mod:`tigrbl_table_durability`."""

from collections.abc import Iterable

from tigrbl import OpSpec, TableSpec
from tigrbl_table_durability import (
    activateRuntimeTableSpec,
    activateRuntimeTableSpecs,
    runtimeOperations,
)


def initializeIdentityRuntimeTables(
    specs: Iterable[TableSpec] | None = None,
) -> dict[str, tuple[OpSpec, ...]]:
    if specs is None:
        from .tables import DURABLE_RUNTIME_TABLE_SPECS

        specs = DURABLE_RUNTIME_TABLE_SPECS
    return activateRuntimeTableSpecs(specs)


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
