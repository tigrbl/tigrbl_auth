from typing import Mapping

from tigrbl_mdoc_credential_concrete import MdocCredential

from .issuer_signed import parse_issuer_signed

Mdoc = MdocCredential


def parse_mdoc(value: Mapping[str, object]) -> MdocCredential:
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
    return MdocCredential(doc_type, parse_issuer_signed(issuer_signed), device_signed)


__all__ = ["Mdoc", "parse_mdoc"]
