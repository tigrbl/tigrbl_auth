"""Protocol-neutral replay reservation bases."""

from abc import ABC
from hashlib import sha256

from tigrbl_replay_contracts import (
    ReplayKey,
    ReplayReservationPort,
    ReplayReservationRequest,
    ReplayReservationResult,
)


class ReplayReservationBase(ReplayReservationPort, ABC):
    provider_id = "replay:abstract"

    @staticmethod
    def digest_key(key: ReplayKey) -> str:
        material = "\x1f".join(
            (key.namespace, key.tenant_id or "", key.issuer or "", key.value)
        ).encode("utf-8")
        return sha256(material).hexdigest()

    async def check_and_reserve(
        self, request: ReplayReservationRequest, /
    ) -> ReplayReservationResult:
        raise NotImplementedError


__all__ = ["ReplayReservationBase"]
