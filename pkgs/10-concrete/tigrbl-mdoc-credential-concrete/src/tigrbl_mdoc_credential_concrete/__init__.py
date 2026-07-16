from dataclasses import dataclass
from typing import Mapping

from tigrbl_digital_credential_bases import CredentialFormatBase


@dataclass(frozen=True, slots=True)
class MdocCredential(CredentialFormatBase):
    format_identifier = "mso_mdoc"
    doc_type: str
    issuer_signed: object
    device_signed: Mapping[str, object] | None = None

    def __post_init__(self) -> None:
        if not self.doc_type:
            raise ValueError("mdoc credential requires a document type")
        if not self.issuer_signed:
            raise ValueError("mdoc credential requires issuer-signed material")

    @property
    def name_spaces(self):
        return getattr(
            self.issuer_signed,
            "name_spaces",
            self.issuer_signed.get("nameSpaces", {})
            if isinstance(self.issuer_signed, Mapping)
            else {},
        )

    @property
    def issuer_auth(self):
        return getattr(
            self.issuer_signed,
            "issuer_auth",
            self.issuer_signed.get("issuerAuth")
            if isinstance(self.issuer_signed, Mapping)
            else None,
        )


__all__ = ["MdocCredential"]
