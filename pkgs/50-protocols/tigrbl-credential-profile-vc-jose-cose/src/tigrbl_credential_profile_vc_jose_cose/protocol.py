"""Executable VC-JOSE-COSE issuance and verification profile."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Mapping

import cbor2
from tigrbl_cose_concrete import CoseMessageKind, decode_cose_message
from tigrbl_identity_core import ProtectedEnvelopeKind
from tigrbl_jws_concrete import parse_jws_compact
from tigrbl_protected_envelope_contracts import (
    EnvelopeVerificationResult,
    ProtectedEnvelope,
)
from tigrbl_vc_cose_credential_concrete import VcCoseCredential
from tigrbl_vc_jose_credential_concrete import VcJoseCredential

from .formats import select_format
from .validation import validate_cose_vc, validate_jose_vc


SecuredVcCredential = VcJoseCredential | VcCoseCredential


@dataclass(frozen=True, slots=True)
class SecuredVcVerificationResult:
    valid: bool
    credential: SecuredVcCredential | None = None
    envelope_result: EnvelopeVerificationResult | None = None
    reason: str | None = None


class VcJoseCoseProtocol:
    def __init__(self, *, jws_protocol=None, cose_protocol=None) -> None:
        self._jws = jws_protocol
        self._cose = cose_protocol

    def issue(
        self,
        claims: Mapping[str, object],
        *,
        media_type: str,
        key_reference: str,
        headers: Mapping[object, object],
    ) -> SecuredVcCredential:
        selected = select_format(media_type)
        materialized = dict(claims)
        if selected.envelope_family == "JOSE":
            if self._jws is None:
                raise RuntimeError("JWS protocol is not configured")
            jose_headers = {str(key): value for key, value in headers.items()}
            validate_jose_vc(jose_headers, materialized, media_type=media_type)
            payload = json.dumps(
                materialized,
                ensure_ascii=False,
                separators=(",", ":"),
                sort_keys=True,
            ).encode("utf-8")
            protected = self._jws.sign(
                payload,
                key_reference=key_reference,
                headers=jose_headers,
            )
            return VcJoseCredential(
                parse_jws_compact(str(protected.serialization)),
                materialized,
            )
        if self._cose is None:
            raise RuntimeError("COSE protocol is not configured")
        cose_headers = dict(headers)
        validate_cose_vc(cose_headers, materialized, media_type=media_type)
        protected = self._cose.sign1(
            cbor2.dumps(materialized, canonical=True),
            key_reference=key_reference,
            headers=cose_headers,
        )
        return VcCoseCredential(
            decode_cose_message(
                bytes(protected.serialization),
                expected_kind=CoseMessageKind.SIGN1,
            ),
            materialized,
        )

    def verify(
        self,
        credential: SecuredVcCredential,
        /,
    ) -> SecuredVcVerificationResult:
        try:
            if isinstance(credential, VcJoseCredential):
                if self._jws is None:
                    raise RuntimeError("JWS protocol is not configured")
                envelope = ProtectedEnvelope(
                    ProtectedEnvelopeKind.JWS,
                    credential.envelope.serialized,
                    credential.envelope.protected_headers,
                )
                result = self._jws.verify(envelope)
                claims = self._decode_json_claims(result.payload)
                validate_jose_vc(
                    credential.envelope.protected_headers,
                    claims,
                    media_type="application/vc+jwt",
                )
                verified = VcJoseCredential(credential.envelope, claims)
            elif isinstance(credential, VcCoseCredential):
                if self._cose is None:
                    raise RuntimeError("COSE protocol is not configured")
                envelope = ProtectedEnvelope(
                    ProtectedEnvelopeKind.COSE_SIGN1,
                    credential.envelope.encoded,
                    credential.envelope.protected_headers,
                    credential.envelope.unprotected_headers,
                )
                result = self._cose.verify1(envelope)
                claims = self._decode_cbor_claims(result.payload)
                validate_cose_vc(
                    credential.envelope.protected_headers,
                    claims,
                    media_type="application/vc+cose",
                )
                verified = VcCoseCredential(credential.envelope, claims)
            else:
                raise TypeError("unsupported secured VC credential")
        except (RuntimeError, TypeError, ValueError) as exc:
            return SecuredVcVerificationResult(False, reason=str(exc))
        return SecuredVcVerificationResult(True, verified, result)

    @staticmethod
    def _decode_json_claims(payload: bytes | None) -> dict[str, object]:
        if payload is None:
            raise ValueError("verified JOSE VC payload is missing")
        value = json.loads(payload)
        if not isinstance(value, dict):
            raise ValueError("verified JOSE VC payload must be an object")
        return value

    @staticmethod
    def _decode_cbor_claims(payload: bytes | None) -> dict[str, object]:
        if payload is None:
            raise ValueError("verified COSE VC payload is missing")
        value = cbor2.loads(payload)
        if not isinstance(value, Mapping):
            raise ValueError("verified COSE VC payload must be a map")
        return dict(value)


__all__ = [
    "SecuredVcCredential",
    "SecuredVcVerificationResult",
    "VcJoseCoseProtocol",
]
