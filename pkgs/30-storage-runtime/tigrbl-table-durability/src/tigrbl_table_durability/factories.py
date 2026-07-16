"""Stable factory aliases for layer-30 authoring."""

from .define import defineRuntimeTableSpec
from .derive import deriveRuntimeTableSpec
from .make import makeRuntimeOperation

operation = makeRuntimeOperation
table_spec = defineRuntimeTableSpec
derive = deriveRuntimeTableSpec

__all__ = [
    "defineRuntimeTableSpec",
    "deriveRuntimeTableSpec",
    "makeRuntimeOperation",
    "derive",
    "operation",
    "table_spec",
]
