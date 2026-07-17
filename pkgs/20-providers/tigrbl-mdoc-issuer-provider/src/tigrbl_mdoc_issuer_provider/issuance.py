from collections.abc import Callable, Mapping
from typing import Protocol

from tigrbl_digital_credential_bases import CredentialIssuerBase
from tigrbl_identity_contracts.digital_credentials import (
    CredentialIssuanceRequest,
    CredentialIssuanceResult,
    DigitalCredential,
)
from tigrbl_mdoc_concrete import parse_mdoc, parse_mobile_security_object

CanonicalCborEncoder = Callable[[Mapping[str, object]], bytes]


class CoseSign1Provider(Protocol):
    """Injected COSE Sign1 behavior used by this provider."""

    def sign1(self, payload: bytes, protected: Mapping[object, object]): ...


class MdocIssuerProvider(CredentialIssuerBase):
    """Compose ISO mdoc issuance from protocol parsing and an injected COSE signer."""

    def __init__(
        self,
        cose: CoseSign1Provider,
        encoder: CanonicalCborEncoder,
        algorithm: int | str,
    ):
        self._cose = cose
        self._encode = encoder
        self._algorithm = algorithm

    def issue(self, request: CredentialIssuanceRequest, /) -> CredentialIssuanceResult:
        if request.format.identifier != "mso_mdoc":
            raise ValueError("mdoc issuer only supports mso_mdoc")
        unsigned = request.attributes.get("mdoc")
        mso = request.attributes.get("mobile_security_object")
        if not isinstance(unsigned, Mapping) or not isinstance(mso, Mapping):
            raise ValueError(
                "mdoc issuance requires mdoc and mobile_security_object attributes"
            )
        parsed_mso = parse_mobile_security_object(mso)
        if unsigned.get("docType") != parsed_mso.doc_type:
            raise ValueError("mdoc docType must match MobileSecurityObject docType")
        issuer_signed = unsigned.get("issuerSigned")
        if not isinstance(issuer_signed, Mapping):
            raise ValueError("mdoc requires issuerSigned")
        issuer_auth = self._cose.sign1(
            self._encode(dict(mso)), {1: self._algorithm}
        ).encoded
        document = dict(unsigned)
        document["issuerSigned"] = {**issuer_signed, "issuerAuth": issuer_auth}
        parse_mdoc(document)
        return CredentialIssuanceResult(
            DigitalCredential(
                request.format,
                self._encode(document),
                subject=request.subject,
            )
        )


__all__ = ["CanonicalCborEncoder", "MdocIssuerProvider"]
