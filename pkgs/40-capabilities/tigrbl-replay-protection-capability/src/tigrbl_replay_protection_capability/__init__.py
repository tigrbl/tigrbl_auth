"""Composable replay-protection capability and reporting."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from tigrbl_capability import Capability
from tigrbl_identity_contracts.capabilities import CapabilityMetadata
from tigrbl_identity_contracts.replay import (
    ReplayReservationPort,
    ReplayReservationRequest,
    ReplayReservationResult,
)


@dataclass(frozen=True, slots=True)
class ReplayCapabilityDescriptor:
    capability_id: str = "security.replay-protection"
    version: str = "1.0"
    operations: tuple[str, ...] = ("check_and_reserve",)
    guarantees: tuple[str, ...] = ("atomic-reservation", "expiry")
    namespaces: tuple[str, ...] = ()
    provider_id: str = ""
    persistence: str = "unknown"
    ready: bool = True
    healthy: bool = True
    limitations: tuple[str, ...] = ()


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
        persistence = str(getattr(provider, "persistence", "unknown"))
        limitations = (
            ("state-lost-on-restart", "not-shared-across-workers")
            if persistence == "ephemeral-process-local"
            else ()
        )
        super().__init__(
            CapabilityMetadata(
                capability_id=self.capability_id,
                version=self.version,
                operations=("check_and_reserve",),
                guarantees=("atomic-reservation", "expiry"),
                namespaces=self._namespaces,
                dependencies=(
                    str(getattr(provider, "provider_id", type(provider).__name__)),
                ),
                persistence=persistence,
                ready=True,
                healthy=True,
                limitations=limitations,
            )
        )
        self.bind("check_and_reserve", self.check_and_reserve, delegated=True)

    async def check_and_reserve(
        self, request: ReplayReservationRequest, /
    ) -> ReplayReservationResult:
        if self._namespaces and request.key.namespace not in self._namespaces:
            raise ValueError(f"unsupported replay namespace: {request.key.namespace}")
        return await self._provider.check_and_reserve(request)

    def describe(self) -> ReplayCapabilityDescriptor:
        persistence = str(getattr(self._provider, "persistence", "unknown"))
        limitations = (
            ("state-lost-on-restart", "not-shared-across-workers")
            if persistence == "ephemeral-process-local"
            else ()
        )
        return ReplayCapabilityDescriptor(
            namespaces=self._namespaces,
            provider_id=str(getattr(self._provider, "provider_id", type(self._provider).__name__)),
            persistence=persistence,
            limitations=limitations,
        )

    def capability_report(self) -> dict[str, object]:
        return asdict(self.describe())


__all__ = ["ReplayCapabilityDescriptor", "ReplayProtectionCapability"]
