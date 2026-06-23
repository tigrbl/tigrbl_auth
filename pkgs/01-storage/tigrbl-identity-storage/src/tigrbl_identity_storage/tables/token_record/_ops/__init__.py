"""TokenRecord-owned operation surface."""

from __future__ import annotations

from importlib import import_module
from types import ModuleType
from typing import Any

from . import _introspection
from . import _persistence
from . import _records

_BASE_MODULES = (_persistence, _records, _introspection)
_runtime: ModuleType | None = None
_request: ModuleType | None = None


def _export_module(module: ModuleType, *, skip: set[str] | None = None) -> None:
    skipped = skip or set()
    globals().update(
        {
            name: value
            for name, value in module.__dict__.items()
            if not name.startswith("__") and name not in skipped
        }
    )


for _module in _BASE_MODULES:
    _export_module(_module)


def _load_runtime_modules() -> tuple[ModuleType, ModuleType]:
    global _runtime, _request
    if _runtime is None or _request is None:
        runtime_module = import_module(f"{__name__}._runtime")
        request_module = import_module(f"{__name__}._request")
        _runtime = runtime_module
        _request = request_module
        _export_module(_runtime, skip={"_load_client"})
    return _runtime, _request


def _iter_sync_names() -> tuple[str, ...]:
    modules = list(_BASE_MODULES)
    if _runtime is not None:
        modules.append(_runtime)
    return tuple(
        name
        for module in modules
        for name in module.__dict__
        if not name.startswith("__")
    )


def _sync_request_runtime() -> None:
    runtime, request = _load_runtime_modules()
    for name in _iter_sync_names():
        if name not in globals():
            continue
        if name == "_load_client" and globals()[name] is _LOAD_CLIENT_WRAPPER:
            continue
        for module in (runtime, request):
            if hasattr(module, name):
                setattr(module, name, globals()[name])


async def _load_client(db: Any, client_id: str):
    runtime, _ = _load_runtime_modules()
    _sync_request_runtime()
    return await runtime._load_client(db, client_id)


_LOAD_CLIENT_WRAPPER = _load_client


async def token_request(*, request, db):
    _, request_module = _load_runtime_modules()
    _sync_request_runtime()
    return await request_module.token_request(request=request, db=db)


def __getattr__(name: str) -> Any:
    runtime, request = _load_runtime_modules()
    for module in (runtime, request):
        if hasattr(module, name):
            value = getattr(module, name)
            if name != "_load_client":
                globals()[name] = value
            return value
    raise AttributeError(f"{__name__!r} has no attribute {name!r}")


__all__ = sorted(
    {
        *_persistence.__all__,
        *_records.__all__,
        *_introspection.__all__,
        "_load_client",
        "token_request",
    }
)
