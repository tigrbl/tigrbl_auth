"""Runtime capability indexing, validation, invocation, and reporting."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass

from tigrbl_identity_contracts.capabilities import (
    CapabilityCallContext,
    CapabilityCallResult,
    CapabilityDefinition,
    ICapability,
)


@dataclass(frozen=True, slots=True)
class CapabilityFactory:
    definition: CapabilityDefinition
    operations: tuple[str, ...]
    build: Callable[..., ICapability]

    def __post_init__(self) -> None:
        operations = tuple(sorted(set(self.operations)))
        if not self.definition.capability_id:
            raise ValueError("capability factory requires a capability_id")
        if not operations:
            raise ValueError("capability factory requires at least one operation")
        if not callable(self.build):
            raise TypeError("capability factory build target must be callable")
        object.__setattr__(self, "operations", operations)


class CapabilityRegistry:
    """One effective runtime registry keyed by stable capability ID."""

    def __init__(
        self,
        capabilities: Iterable[ICapability] = (),
        *,
        factories: Iterable[CapabilityFactory] = (),
    ) -> None:
        self._capabilities: dict[str, ICapability] = {}
        self._factories: dict[str, CapabilityFactory] = {}
        for capability in capabilities:
            self.register(capability)
        for factory in factories:
            self.register_factory(factory)

    def _assert_available_id(self, capability_id: str) -> None:
        if capability_id in self._capabilities or capability_id in self._factories:
            raise ValueError(f"duplicate capability_id: {capability_id}")

    def register(self, capability: ICapability) -> None:
        capability_id = capability.definition().capability_id
        if not capability_id:
            raise ValueError("capability_id is required")
        self._assert_available_id(capability_id)
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

    def register_factory(self, factory: CapabilityFactory) -> None:
        capability_id = factory.definition.capability_id
        self._assert_available_id(capability_id)
        self._factories[capability_id] = factory

    def capability_ids(self) -> tuple[str, ...]:
        return tuple(sorted(set(self._capabilities) | set(self._factories)))

    def operation_names(self, capability_id: str) -> tuple[str, ...]:
        if capability_id in self._capabilities:
            return tuple(sorted(self._capabilities[capability_id].callables()))
        try:
            return self._factories[capability_id].operations
        except KeyError as exc:
            raise KeyError(f"unknown capability_id: {capability_id}") from exc

    def resolve(self, capability_id: str) -> ICapability:
        try:
            return self._capabilities[capability_id]
        except KeyError as exc:
            if capability_id in self._factories:
                raise LookupError(
                    f"capability {capability_id} requires request-scoped materialization"
                ) from exc
            raise KeyError(f"unknown capability_id: {capability_id}") from exc

    def materialize(
        self,
        capability_id: str,
        *args: object,
        **kwargs: object,
    ) -> ICapability:
        if capability_id in self._capabilities:
            if args or kwargs:
                raise TypeError(
                    f"singleton capability {capability_id} does not accept factory inputs"
                )
            return self._capabilities[capability_id]
        try:
            factory = self._factories[capability_id]
        except KeyError as exc:
            raise KeyError(f"unknown capability_id: {capability_id}") from exc
        capability = factory.build(*args, **kwargs)
        if not isinstance(capability, ICapability):
            raise TypeError(
                f"factory {capability_id} must return an ICapability implementation"
            )
        if capability.definition() != factory.definition:
            raise ValueError(
                f"factory {capability_id} returned a different capability definition"
            )
        missing = tuple(
            sorted(set(factory.operations) - set(capability.callables()))
        )
        if missing:
            raise NotImplementedError(
                f"factory {capability_id} did not bind declared operations: {missing}"
            )
        return capability

    def require(
        self,
        capability_id: str,
        *,
        operations: Iterable[str] = (),
    ) -> ICapability:
        capability = self.resolve(capability_id)
        missing = tuple(sorted(set(operations) - set(capability.callables())))
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
                capability_id: (
                    dict(self._capabilities[capability_id].capability_report())
                    if capability_id in self._capabilities
                    else {
                        "definition": {
                            "capability_id": capability_id,
                            "version": self._factories[
                                capability_id
                            ].definition.version,
                        },
                        "operations": self._factories[capability_id].operations,
                        "lifetime": "request-scoped",
                        "state": {
                            "ready": None,
                            "healthy": None,
                            "status": "requires-materialization",
                        },
                    }
                )
                for capability_id in capability_ids
            },
        }


__all__ = ["CapabilityFactory", "CapabilityRegistry"]
