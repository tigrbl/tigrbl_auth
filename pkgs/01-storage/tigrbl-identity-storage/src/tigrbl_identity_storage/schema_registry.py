"""OpenAPI-named schema registry derived from storage table bindings."""

from __future__ import annotations

from collections.abc import Iterable, Iterator, Mapping
from types import MappingProxyType
from typing import Any, Literal, get_args

from .tables.consent import MyAccountAuthorizedAppOut, MyAccountConsentOut
from .tables import TABLE_MODELS

SchemaDirection = Literal["in", "out"]
TableSchemaKey = tuple[str, str, SchemaDirection]
EXTRA_OPENAPI_SCHEMAS = (
    MyAccountAuthorizedAppOut,
    MyAccountConsentOut,
)


class SchemaRegistryError(RuntimeError):
    """Raised when table-bound schema metadata cannot form a stable registry."""


def _schema_json(schema: Any) -> dict[str, Any] | None:
    if hasattr(schema, "model_json_schema"):
        return schema.model_json_schema()
    if hasattr(schema, "schema"):
        return schema.schema()
    return None


def _schema_name(schema: Any) -> str | None:
    schema_name = getattr(schema, "__name__", "")
    if not schema_name or not schema_name.isidentifier():
        return None
    if _schema_json(schema) is None:
        return None
    return schema_name


def _iter_concrete_schemas(schema: Any) -> Iterator[Any]:
    if _schema_name(schema) is not None:
        yield schema
    for arg in get_args(schema):
        yield from _iter_concrete_schemas(arg)


def _iter_table_schema_bindings(
    table_models: Iterable[type],
) -> Iterator[tuple[TableSchemaKey, Any]]:
    for table_model in table_models:
        schemas = getattr(table_model, "schemas", None)
        if schemas is None:
            continue
        for op_name in dir(schemas):
            if op_name.startswith("_"):
                continue
            op_schema = getattr(schemas, op_name)
            for direction, attr in (("in", "in_"), ("out", "out")):
                schema = getattr(op_schema, attr, None)
                if schema is None:
                    continue
                yield (table_model.__name__, op_name, direction), schema


def _build_schema_indexes(
    table_models: Iterable[type],
    extra_openapi_schemas: Iterable[Any] = EXTRA_OPENAPI_SCHEMAS,
) -> tuple[dict[str, Any], dict[TableSchemaKey, Any]]:
    openapi_schemas: dict[str, Any] = {}
    table_bindings: dict[TableSchemaKey, Any] = {}
    schema_json_by_name: dict[str, dict[str, Any]] = {}

    for key, schema in _iter_table_schema_bindings(table_models):
        table_bindings[key] = schema
        for concrete_schema in _iter_concrete_schemas(schema):
            schema_name = _schema_name(concrete_schema)
            if schema_name is None:
                continue

            schema_json = _schema_json(concrete_schema)
            existing_json = schema_json_by_name.get(schema_name)
            if existing_json is not None and existing_json != schema_json:
                raise SchemaRegistryError(
                    f"duplicate OpenAPI schema name {schema_name!r} has conflicting shapes"
                )
            schema_json_by_name.setdefault(schema_name, schema_json or {})
            openapi_schemas.setdefault(schema_name, concrete_schema)

    for schema in extra_openapi_schemas:
        schema_name = _schema_name(schema)
        if schema_name is None:
            continue
        schema_json = _schema_json(schema)
        existing_json = schema_json_by_name.get(schema_name)
        if existing_json is not None and existing_json != schema_json:
            raise SchemaRegistryError(
                f"duplicate OpenAPI schema name {schema_name!r} has conflicting shapes"
            )
        schema_json_by_name.setdefault(schema_name, schema_json or {})
        openapi_schemas.setdefault(schema_name, schema)

    return openapi_schemas, table_bindings


_OPENAPI_SCHEMA_REGISTRY, _TABLE_SCHEMA_BINDINGS = _build_schema_indexes(TABLE_MODELS)

OPENAPI_SCHEMA_REGISTRY: Mapping[str, Any] = MappingProxyType(_OPENAPI_SCHEMA_REGISTRY)
TABLE_SCHEMA_BINDINGS: Mapping[TableSchemaKey, Any] = MappingProxyType(_TABLE_SCHEMA_BINDINGS)


def get_openapi_schema(name: str) -> Any:
    return OPENAPI_SCHEMA_REGISTRY[name]


def get_table_op_schema(table: str, op: str, direction: SchemaDirection) -> Any:
    return TABLE_SCHEMA_BINDINGS[(table, op, direction)]


def iter_openapi_schemas() -> Iterator[tuple[str, Any]]:
    yield from OPENAPI_SCHEMA_REGISTRY.items()


def iter_table_schema_bindings() -> Iterator[tuple[TableSchemaKey, Any]]:
    yield from TABLE_SCHEMA_BINDINGS.items()


__all__ = [
    "OPENAPI_SCHEMA_REGISTRY",
    "EXTRA_OPENAPI_SCHEMAS",
    "SchemaDirection",
    "SchemaRegistryError",
    "TABLE_SCHEMA_BINDINGS",
    "TableSchemaKey",
    "get_openapi_schema",
    "get_table_op_schema",
    "iter_openapi_schemas",
    "iter_table_schema_bindings",
]
