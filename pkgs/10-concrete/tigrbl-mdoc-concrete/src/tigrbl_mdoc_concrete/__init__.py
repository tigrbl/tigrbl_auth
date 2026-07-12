"""Standalone ISO mdoc structural concrete."""

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class Mdoc:
    doc_type: str
    name_spaces: Mapping[str, tuple[Mapping[str, Any], ...]]
    issuer_auth: bytes
    device_signed: Mapping[str, Any] | None = None


def parse_mdoc(value: Mapping[str, Any]) -> Mdoc:
    doc_type = value.get("docType")
    issuer_signed = value.get("issuerSigned")
    if not isinstance(doc_type, str) or not doc_type:
        raise ValueError("mdoc requires docType")
    if not isinstance(issuer_signed, Mapping):
        raise ValueError("mdoc requires issuerSigned")
    namespaces = issuer_signed.get("nameSpaces", {})
    issuer_auth = issuer_signed.get("issuerAuth")
    if not isinstance(namespaces, Mapping) or not isinstance(issuer_auth, bytes):
        raise ValueError("issuerSigned requires nameSpaces and byte-valued issuerAuth")
    normalized = {}
    for name, items in namespaces.items():
        if (
            not isinstance(name, str)
            or not isinstance(items, (list, tuple))
            or not all(isinstance(i, Mapping) for i in items)
        ):
            raise ValueError(
                "mdoc namespaces must map strings to issuer-signed item arrays"
            )
        normalized[name] = tuple(dict(i) for i in items)
    device_signed = value.get("deviceSigned")
    if device_signed is not None and not isinstance(device_signed, Mapping):
        raise ValueError("deviceSigned must be an object")
    return Mdoc(doc_type, normalized, issuer_auth, device_signed)


__all__ = ["Mdoc", "parse_mdoc"]
