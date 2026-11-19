from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True, slots=True)
class CoswidTag:
    tag_id: bytes | str
    software_name: str
    entity: tuple[Mapping[str, object], ...]
    raw: Mapping[str, object]


def parse_coswid(value: Mapping[str, object]) -> CoswidTag:
    tag_id, name, entities = (
        value.get("tag-id"),
        value.get("software-name"),
        value.get("entity", ()),
    )
    if (
        not isinstance(tag_id, (bytes, str))
        or not tag_id
        or not isinstance(name, str)
        or not name
    ):
        raise ValueError("CoSWID requires tag-id and software-name")
    if not isinstance(entities, list) or not all(
        isinstance(item, Mapping) for item in entities
    ):
        raise ValueError("CoSWID entity must be an array")
    return CoswidTag(tag_id, name, tuple(dict(item) for item in entities), dict(value))


__all__ = ["CoswidTag", "parse_coswid"]
