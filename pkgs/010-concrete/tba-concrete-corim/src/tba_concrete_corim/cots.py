from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True, slots=True)
class ConciseTrustStore:
    tag_identity: str | bytes
    stores: tuple[Mapping[str, object], ...]


def parse_cots(value: Mapping[str, object]) -> ConciseTrustStore:
    identity, stores = value.get("tag-identity"), value.get("trust-store", ())
    if (
        not isinstance(identity, (str, bytes))
        or not identity
        or not isinstance(stores, list)
        or not all(isinstance(item, Mapping) for item in stores)
    ):
        raise ValueError("CoTS requires tag-identity and trust-store entries")
    return ConciseTrustStore(identity, tuple(dict(item) for item in stores))


__all__ = ["ConciseTrustStore", "parse_cots"]
