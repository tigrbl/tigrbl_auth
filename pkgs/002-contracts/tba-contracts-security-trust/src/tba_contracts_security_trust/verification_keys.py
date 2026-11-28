from dataclasses import dataclass
from typing import Mapping, Protocol, Sequence


@dataclass(frozen=True, slots=True)
class VerificationKey:
    key_id: str
    algorithm: str
    material: Mapping[str, object] | bytes


class VerificationKeyResolverPort(Protocol):
    def resolve(
        self, issuer: str, key_id: str | None, /
    ) -> Sequence[VerificationKey]: ...


__all__ = ["VerificationKey", "VerificationKeyResolverPort"]
