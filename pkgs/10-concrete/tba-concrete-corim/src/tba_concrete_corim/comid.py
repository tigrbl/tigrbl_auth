from dataclasses import dataclass
from typing import Mapping, Sequence


@dataclass(frozen=True, slots=True)
class ComidTag:
    tag_identity: str | bytes
    entities: Sequence[Mapping[str, object]]
    triples: Mapping[str, Sequence[Mapping[str, object]]]


def parse_comid(value: Mapping[str, object]) -> ComidTag:
    identity, entities, triples = (
        value.get("tag-identity"),
        value.get("entities", ()),
        value.get("triples", {}),
    )
    if not isinstance(identity, (str, bytes)) or not identity:
        raise ValueError("CoMID requires tag-identity")
    if not isinstance(entities, list) or not all(
        isinstance(item, Mapping) for item in entities
    ):
        raise ValueError("CoMID entities must be an array of objects")
    if not isinstance(triples, Mapping) or any(
        not isinstance(name, str)
        or not isinstance(items, list)
        or not all(isinstance(item, Mapping) for item in items)
        for name, items in triples.items()
    ):
        raise ValueError("CoMID triples must map relationship names to arrays")
    return ComidTag(
        identity,
        tuple(dict(item) for item in entities),
        {name: tuple(dict(item) for item in items) for name, items in triples.items()},
    )


__all__ = ["ComidTag", "parse_comid"]
