import base64
import json
from dataclasses import dataclass
from typing import Mapping


def _decode_object(segment: str) -> Mapping[str, object]:
    try:
        value = json.loads(
            base64.urlsafe_b64decode(segment + "=" * (-len(segment) % 4))
        )
    except (ValueError, UnicodeDecodeError) as exc:
        raise ValueError("invalid base64url JSON segment") from exc
    if not isinstance(value, dict):
        raise ValueError("JOSE JSON segment must be an object")
    return value


@dataclass(frozen=True, slots=True)
class CompactJose:
    protected: Mapping[str, object]
    payload_segment: str
    integrity_segment: str
    segment_count: int


def parse_compact_jose(value: str) -> CompactJose:
    parts = value.split(".")
    if len(parts) not in (3, 5) or not all(parts):
        raise ValueError("compact JOSE must contain three JWS or five JWE segments")
    return CompactJose(_decode_object(parts[0]), parts[1], parts[-1], len(parts))


__all__ = ["CompactJose", "parse_compact_jose"]
