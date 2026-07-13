"""Neutral capability execution and protocol-requirement contracts."""

from __future__ import annotations

from collections.abc import Awaitable, Callable, Mapping
from dataclasses import dataclass, field
from typing import Protocol, TypeAlias, runtime_checkable


@dataclass(frozen=True, slots=True)
class CapabilityMetadata:
    capability_id: str
    version: str
    operations: tuple[str, ...]
    guarantees: tuple[str, ...] = ()
    optional_features: tuple[str, ...] = ()
    required_capabilities: tuple[str, ...] = ()
    dependencies: tuple[str, ...] = ()
    namespaces: tuple[str, ...] = ()
    persistence: str | None = None
    ready: bool | None = None
    healthy: bool | None = None
    limitations: tuple[str, ...] = ()
    unsupported: tuple[str, ...] = ()
    implementation: str = "generic"
    effective_defaults: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class CapabilityState:
    ready: bool | None = None
    healthy: bool | None = None
    status: str | None = None
    details: Mapping[str, object] = field(default_factory=dict)


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


CapabilityCallable: TypeAlias = Callable[..., object | Awaitable[object]]


@runtime_checkable
class ICapability(Protocol):
    def emit_capability_metadata(self) -> CapabilityMetadata: ...

    def attributes(self) -> Mapping[str, object]: ...

    def callables(self) -> Mapping[str, CapabilityCallable]: ...

    def state(self) -> CapabilityState: ...

    def bind(
        self, operation: str, target: CapabilityCallable, *, delegated: bool = False
    ) -> None: ...

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
    "CapabilityMetadata",
    "CapabilityState",
    "ICapability",
    "ProtocolCapabilityRequirement",
]
