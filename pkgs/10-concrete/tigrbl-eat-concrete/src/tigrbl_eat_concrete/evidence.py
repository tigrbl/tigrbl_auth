from dataclasses import dataclass
from typing import Mapping

from tigrbl_eat_evidence_concrete import EatEvidence

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
