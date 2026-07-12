from dataclasses import dataclass
from typing import Mapping

from .issuer_signed import IssuerSigned, parse_issuer_signed


@dataclass(frozen=True, slots=True)
class Mdoc:
    doc_type: str
    issuer_signed: IssuerSigned
    device_signed: Mapping[str, object] | None = None

    @property
    def name_spaces(self):
        return self.issuer_signed.name_spaces

    @property
    def issuer_auth(self):
        return self.issuer_signed.issuer_auth


def parse_mdoc(value: Mapping[str, object]) -> Mdoc:
    doc_type, issuer_signed = value.get("docType"), value.get("issuerSigned")
    if (
        not isinstance(doc_type, str)
        or not doc_type
        or not isinstance(issuer_signed, Mapping)
    ):
        raise ValueError("mdoc requires docType and issuerSigned")
    device_signed = value.get("deviceSigned")
    if device_signed is not None and not isinstance(device_signed, Mapping):
        raise ValueError("deviceSigned must be an object")
    return Mdoc(doc_type, parse_issuer_signed(issuer_signed), device_signed)


__all__ = ["Mdoc", "parse_mdoc"]
