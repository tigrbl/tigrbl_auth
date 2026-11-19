from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True, slots=True)
class ConciseTrustList:
    tag_identity: str | bytes
    entries: tuple[Mapping[str, object], ...]


def parse_cotl(value: Mapping[str, object]) -> ConciseTrustList:
    identity, entries = value.get("tag-identity"), value.get("trust-list", ())
    if (
        not isinstance(identity, (str, bytes))
        or not identity
        or not isinstance(entries, list)
        or not all(isinstance(item, Mapping) for item in entries)
    ):
        raise ValueError("CoTL requires tag-identity and trust-list entries")
    return ConciseTrustList(identity, tuple(dict(item) for item in entries))


__all__ = ["ConciseTrustList", "parse_cotl"]
