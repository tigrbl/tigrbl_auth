from __future__ import annotations

from collections.abc import Iterable
from typing import Any


def _iter_security_dependencies(dep: Any, seen: set[int]) -> Iterable[Any]:
    if dep is None:
        return

    dep_id = id(dep)
    if dep_id in seen:
        return
    seen.add(dep_id)

    dependency = getattr(dep, "dependency", None)
    if dependency is not None:
        yield from _iter_security_dependencies(dependency, seen)
        return

    yield dep


def _security_requirement(dep: Any) -> list[dict[str, list[str]]]:
    requirement = getattr(dep, "openapi_security_requirement", None)
    if callable(requirement):
        value = requirement()
        if isinstance(value, dict):
            return [value]
        if isinstance(value, list) and all(isinstance(item, dict) for item in value):
            return value

    if dep.__class__.__name__ == "HTTPBearer":
        scheme_name = getattr(dep, "scheme_name", None) or "HTTPBearer"
        return [{scheme_name: []}]
    return []


def _security_scheme(dep: Any) -> dict[str, Any]:
    scheme_factory = getattr(dep, "openapi_security_scheme", None)
    requirement = _security_requirement(dep)
    if callable(scheme_factory) and requirement:
        scheme = scheme_factory()
        if isinstance(scheme, dict):
            scheme_name = next(iter(requirement[0].keys()), None)
            if scheme_name:
                return {scheme_name: scheme}

    if dep.__class__.__name__ == "HTTPBearer":
        scheme_name = getattr(dep, "scheme_name", None) or "HTTPBearer"
        return {scheme_name: {"type": "http", "scheme": "bearer"}}
    return {}


def security_from_dependencies(deps: Iterable[Any]) -> list[dict[str, list[str]]]:
    security: list[dict[str, list[str]]] = []
    seen: set[int] = set()
    for dep in deps:
        for security_dep in _iter_security_dependencies(dep, seen):
            security.extend(_security_requirement(security_dep))
    return security


def security_schemes_from_dependencies(deps: Iterable[Any]) -> dict[str, Any]:
    schemes: dict[str, Any] = {}
    seen: set[int] = set()
    for dep in deps:
        for security_dep in _iter_security_dependencies(dep, seen):
            schemes.update(_security_scheme(security_dep))
    return schemes


def install_tigrbl_openapi_security_compat() -> None:
    from tigrbl.system.docs.openapi import schema as openapi_schema

    openapi_schema._security_from_dependencies = security_from_dependencies
    openapi_schema._security_schemes_from_dependencies = security_schemes_from_dependencies


__all__ = [
    "install_tigrbl_openapi_security_compat",
    "security_from_dependencies",
    "security_schemes_from_dependencies",
]
