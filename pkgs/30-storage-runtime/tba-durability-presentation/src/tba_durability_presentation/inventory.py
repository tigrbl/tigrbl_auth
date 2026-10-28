"""Immutable inventory of this durable family's table specifications."""

from . import specifications as _specifications

RUNTIME_TABLE_SPECS = tuple(
    value
    for name, value in vars(_specifications).items()
    if name.endswith("RuntimeSpec") and getattr(value, "model", None) is not None
)
RUNTIME_TABLES = tuple(spec.model for spec in RUNTIME_TABLE_SPECS)
RUNTIME_OPERATION_BY_ALIAS = {
    operation.alias: operation
    for spec in RUNTIME_TABLE_SPECS
    for operation in spec.ops
    if operation.extra.get("owner_layer") == "30-storage-runtime"
}

__all__ = [
    "RUNTIME_OPERATION_BY_ALIAS",
    "RUNTIME_TABLE_SPECS",
    "RUNTIME_TABLES",
]
