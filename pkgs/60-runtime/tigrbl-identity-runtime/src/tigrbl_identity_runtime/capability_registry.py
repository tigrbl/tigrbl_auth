"""Runtime capability indexing, validation, invocation, and reporting."""

from __future__ import annotations

from collections.abc import Iterable, Mapping

from tigrbl_identity_contracts.capabilities import (
    CapabilityCallContext,
    CapabilityCallResult,
    ICapability,
)


class CapabilityRegistry:
    """One effective runtime registry keyed by stable capability ID."""

    def __init__(self, capabilities: Iterable[ICapability] = ()) -> None:
        self._capabilities: dict[str, ICapability] = {}
        for capability in capabilities:
            self.register(capability)

    def register(self, capability: ICapability) -> None:
        capability_id = capability.definition().capability_id
        if not capability_id:
            raise ValueError("capability_id is required")
        if capability_id in self._capabilities:
            raise ValueError(f"duplicate capability_id: {capability_id}")
        missing = tuple(
            name
            for name, operation in capability.operations().items()
            if operation.required and operation.target is None
        )
        if missing:
            raise NotImplementedError(
                f"required capability operations are not implemented: {missing}"
            )
        self._capabilities[capability_id] = capability

    def capability_ids(self) -> tuple[str, ...]:
        return tuple(sorted(self._capabilities))

    def resolve(self, capability_id: str) -> ICapability:
        try:
            return self._capabilities[capability_id]
        except KeyError as exc:
            raise KeyError(f"unknown capability_id: {capability_id}") from exc

    def require(
        self,
        capability_id: str,
        *,
        operations: Iterable[str] = (),
    ) -> ICapability:
        capability = self.resolve(capability_id)
        missing = tuple(
            sorted(set(operations) - set(capability.callables()))
        )
        if missing:
            raise LookupError(
                f"capability {capability_id} has unavailable operations: {missing}"
            )
        return capability

    async def call(
        self,
        capability_id: str,
        operation: str,
        *args: object,
        context: CapabilityCallContext | None = None,
        **kwargs: object,
    ) -> CapabilityCallResult:
        capability = self.require(capability_id, operations=(operation,))
        return await capability.call(
            operation,
            *args,
            context=context,
            **kwargs,
        )

    def report(self) -> Mapping[str, object]:
        capability_ids = self.capability_ids()
        return {
            "capability_ids": capability_ids,
            "capabilities": {
                capability_id: dict(
                    self._capabilities[capability_id].capability_report()
                )
                for capability_id in capability_ids
            },
        }


__all__ = ["CapabilityRegistry"]
