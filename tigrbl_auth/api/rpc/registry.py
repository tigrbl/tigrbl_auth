"""Implementation-backed RPC method registry for the admin/operator plane."""

from __future__ import annotations

import asyncio
import importlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Awaitable, Callable, Mapping

from pydantic import BaseModel, ConfigDict

RpcHandler = Callable[[BaseModel, "RpcRequestContext"], Any | Awaitable[Any]]


class RpcSchema(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class EmptyParams(RpcSchema):
    """Methods with no parameters use an empty request object."""


@dataclass(slots=True, frozen=True)
class RpcMethodDefinition:
    name: str
    summary: str
    description: str
    params_model: type[BaseModel]
    result_model: type[BaseModel]
    handler: RpcHandler
    owner_module: str
    surface_set: str = "admin-rpc"
    required_flags: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    since_phase: str = "capability"

    def to_registry_metadata(self) -> dict[str, Any]:
        return {
            "surface_set": self.surface_set,
            "summary": self.summary,
            "description": self.description,
            "owner_module": self.owner_module,
            "required_flags": list(self.required_flags),
            "tags": list(self.tags),
            "since_phase": self.since_phase,
        }


@dataclass(slots=True)
class RpcRequestContext:
    repo_root: Path | None = None
    profile: str | None = None
    deployment: Any | None = None
    runtime_metadata: dict[str, Any] = field(default_factory=dict)

    def resolved_repo_root(self) -> Path:
        if self.repo_root is not None:
            return self.repo_root
        return Path(__file__).resolve().parents[3]


METHOD_MODULES: tuple[str, ...] = (
    "tigrbl_auth.api.rpc.methods.governance",
    "tigrbl_auth.api.rpc.methods.directory",
    "tigrbl_auth.api.rpc.methods.client_registration",
    "tigrbl_auth.api.rpc.methods.session",
    "tigrbl_auth.api.rpc.methods.token",
    "tigrbl_auth.api.rpc.methods.consent",
    "tigrbl_auth.api.rpc.methods.audit",
    "tigrbl_auth.api.rpc.methods.keys",
    "tigrbl_auth.api.rpc.methods.profile",
)

_METHODS: dict[str, RpcMethodDefinition] | None = None


def _load_method_definitions() -> dict[str, RpcMethodDefinition]:
    methods: dict[str, RpcMethodDefinition] = {}
    for module_name in METHOD_MODULES:
        module = importlib.import_module(module_name)
        for definition in getattr(module, "METHODS", ()):
            if definition.name in methods:
                raise ValueError(f"duplicate RPC method definition: {definition.name}")
            methods[definition.name] = definition
    return dict(sorted(methods.items(), key=lambda item: item[0]))


def list_rpc_methods() -> list[RpcMethodDefinition]:
    global _METHODS
    if _METHODS is None:
        _METHODS = _load_method_definitions()
    return list(_METHODS.values())


def get_rpc_method(name: str) -> RpcMethodDefinition:
    for item in list_rpc_methods():
        if item.name == name:
            return item
    raise KeyError(name)


def get_rpc_method_registry() -> dict[str, dict[str, Any]]:
    return {item.name: item.to_registry_metadata() for item in list_rpc_methods()}


def iter_active_rpc_methods(deployment: Any) -> list[RpcMethodDefinition]:
    active: list[RpcMethodDefinition] = []
    for item in list_rpc_methods():
        if hasattr(deployment, "surface_enabled") and not deployment.surface_enabled(item.surface_set):
            continue
        if item.required_flags and hasattr(deployment, "flag_enabled"):
            if not all(deployment.flag_enabled(flag) for flag in item.required_flags):
                continue
        active.append(item)
    return active


async def invoke_rpc_method_async(
    name: str,
    params: Mapping[str, Any] | BaseModel | None = None,
    *,
    context: RpcRequestContext | None = None,
) -> Any:
    definition = get_rpc_method(name)
    context = context or RpcRequestContext()
    if params is None:
        payload = definition.params_model()
    elif isinstance(params, definition.params_model):
        payload = params
    elif isinstance(params, BaseModel):
        payload = definition.params_model.model_validate(params.model_dump())
    else:
        payload = definition.params_model.model_validate(dict(params))
    result = definition.handler(payload, context)
    if asyncio.iscoroutine(result):
        result = await result
    if isinstance(result, BaseModel):
        return result.model_dump(mode="json")
    return result


def invoke_rpc_method(
    name: str,
    params: Mapping[str, Any] | BaseModel | None = None,
    *,
    context: RpcRequestContext | None = None,
) -> Any:
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(invoke_rpc_method_async(name, params, context=context))

    result_box: dict[str, Any] = {}
    error_box: dict[str, BaseException] = {}

    def runner() -> None:
        try:
            result_box["result"] = asyncio.run(invoke_rpc_method_async(name, params, context=context))
        except BaseException as exc:  # pragma: no cover - defensive surfacing
            error_box["error"] = exc

    import threading

    thread = threading.Thread(target=runner)
    thread.start()
    thread.join()
    if "error" in error_box:
        raise error_box["error"]
    return result_box.get("result")


__all__ = [
    "EmptyParams",
    "METHOD_MODULES",
    "RpcMethodDefinition",
    "RpcRequestContext",
    "RpcSchema",
    "get_rpc_method",
    "get_rpc_method_registry",
    "invoke_rpc_method",
    "invoke_rpc_method_async",
    "iter_active_rpc_methods",
    "list_rpc_methods",
]
