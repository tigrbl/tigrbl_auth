"""Policy-gated operator administration over injected durable operations."""

from __future__ import annotations

import asyncio
import inspect
from collections.abc import Callable, Mapping
from functools import partial
from typing import TypeAlias

from tigrbl_capability import Capability
from tigrbl_identity_contracts.capabilities import (
    CapabilityDefinition,
    CapabilityOperation,
)


OperatorAdministrationOperation: TypeAlias = Callable[..., object]
OperatorAdministrationAuthorizer: TypeAlias = Callable[[str, object], object]

OPERATOR_ADMINISTRATION_OPERATIONS = (
    "create_resource",
    "delete_resource",
    "get_resource",
    "key_delete",
    "key_export",
    "key_generate",
    "key_get",
    "key_import",
    "key_list",
    "key_publish_jwks",
    "key_retire",
    "key_rotate",
    "list_resources",
    "lock_identity",
    "rotate_client_secret",
    "set_identity_password",
    "toggle_resource",
    "update_resource",
)


async def _resolve(value: object) -> object:
    return await value if inspect.isawaitable(value) else value


class OperatorAdministrationCapability(Capability):
    """Authorize and delegate operator-plane mutations and durable reads."""

    def __init__(
        self,
        *,
        authorize: OperatorAdministrationAuthorizer,
        delegates: Mapping[str, OperatorAdministrationOperation],
    ) -> None:
        if not callable(authorize):
            raise TypeError("operator administration authorizer must be callable")
        missing = tuple(
            sorted(set(OPERATOR_ADMINISTRATION_OPERATIONS) - set(delegates))
        )
        extra = tuple(sorted(set(delegates) - set(OPERATOR_ADMINISTRATION_OPERATIONS)))
        if missing:
            raise NotImplementedError(
                f"required operator administration operations are missing: {missing}"
            )
        if extra:
            raise ValueError(f"unknown operator administration operations: {extra}")
        invalid = tuple(
            sorted(name for name, target in delegates.items() if not callable(target))
        )
        if invalid:
            raise TypeError(
                f"operator administration delegates must be callable: {invalid}"
            )

        self._authorize = authorize
        self._delegates = dict(delegates)
        super().__init__(
            CapabilityDefinition("identity-admin.operator", "1.0"),
            operations={
                name: CapabilityOperation(
                    target=partial(self._invoke, name),
                    delegated=True,
                )
                for name in OPERATOR_ADMINISTRATION_OPERATIONS
            },
        )

    async def _invoke(
        self,
        operation: str,
        operation_context: object,
        /,
        **kwargs: object,
    ) -> object:
        await _resolve(self._authorize(operation, operation_context))
        delegate = self._delegates[operation]
        if inspect.iscoroutinefunction(delegate):
            return await _resolve(delegate(operation_context, **kwargs))
        value = await asyncio.to_thread(delegate, operation_context, **kwargs)
        return await _resolve(value)


__all__ = [
    "OPERATOR_ADMINISTRATION_OPERATIONS",
    "OperatorAdministrationAuthorizer",
    "OperatorAdministrationCapability",
    "OperatorAdministrationOperation",
]
