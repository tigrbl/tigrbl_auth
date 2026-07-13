from __future__ import annotations

import inspect
import time
from collections.abc import Mapping
from dataclasses import asdict, replace

from tigrbl_capability_bases import CapabilityBase
from tigrbl_identity_core.clock import utc_now_iso
from tigrbl_identity_core.primitives import new_opaque_id, new_prefixed_id
from tigrbl_identity_contracts.capabilities import (
    CapabilityCallContext,
    CapabilityCallable,
    CapabilityCallResult,
    CapabilityDefinition,
    CapabilityOperation,
    CapabilityState,
    CapabilityStateProvider,
    ICapability,
)


class Capability(CapabilityBase):
    """Neutral generic capability with only explicitly supplied configuration."""

    def __init__(
        self,
        definition: CapabilityDefinition,
        /,
        *,
        operations: Mapping[str, CapabilityOperation],
        attributes: Mapping[str, object] | None = None,
        state: CapabilityState | CapabilityStateProvider | None = None,
    ) -> None:
        if not definition.capability_id.strip():
            raise ValueError("capability_id is required")
        if not definition.version.strip():
            raise ValueError("capability version is required")
        if not operations:
            raise ValueError("at least one capability operation is required")
        normalized_operations: dict[str, CapabilityOperation] = {}
        for name, operation in operations.items():
            if not name.strip():
                raise ValueError("capability operation name is required")
            if not isinstance(operation, CapabilityOperation):
                raise TypeError(f"invalid capability operation: {name}")
            if operation.target is not None and not callable(operation.target):
                raise TypeError(f"capability operation target must be callable: {name}")
            if operation.required and operation.target is None:
                raise NotImplementedError(
                    f"required capability operation is not implemented: {name}"
                )
            normalized_operations[name] = operation
        self._capability_definition = definition
        self._capability_operations = normalized_operations
        self._capability_attributes = dict(attributes or {})
        if state is None:
            self._capability_state_provider: CapabilityStateProvider = CapabilityState
        elif isinstance(state, CapabilityState):
            self._capability_state_provider = lambda state=state: state
        elif callable(state):
            self._capability_state_provider = state
        else:
            raise TypeError("capability state must be a CapabilityState or state provider")

    def definition(self) -> CapabilityDefinition:
        return self._capability_definition

    def operations(self) -> Mapping[str, CapabilityOperation]:
        return dict(self._capability_operations)

    def attributes(self) -> Mapping[str, object]:
        return dict(self._capability_attributes)

    def callables(self) -> Mapping[str, CapabilityCallable]:
        return {
            name: operation.target
            for name, operation in self._capability_operations.items()
            if operation.target is not None
        }

    def state(self) -> CapabilityState:
        state = self._capability_state_provider()
        if not isinstance(state, CapabilityState):
            raise TypeError("capability state provider must return CapabilityState")
        return state

    def capability_report(self) -> dict[str, object]:
        """Return the complete, operator-inspectable effective capability set."""
        report: dict[str, object] = dict(asdict(self._capability_definition))
        report["operations"] = tuple(self._capability_operations)
        report["bound_operations"] = tuple(sorted(self.callables()))
        report["delegated_operations"] = tuple(
            sorted(
                name
                for name, operation in self._capability_operations.items()
                if operation.target is not None and operation.delegated
            )
        )
        report["optional_operations"] = tuple(
            sorted(
                name
                for name, operation in self._capability_operations.items()
                if not operation.required
            )
        )
        report["unavailable_optional_operations"] = tuple(
            sorted(
                name
                for name, operation in self._capability_operations.items()
                if not operation.required and operation.target is None
            )
        )
        report["state"] = asdict(self.state())
        return report

    async def call(
        self,
        operation: str,
        *args: object,
        context: CapabilityCallContext | None = None,
        **kwargs: object,
    ) -> CapabilityCallResult:
        try:
            operation_definition = self._capability_operations[operation]
        except KeyError as exc:
            raise KeyError(f"unknown capability operation: {operation}") from exc
        target = operation_definition.target
        if target is None:
            raise LookupError(f"unbound optional capability operation: {operation}")
        active = context or CapabilityCallContext(call_id=new_opaque_id())
        if active.deadline is not None and time.time() > active.deadline:
            raise TimeoutError("capability call deadline exceeded")
        value = target(*args, **kwargs)
        if inspect.isawaitable(value):
            value = await value
        return CapabilityCallResult(
            value=value,
            capability_id=self._capability_definition.capability_id,
            operation=operation,
            call_id=active.call_id,
            delegated=operation_definition.delegated,
        )

    async def subcall(
        self,
        capability: ICapability,
        operation: str,
        *args: object,
        context: CapabilityCallContext,
        **kwargs: object,
    ) -> CapabilityCallResult:
        target_capability_id = capability.definition().capability_id
        delegation_chain = context.delegation_chain + (
            self._capability_definition.capability_id,
        )
        if target_capability_id in delegation_chain:
            raise RuntimeError("capability delegation cycle detected")
        child = replace(
            context,
            parent_call_id=context.call_id,
            call_id=new_opaque_id(),
            capability_id=target_capability_id,
            operation=operation,
            delegation_chain=delegation_chain,
        )
        return await capability.call(operation, *args, context=child, **kwargs)


__all__ = ["Capability", "new_prefixed_id", "utc_now_iso"]
