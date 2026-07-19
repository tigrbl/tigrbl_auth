import json
import os
from collections.abc import Mapping
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from tigrbl_identity_core.base64url import base64url_encode
from tigrbl_jwe_concrete import parse_jwe_compact
from tigrbl_protected_envelope_bases import (
    ProtectedEnvelopeIssuerBase,
    ProtectedEnvelopeVerifierBase,
)
from tigrbl_protected_envelope_contracts import (
    EnvelopeProtectionRequest,
    EnvelopeVerificationRequest,
    EnvelopeVerificationResult,
    ProtectedEnvelope,
)


class JweCryptographyProvider(
    ProtectedEnvelopeIssuerBase, ProtectedEnvelopeVerifierBase
):
    def __init__(self, keys: Mapping[str, bytes]):
        self._keys = {k: bytes(v) for k, v in keys.items()}

    def _key(self, reference: str) -> bytes:
        try:
            key = self._keys[reference]
        except KeyError as exc:
            raise LookupError(f"unknown JWE key: {reference}") from exc
        if len(key) != 32:
            raise ValueError("A256GCM requires a 256-bit key")
        return key

    def protect(self, request: EnvelopeProtectionRequest, /) -> ProtectedEnvelope:
        if request.external_aad:
            raise ValueError("compact JWE does not support external AAD")
        headers = dict(request.protected_headers)
        if headers.get("alg") != "dir" or headers.get("enc") != "A256GCM":
            raise ValueError("provider supports only dir/A256GCM")
        headers.setdefault("kid", request.key_reference)
        protected = base64url_encode(
            json.dumps(headers, separators=(",", ":"), sort_keys=True).encode()
        )
        iv = os.urandom(12)
        result = AESGCM(self._key(request.key_reference)).encrypt(
            iv, request.payload, protected.encode()
        )
        ciphertext, tag = result[:-16], result[-16:]
        token = ".".join(
            (
                protected,
                "",
                base64url_encode(iv),
                base64url_encode(ciphertext),
                base64url_encode(tag),
            )
        )
        return ProtectedEnvelope(request.kind, token, headers, payload=request.payload)

    def verify(
        self, request: EnvelopeVerificationRequest, /
    ) -> EnvelopeVerificationResult:
        try:
            parsed = parse_jwe_compact(str(request.envelope.serialization))
            kid = parsed.protected_headers.get("kid")
            if not isinstance(kid, str):
                raise ValueError("JWE kid is required")
            payload = AESGCM(self._key(kid)).decrypt(
                parsed.iv,
                parsed.ciphertext + parsed.authentication_tag,
                parsed.additional_authenticated_data,
            )
            return EnvelopeVerificationResult(
                True,
                structural_valid=True,
                cryptographic_valid=True,
                key_resolved=True,
                profile_valid=True,
                payload=payload,
                key_reference=kid,
            )
        except Exception as exc:
            return EnvelopeVerificationResult(False, reason=str(exc))
