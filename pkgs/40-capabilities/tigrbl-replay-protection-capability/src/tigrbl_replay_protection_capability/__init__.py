"""Composable replay-protection capability and reporting."""

from __future__ import annotations

from typing import NamedTuple

from tigrbl_capability import Capability
from tigrbl_identity_contracts.capabilities import (
    CapabilityDefinition,
    CapabilityOperation,
    CapabilityState,
)
from tigrbl_identity_contracts.replay import (
    ReplayReservationPort,
    ReplayReservationRequest,
    ReplayReservationResult,
)


class ReplayCapabilityDescriptor(NamedTuple):
    namespaces: tuple[str, ...] = ()
    provider_id: str = ""
    persistence: str = "unknown"


class ReplayProtectionCapability(Capability):
    capability_id = "security.replay-protection"
    version = "1.0"

    def __init__(
        self,
        provider: ReplayReservationPort,
        /,
        *,
        namespaces: tuple[str, ...] = (),
    ) -> None:
        self._provider = provider
        self._namespaces = tuple(sorted(set(namespaces)))
        super().__init__(
            CapabilityDefinition(
                capability_id=self.capability_id,
                version=self.version,
            ),
            operations={
                "check_and_reserve": CapabilityOperation(
                    target=self.check_and_reserve,
                    delegated=True,
                ),
            },
            state=self._state,
        )

    def _state(self) -> CapabilityState:
        return CapabilityState(
            ready=bool(getattr(self._provider, "ready", True)),
            healthy=bool(getattr(self._provider, "healthy", True)),
            status=str(getattr(self._provider, "status", "ready")),
        )

    async def check_and_reserve(
        self, request: ReplayReservationRequest, /
    ) -> ReplayReservationResult:
        if self._namespaces and request.key.namespace not in self._namespaces:
            raise ValueError(f"unsupported replay namespace: {request.key.namespace}")
        return await self._provider.check_and_reserve(request)

    def describe(self) -> ReplayCapabilityDescriptor:
        persistence = str(getattr(self._provider, "persistence", "unknown"))
        return ReplayCapabilityDescriptor(
            namespaces=self._namespaces,
            provider_id=str(getattr(self._provider, "provider_id", type(self._provider).__name__)),
            persistence=persistence,
        )

    def capability_report(self) -> dict[str, object]:
        report = super().capability_report()
        report.update(self.describe()._asdict())
        return report


__all__ = ["ReplayCapabilityDescriptor", "ReplayProtectionCapability"]
