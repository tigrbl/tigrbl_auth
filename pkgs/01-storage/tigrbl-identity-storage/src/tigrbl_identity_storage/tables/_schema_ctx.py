from __future__ import annotations

from types import SimpleNamespace


def set_schema(model: type, op_name: str, *, in_: object | None = None, out: object | None = None) -> None:
    schemas = getattr(model, "schemas", None)
    if schemas is None:
        schemas = SimpleNamespace()
        setattr(model, "schemas", schemas)
    setattr(schemas, op_name, SimpleNamespace(in_=in_, out=out))


__all__ = ["set_schema"]
