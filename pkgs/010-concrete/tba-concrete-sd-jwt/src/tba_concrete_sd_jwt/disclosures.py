import base64
import json
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Disclosure:
    salt: str
    claim_name: str | None
    value: object


def encode_disclosure(disclosure: Disclosure) -> str:
    value = (
        [disclosure.salt, disclosure.value]
        if disclosure.claim_name is None
        else [disclosure.salt, disclosure.claim_name, disclosure.value]
    )
    raw = json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode()
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def decode_disclosure(encoded: str) -> Disclosure:
    try:
        value = json.loads(
            base64.urlsafe_b64decode(encoded + "=" * (-len(encoded) % 4))
        )
    except (ValueError, UnicodeDecodeError) as exc:
        raise ValueError("invalid SD-JWT disclosure") from exc
    if (
        not isinstance(value, list)
        or len(value) not in (2, 3)
        or not isinstance(value[0], str)
        or not value[0]
    ):
        raise ValueError("disclosure must contain salt, optional claim name, and value")
    if len(value) == 2:
        return Disclosure(value[0], None, value[1])
    if not isinstance(value[1], str) or not value[1]:
        raise ValueError("object-property disclosure requires a claim name")
    return Disclosure(value[0], value[1], value[2])


__all__ = ["Disclosure", "decode_disclosure", "encode_disclosure"]
