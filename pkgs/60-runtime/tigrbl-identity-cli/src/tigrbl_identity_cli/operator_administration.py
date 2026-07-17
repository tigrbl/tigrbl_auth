"""Layer-60 composition for policy-gated operator administration."""

from __future__ import annotations

import asyncio
from collections.abc import Callable, Mapping
from functools import lru_cache
from pathlib import Path

from tigrbl_operator_administration_capability import OperatorAdministrationCapability
from tigrbl_identity_runtime import CapabilityRegistry
from tigrbl_identity_storage_runtime.key_management import (
    create_operator_key_for_context,
    delete_operator_key_for_context,
    export_operator_key_for_context,
    generate_operator_key_for_context,
    get_operator_key_for_context,
    import_operator_key_for_context,
    list_operator_keys_for_context,
    publish_operator_jwks_for_context,
    retire_operator_key_for_context,
    rotate_operator_key_for_context,
    seed_operator_key_for_context,
    update_operator_key_for_context,
)
from tigrbl_identity_storage_runtime.operator_store import (
    ArtifactResult,
    OperationContext,
    TransactionResult,
    operator_state_root,
)
from tigrbl_identity_storage_runtime.resource_service import (
    OperatorStateError,
    create_resource as _create_resource,
    delete_resource as _delete_resource,
    get_resource as _get_resource,
    list_resource_result as _list_resources,
    lock_identity as _lock_identity,
    rotate_client_secret as _rotate_client_secret,
    set_identity_password as _set_identity_password,
    toggle_resource as _toggle_resource,
    update_resource as _update_resource,
)


OperatorAuthorizer = Callable[[str, object], object]


def authorize_local_operator(operation: str, context: object) -> None:
    """Require an identified local operator before delegating durable work."""

    actor = str(getattr(context, "actor", "") or "").strip()
    if not actor:
        raise PermissionError(f"{operation} requires an identified operator")


def operator_administration_delegates() -> Mapping[str, Callable[..., object]]:
    return {
        "create_resource": _create_resource,
        "delete_resource": _delete_resource,
        "get_resource": _get_resource,
        "key_create": create_operator_key_for_context,
        "key_delete": delete_operator_key_for_context,
        "key_export": export_operator_key_for_context,
        "key_generate": generate_operator_key_for_context,
        "key_get": get_operator_key_for_context,
        "key_import": import_operator_key_for_context,
        "key_list": list_operator_keys_for_context,
        "key_publish_jwks": publish_operator_jwks_for_context,
        "key_retire": retire_operator_key_for_context,
        "key_rotate": rotate_operator_key_for_context,
        "key_seed": seed_operator_key_for_context,
        "key_update": update_operator_key_for_context,
        "list_resources": _list_resources,
        "lock_identity": _lock_identity,
        "rotate_client_secret": _rotate_client_secret,
        "set_identity_password": _set_identity_password,
        "toggle_resource": _toggle_resource,
        "update_resource": _update_resource,
    }


def build_operator_administration_capability(
    *,
    authorize: OperatorAuthorizer = authorize_local_operator,
    delegates: Mapping[str, Callable[..., object]] | None = None,
) -> OperatorAdministrationCapability:
    return OperatorAdministrationCapability(
        authorize=authorize,
        delegates=delegates or operator_administration_delegates(),
    )


@lru_cache(maxsize=1)
def operator_administration_registry() -> CapabilityRegistry:
    return CapabilityRegistry((build_operator_administration_capability(),))


def call_operator_administration(
    operation: str,
    context: OperationContext,
    /,
    **kwargs: object,
) -> object:
    """Invoke the operator capability from the synchronous CLI boundary."""

    async def invoke() -> object:
        result = await operator_administration_registry().call(
            "identity-admin.operator",
            operation,
            context,
            **kwargs,
        )
        return result.value

    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(invoke())
    raise RuntimeError("synchronous CLI administration cannot run inside an event loop")


def create_resource(context: OperationContext, **kwargs: object) -> object:
    return call_operator_administration("create_resource", context, **kwargs)


def update_resource(context: OperationContext, **kwargs: object) -> object:
    return call_operator_administration("update_resource", context, **kwargs)


def delete_resource(context: OperationContext, **kwargs: object) -> object:
    return call_operator_administration("delete_resource", context, **kwargs)


def get_resource(context: OperationContext, **kwargs: object) -> object:
    return call_operator_administration("get_resource", context, **kwargs)


def list_resources(context: OperationContext, **kwargs: object) -> object:
    return call_operator_administration("list_resources", context, **kwargs)


def toggle_resource(context: OperationContext, **kwargs: object) -> object:
    return call_operator_administration("toggle_resource", context, **kwargs)


def rotate_client_secret(context: OperationContext, **kwargs: object) -> object:
    return call_operator_administration("rotate_client_secret", context, **kwargs)


def set_identity_password(context: OperationContext, **kwargs: object) -> object:
    return call_operator_administration("set_identity_password", context, **kwargs)


def lock_identity(context: OperationContext, **kwargs: object) -> object:
    return call_operator_administration("lock_identity", context, **kwargs)


def key_generate(context: OperationContext, **kwargs: object) -> object:
    return call_operator_administration("key_generate", context, **kwargs)


def key_import(context: OperationContext, **kwargs: object) -> object:
    return call_operator_administration("key_import", context, **kwargs)


def key_export(context: OperationContext, **kwargs: object) -> object:
    return call_operator_administration("key_export", context, **kwargs)


def key_get(context: OperationContext, **kwargs: object) -> object:
    return call_operator_administration("key_get", context, **kwargs)


def key_list(context: OperationContext, **kwargs: object) -> object:
    return call_operator_administration("key_list", context, **kwargs)


def key_rotate(context: OperationContext, **kwargs: object) -> object:
    return call_operator_administration("key_rotate", context, **kwargs)


def key_retire(context: OperationContext, **kwargs: object) -> object:
    return call_operator_administration("key_retire", context, **kwargs)


def key_publish_jwks(context: OperationContext, **kwargs: object) -> object:
    return call_operator_administration("key_publish_jwks", context, **kwargs)


def key_create(context: OperationContext, **kwargs: object) -> object:
    return call_operator_administration("key_create", context, **kwargs)


def key_seed(context: OperationContext, **kwargs: object) -> object:
    return call_operator_administration("key_seed", context, **kwargs)


def key_update(context: OperationContext, **kwargs: object) -> object:
    return call_operator_administration("key_update", context, **kwargs)


def key_delete(context: OperationContext, **kwargs: object) -> object:
    return call_operator_administration("key_delete", context, **kwargs)


def durable_operator_state_root(repo_root: Path) -> Path:
    return operator_state_root(repo_root)


__all__ = [
    "ArtifactResult",
    "OperationContext",
    "OperatorStateError",
    "TransactionResult",
    "authorize_local_operator",
    "build_operator_administration_capability",
    "call_operator_administration",
    "create_resource",
    "delete_resource",
    "durable_operator_state_root",
    "get_resource",
    "key_create",
    "key_delete",
    "key_export",
    "key_generate",
    "key_get",
    "key_import",
    "key_list",
    "key_publish_jwks",
    "key_retire",
    "key_rotate",
    "key_seed",
    "key_update",
    "list_resources",
    "lock_identity",
    "operator_administration_delegates",
    "operator_administration_registry",
    "rotate_client_secret",
    "set_identity_password",
    "toggle_resource",
    "update_resource",
]
