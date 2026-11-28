"""Activation entrypoint for the identity runtime table inventory."""

from collections.abc import Iterable

from tigrbl_concrete.factories import activateTableSpecs
from tigrbl_core._spec import OpSpec, TableSpec


def initializeIdentityRuntimeTables(
    specs: Iterable[TableSpec] | None = None,
) -> dict[str, tuple[OpSpec, ...]]:
    if specs is None:
        from .tables import DURABLE_RUNTIME_TABLE_SPECS

        specs = DURABLE_RUNTIME_TABLE_SPECS
    return activateTableSpecs(specs)


initialize_identity_runtime_tables = initializeIdentityRuntimeTables

__all__ = [
    "initializeIdentityRuntimeTables",
    "initialize_identity_runtime_tables",
]
