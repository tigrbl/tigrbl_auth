from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping

from tigrbl_identity_contracts.capabilities import (
    CapabilityCallContext,
    CapabilityCallable,
    CapabilityCallResult,
    CapabilityMetadata,
    CapabilityState,
    ICapability,
)


class CapabilityBase(ICapability, ABC):
    @abstractmethod
    def emit_capability_metadata(self) -> CapabilityMetadata: ...

    @abstractmethod
    def attributes(self) -> Mapping[str, object]: ...

    @abstractmethod
    def callables(self) -> Mapping[str, CapabilityCallable]: ...

    @abstractmethod
    def state(self) -> CapabilityState: ...

    @abstractmethod
    def bind(
        self, operation: str, target: CapabilityCallable, *, delegated: bool = False
    ) -> None: ...

    @abstractmethod
    async def call(
        self,
        operation: str,
        *args: object,
        context: CapabilityCallContext | None = None,
        **kwargs: object,
    ) -> CapabilityCallResult: ...

    @abstractmethod
    async def subcall(
        self,
        capability: ICapability,
        operation: str,
        *args: object,
        context: CapabilityCallContext,
        **kwargs: object,
    ) -> CapabilityCallResult: ...


__all__ = ["CapabilityBase"]
