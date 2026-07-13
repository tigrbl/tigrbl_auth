from __future__ import annotations

import inspect
import time
from collections.abc import Mapping
from dataclasses import replace
from uuid import uuid4

from tigrbl_capability_bases import CapabilityBase
from tigrbl_identity_contracts.capabilities import (
    CapabilityCallContext,
    CapabilityCallable,
    CapabilityCallResult,
    CapabilityMetadata,
    CapabilityState,
    ICapability,
)


class Capability(CapabilityBase):
    """Neutral generic capability with only explicitly supplied configuration."""

    def __init__(
        self,
        metadata: CapabilityMetadata,
        /,
        *,
        attributes: Mapping[str, object] | None = None,
        state: CapabilityState | None = None,
    ) -> None:
        if not metadata.capability_id.strip():
            raise ValueError("capability_id is required")
        if not metadata.version.strip():
            raise ValueError("capability version is required")
        if not metadata.operations:
            raise ValueError("at least one capability operation is required")
        if len(set(metadata.operations)) != len(metadata.operations):
            raise ValueError("capability operations must be unique")
        self._capability_metadata = metadata
        self._capability_attributes = dict(attributes or {})
        self._capability_state = state if state is not None else CapabilityState()
        self._capability_bindings: dict[str, tuple[CapabilityCallable, bool]] = {}

    def emit_capability_metadata(self) -> CapabilityMetadata:
        return self._capability_metadata

    def attributes(self) -> Mapping[str, object]:
        return dict(self._capability_attributes)

    def callables(self) -> Mapping[str, CapabilityCallable]:
        return {
            name: binding[0] for name, binding in self._capability_bindings.items()
        }

    def state(self) -> CapabilityState:
        return self._capability_state

    def bind(
        self, operation: str, target: CapabilityCallable, *, delegated: bool = False
    ) -> None:
        if operation not in self._capability_metadata.operations:
            raise KeyError(f"undeclared capability operation: {operation}")
        if not callable(target):
            raise TypeError("capability binding target must be callable")
        self._capability_bindings[operation] = (target, delegated)

    async def call(
        self,
        operation: str,
        *args: object,
        context: CapabilityCallContext | None = None,
        **kwargs: object,
    ) -> CapabilityCallResult:
        try:
            target, delegated = self._capability_bindings[operation]
        except KeyError as exc:
            raise LookupError(f"unbound capability operation: {operation}") from exc
        active = context or CapabilityCallContext(call_id=uuid4().hex)
        if active.deadline is not None and time.time() > active.deadline:
            raise TimeoutError("capability call deadline exceeded")
        value = target(*args, **kwargs)
        if inspect.isawaitable(value):
            value = await value
        return CapabilityCallResult(
            value=value,
            capability_id=self._capability_metadata.capability_id,
            operation=operation,
            call_id=active.call_id,
            delegated=delegated,
        )

    async def subcall(
        self,
        capability: ICapability,
        operation: str,
        *args: object,
        context: CapabilityCallContext,
        **kwargs: object,
    ) -> CapabilityCallResult:
        child = replace(
            context,
            parent_call_id=context.call_id,
            call_id=uuid4().hex,
            capability_id=capability.emit_capability_metadata().capability_id,
            operation=operation,
        )
        return await capability.call(operation, *args, context=child, **kwargs)


__all__ = ["Capability"]
