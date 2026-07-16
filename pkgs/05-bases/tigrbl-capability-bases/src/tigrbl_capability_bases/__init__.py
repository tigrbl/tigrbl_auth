from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping

from tigrbl_identity_contracts.capabilities import (
    CapabilityCallContext,
    CapabilityCallable,
    CapabilityCallResult,
    CapabilityDefinition,
    CapabilityOperation,
    CapabilityState,
    ICapability,
)
from tigrbl_security_trust_contracts import CapabilityMap, ICapabilityProvider


class CapabilityBase(ICapability, ABC):
    @abstractmethod
    def definition(self) -> CapabilityDefinition: ...

    @abstractmethod
    def operations(self) -> Mapping[str, CapabilityOperation]: ...

    @abstractmethod
    def attributes(self) -> Mapping[str, object]: ...

    @abstractmethod
    def callables(self) -> Mapping[str, CapabilityCallable]: ...

    @abstractmethod
    def state(self) -> CapabilityState: ...

    @abstractmethod
    async def call(
        self,
        operation: str,
        *args: object,
        context: CapabilityCallContext | None = None,
        **kwargs: object,
    ) -> CapabilityCallResult: ...


class CapabilityProviderBase(ICapabilityProvider, ABC):
    """Base for providers that advertise executable support."""

    @abstractmethod
    def supports(self) -> CapabilityMap: ...

    @abstractmethod
    async def subcall(
        self,
        capability: ICapability,
        operation: str,
        *args: object,
        context: CapabilityCallContext,
        **kwargs: object,
    ) -> CapabilityCallResult: ...


__all__ = ["CapabilityBase", "CapabilityProviderBase"]
