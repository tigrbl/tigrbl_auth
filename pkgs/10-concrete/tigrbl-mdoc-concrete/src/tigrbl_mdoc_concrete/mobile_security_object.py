from dataclasses import dataclass
from datetime import datetime
from typing import Mapping


@dataclass(frozen=True, slots=True)
class ValidityInfo:
    signed: datetime
    valid_from: datetime
    valid_until: datetime
    expected_update: datetime | None = None

    def __post_init__(self):
        if not self.signed <= self.valid_from <= self.valid_until:
            raise ValueError("MSO validity times are not ordered")


@dataclass(frozen=True, slots=True)
class MobileSecurityObject:
    version: str
    digest_algorithm: str
    value_digests: Mapping[str, Mapping[int, bytes]]
    device_key_info: Mapping[str, object]
    doc_type: str
    validity_info: ValidityInfo


def _time(value: object, name: str) -> datetime:
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError(f"invalid {name}") from exc
    raise ValueError(f"{name} must be a datetime")


def parse_mobile_security_object(value: Mapping[str, object]) -> MobileSecurityObject:
    version, algorithm, doc_type = (
        value.get("version"),
        value.get("digestAlgorithm"),
        value.get("docType"),
    )
    digests, key_info, validity = (
        value.get("valueDigests"),
        value.get("deviceKeyInfo"),
        value.get("validityInfo"),
    )
    if not all(
        isinstance(item, str) and item for item in (version, algorithm, doc_type)
    ):
        raise ValueError("MSO requires version, digestAlgorithm, and docType")
    if (
        not isinstance(digests, Mapping)
        or not isinstance(key_info, Mapping)
        or not isinstance(validity, Mapping)
    ):
        raise ValueError("MSO requires valueDigests, deviceKeyInfo, and validityInfo")
    normalized = {}
    for namespace, entries in digests.items():
        if not isinstance(namespace, str) or not isinstance(entries, Mapping):
            raise ValueError("valueDigests must map namespaces to digest maps")
        if any(
            not isinstance(index, int) or not isinstance(digest, bytes)
            for index, digest in entries.items()
        ):
            raise ValueError("value digest entries must map integers to bytes")
        normalized[namespace] = dict(entries)
    validity_info = ValidityInfo(
        _time(validity.get("signed"), "signed"),
        _time(validity.get("validFrom"), "validFrom"),
        _time(validity.get("validUntil"), "validUntil"),
        _time(validity["expectedUpdate"], "expectedUpdate")
        if "expectedUpdate" in validity
        else None,
    )
    return MobileSecurityObject(
        version, algorithm, normalized, dict(key_info), doc_type, validity_info
    )


__all__ = ["MobileSecurityObject", "ValidityInfo", "parse_mobile_security_object"]
