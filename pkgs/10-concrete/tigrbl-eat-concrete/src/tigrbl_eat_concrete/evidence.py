from dataclasses import dataclass
from typing import Mapping

from tigrbl_identity_contracts.attestation import AttestationEvidence

from .claims import EatClaimSetPayload


@dataclass(frozen=True, slots=True)
class EatEvidence(AttestationEvidence):
    """EAT specialization of neutral attestation evidence.

    ``raw`` is the protected JWT/CWT serialization. Integrity verification and
    appraisal are deliberately performed by provider layers.
    """

    @classmethod
    def from_payload(
        cls, payload: EatClaimSetPayload, protected_token: bytes | str | None = None
    ) -> "EatEvidence":
        return cls(
            str(payload.profile.identifier),
            dict(payload.raw_claims or {}),
            protected_token,
        )


@dataclass(frozen=True, slots=True)
class DetachedEatBundle:
    detached_claim_sets: Mapping[str, Mapping[str | int, object]]
    integrity_token: bytes | str


def parse_detached_bundle(value: Mapping[str, object]) -> DetachedEatBundle:
    sets, token = value.get("detached_claim_sets"), value.get("integrity_token")
    if (
        not isinstance(sets, Mapping)
        or not sets
        or not all(
            isinstance(name, str) and isinstance(claims, Mapping)
            for name, claims in sets.items()
        )
    ):
        raise ValueError("detached EAT bundle requires named claims sets")
    if not isinstance(token, (bytes, str)) or not token:
        raise ValueError("detached EAT bundle requires an integrity token")
    return DetachedEatBundle(
        {name: dict(claims) for name, claims in sets.items()}, token
    )


__all__ = ["DetachedEatBundle", "EatEvidence", "parse_detached_bundle"]
