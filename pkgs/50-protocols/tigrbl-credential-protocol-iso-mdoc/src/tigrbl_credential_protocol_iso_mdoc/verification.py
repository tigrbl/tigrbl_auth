from collections.abc import Callable, Mapping
from hashlib import new

from tigrbl_digital_credential_bases import CredentialVerifierBase
from tigrbl_identity_contracts.digital_credentials import (
    CredentialVerificationRequest,
    CredentialVerificationResult,
)
from tigrbl_security_cose import CoseSign1Provider

from .schemas import parse_mdoc, parse_mobile_security_object

CanonicalCborEncoder = Callable[[Mapping[str, object]], bytes]
CborDecoder = Callable[[bytes], Mapping[str, object]]
CosePayloadDecoder = Callable[[bytes], bytes]


class MdocVerifierProvider(CredentialVerifierBase):
    """Compose ISO mdoc verification from protocol rules and injected trust tools."""

    def __init__(
        self,
        cose: CoseSign1Provider,
        encoder: CanonicalCborEncoder,
        decoder: CborDecoder,
        cose_payload_decoder: CosePayloadDecoder,
    ):
        self._cose = cose
        self._encode = encoder
        self._decode = decoder
        self._cose_payload = cose_payload_decoder

    def verify(
        self, request: CredentialVerificationRequest, /
    ) -> CredentialVerificationResult:
        if (
            request.expected_format.identifier != "mso_mdoc"
            or request.credential.format != request.expected_format
        ):
            return CredentialVerificationResult(
                False, errors=("unexpected mdoc format",)
            )
        if not isinstance(request.credential.payload, bytes):
            return CredentialVerificationResult(
                False, errors=("mdoc payload must be CBOR bytes",)
            )
        try:
            document = parse_mdoc(self._decode(request.credential.payload))
            if not self._cose.verify1(document.issuer_auth, b"", "mdoc-issuer"):
                return CredentialVerificationResult(
                    False, errors=("mdoc issuer authentication failed",)
                )
            mso = parse_mobile_security_object(
                self._decode(self._cose_payload(document.issuer_auth))
            )
            if mso.doc_type != document.doc_type:
                return CredentialVerificationResult(
                    False, errors=("MSO docType mismatch",)
                )
            for namespace, items in document.name_spaces.items():
                expected = mso.value_digests.get(namespace, {})
                for item in items:
                    encoded_item = self._encode(
                        {
                            "digestID": item.digest_id,
                            "random": item.random,
                            "elementIdentifier": item.element_identifier,
                            "elementValue": item.element_value,
                        }
                    )
                    digest = new(
                        mso.digest_algorithm.replace("-", "").lower(), encoded_item
                    ).digest()
                    if expected.get(item.digest_id) != digest:
                        return CredentialVerificationResult(
                            False, errors=("issuer-signed item digest mismatch",)
                        )
        except (TypeError, ValueError) as exc:
            return CredentialVerificationResult(False, errors=(f"invalid mdoc: {exc}",))
        claims = {
            namespace: {item.element_identifier: item.element_value for item in items}
            for namespace, items in document.name_spaces.items()
        }
        return CredentialVerificationResult(True, claims)


__all__ = [
    "CanonicalCborEncoder",
    "CborDecoder",
    "CosePayloadDecoder",
    "MdocVerifierProvider",
]
