from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True, slots=True)
class SdJwtVcStatusReference:
    mechanism: str
    index: int | None = None
    uri: str | None = None


def parse_status_reference(value: Mapping[str, object]) -> SdJwtVcStatusReference:
    if len(value) != 1:
        raise ValueError("status must select exactly one status mechanism")
    mechanism, details = next(iter(value.items()))
    if not isinstance(details, Mapping):
        raise ValueError("status mechanism details must be an object")
    index, uri = details.get("idx"), details.get("uri")
    if index is not None and (
        not isinstance(index, int) or isinstance(index, bool) or index < 0
    ):
        raise ValueError("status index must be a non-negative integer")
    if uri is not None and (not isinstance(uri, str) or not uri):
        raise ValueError("status URI must be a non-empty string")
    return SdJwtVcStatusReference(mechanism, index, uri)


__all__ = ["SdJwtVcStatusReference", "parse_status_reference"]
