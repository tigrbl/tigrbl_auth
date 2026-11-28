"""Neutral capability execution and protocol-requirement contracts."""

from __future__ import annotations

from collections.abc import Awaitable, Callable, Mapping
from dataclasses import dataclass, field
from typing import Protocol, TypeAlias, runtime_checkable


CapabilityCallable: TypeAlias = Callable[..., object | Awaitable[object]]


class CapabilityError(RuntimeError):
    """Base error for capability definition, resolution, and execution."""


class CapabilityContextError(CapabilityError, ValueError):
    """Raised when a supplied call context conflicts with the target call."""


class CapabilityOperationNotFoundError(CapabilityError, KeyError):
    """Raised when a capability does not declare the requested operation."""


class CapabilityOperationUnavailableError(CapabilityError, LookupError):
    """Raised when an optional operation is declared but not bound."""


class CapabilityDeadlineExceededError(CapabilityError, TimeoutError):
    """Raised when execution begins after the caller's deadline."""


class CapabilityDelegationCycleError(CapabilityError):
    """Raised when a delegated call would revisit a capability."""


@dataclass(frozen=True, slots=True)
class CapabilityDefinition:
    capability_id: str
    version: str


@dataclass(frozen=True, slots=True)
class CapabilityOperation:
    target: CapabilityCallable | None
    required: bool = True
    delegated: bool = False


@dataclass(frozen=True, slots=True)
class CapabilityState:
    ready: bool | None = None
    healthy: bool | None = None
    status: str | None = None
    details: Mapping[str, object] = field(default_factory=dict)


CapabilityStateProvider: TypeAlias = Callable[[], CapabilityState]


@dataclass(frozen=True, slots=True)
class CapabilityCallContext:
    call_id: str
    parent_call_id: str | None = None
    capability_id: str | None = None
    operation: str | None = None
    principal_id: str | None = None
    tenant_id: str | None = None
    authority: tuple[str, ...] = ()
    delegation_chain: tuple[str, ...] = ()
    deadline: float | None = None
    idempotency_key: str | None = None
    trace_id: str | None = None
    correlation_id: str | None = None
    metadata: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class CapabilityCallResult:
    value: object = None
    capability_id: str = ""
    operation: str = ""
    call_id: str = ""
    delegated: bool = False
    context: CapabilityCallContext | None = None


@runtime_checkable
class ICapability(Protocol):
    def definition(self) -> CapabilityDefinition: ...

    def operations(self) -> Mapping[str, CapabilityOperation]: ...

    def attributes(self) -> Mapping[str, object]: ...

    def callables(self) -> Mapping[str, CapabilityCallable]: ...

    def state(self) -> CapabilityState: ...

    def capability_report(self) -> Mapping[str, object]: ...

    async def call(
        self,
        operation: str,
        *args: object,
        context: CapabilityCallContext | None = None,
        **kwargs: object,
    ) -> CapabilityCallResult: ...

    async def subcall(
        self,
        capability: "ICapability",
        operation: str,
        *args: object,
        context: CapabilityCallContext,
        authority: tuple[str, ...] | None = None,
        **kwargs: object,
    ) -> CapabilityCallResult: ...


@dataclass(frozen=True, slots=True)
class ProtocolCapabilityRequirement:
    protocol: str
    revision: str
    requirement_id: str
    wire_element: str
    capability_id: str
    operation: str
    normalized_namespace: str
    required: bool = True


__all__ = [
    "CapabilityCallContext",
    "CapabilityCallable",
    "CapabilityCallResult",
    "CapabilityContextError",
    "CapabilityDeadlineExceededError",
    "CapabilityDefinition",
    "CapabilityDelegationCycleError",
    "CapabilityError",
    "CapabilityOperation",
    "CapabilityOperationNotFoundError",
    "CapabilityOperationUnavailableError",
    "CapabilityState",
    "CapabilityStateProvider",
    "ICapability",
    "ProtocolCapabilityRequirement",
]
