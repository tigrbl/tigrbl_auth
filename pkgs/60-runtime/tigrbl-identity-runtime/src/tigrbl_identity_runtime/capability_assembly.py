"""Ordered runtime assembly and protocol-to-capability validation."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from typing import TypeAlias

from tigrbl_identity_contracts.capabilities import (
    ICapability,
    ProtocolCapabilityRequirement,
)

from .capability_registry import CapabilityRegistry


ProviderSet: TypeAlias = Mapping[str, object]
StorageRuntimeSet: TypeAlias = Mapping[str, object]
ProtocolReport: TypeAlias = Mapping[str, object]
ProviderBuilder: TypeAlias = Callable[[], ProviderSet]
StorageRuntimeBuilder: TypeAlias = Callable[[ProviderSet], StorageRuntimeSet]
CapabilityBuilder: TypeAlias = Callable[
    [ProviderSet, StorageRuntimeSet],
    Iterable[ICapability] | CapabilityRegistry,
]
ProtocolBuilder: TypeAlias = Callable[
    [CapabilityRegistry], Iterable[ProtocolReport]
]


class ProtocolCapabilityBindingError(RuntimeError):
    """Raised when a selected protocol has no executable capability target."""


@dataclass(frozen=True, slots=True)
class RuntimeCapabilityAssembly:
    providers: ProviderSet
    storage_runtime: StorageRuntimeSet
    capabilities: CapabilityRegistry
    protocols: tuple[ProtocolReport, ...]
    construction_order: tuple[str, ...]

    def report(self) -> dict[str, object]:
        return {
            "construction_order": self.construction_order,
            "provider_ids": tuple(sorted(self.providers)),
            "storage_runtime_ids": tuple(sorted(self.storage_runtime)),
            "capabilities": self.capabilities.report(),
            "protocols": self.protocols,
        }


def _requirements(
    reports: Iterable[ProtocolReport],
) -> tuple[ProtocolCapabilityRequirement, ...]:
    requirements: list[ProtocolCapabilityRequirement] = []
    for report in reports:
        values = report.get("requirements", ())
        if not isinstance(values, (tuple, list)):
            raise TypeError("protocol report requirements must be a sequence")
        for value in values:
            if not isinstance(value, ProtocolCapabilityRequirement):
                raise TypeError(
                    "protocol requirements must be ProtocolCapabilityRequirement objects"
                )
            requirements.append(value)
    return tuple(requirements)


def validate_protocol_capabilities(
    registry: CapabilityRegistry,
    reports: Iterable[ProtocolReport],
) -> None:
    failures: list[str] = []
    for requirement in _requirements(reports):
        try:
            operations = registry.operation_names(requirement.capability_id)
        except KeyError:
            if requirement.required:
                failures.append(
                    f"{requirement.protocol}@{requirement.revision}: "
                    f"{requirement.requirement_id} requires missing capability "
                    f"{requirement.capability_id}"
                )
            continue
        if requirement.operation not in operations:
            failures.append(
                f"{requirement.protocol}@{requirement.revision}: "
                f"{requirement.requirement_id} requires unavailable operation "
                f"{requirement.capability_id}.{requirement.operation}"
            )
    if failures:
        raise ProtocolCapabilityBindingError("; ".join(failures))


def build_runtime_capability_assembly(
    *,
    build_providers: ProviderBuilder,
    build_storage_runtime: StorageRuntimeBuilder,
    build_capabilities: CapabilityBuilder,
    build_protocols: ProtocolBuilder,
) -> RuntimeCapabilityAssembly:
    construction_order: list[str] = []

    providers = dict(build_providers())
    construction_order.append("providers")

    storage_runtime = dict(build_storage_runtime(providers))
    construction_order.append("storage-runtime")

    capabilities = build_capabilities(providers, storage_runtime)
    registry = (
        capabilities
        if isinstance(capabilities, CapabilityRegistry)
        else CapabilityRegistry(capabilities)
    )
    construction_order.append("capabilities")

    protocols = tuple(build_protocols(registry))
    construction_order.append("protocols")
    validate_protocol_capabilities(registry, protocols)

    return RuntimeCapabilityAssembly(
        providers=providers,
        storage_runtime=storage_runtime,
        capabilities=registry,
        protocols=protocols,
        construction_order=tuple(construction_order),
    )


__all__ = [
    "CapabilityBuilder",
    "ProtocolBuilder",
    "ProtocolCapabilityBindingError",
    "ProtocolReport",
    "ProviderBuilder",
    "ProviderSet",
    "RuntimeCapabilityAssembly",
    "StorageRuntimeBuilder",
    "StorageRuntimeSet",
    "build_runtime_capability_assembly",
    "validate_protocol_capabilities",
]
