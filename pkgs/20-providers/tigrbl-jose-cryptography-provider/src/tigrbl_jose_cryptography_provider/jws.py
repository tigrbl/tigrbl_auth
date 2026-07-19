import hashlib
import hmac
import json
from collections.abc import Mapping
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
from tigrbl_identity_core.base64url import base64url_encode
from tigrbl_jws_concrete import parse_jws_compact, validate_unencoded_payload_headers
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


class JwsCryptographyProvider(
    ProtectedEnvelopeIssuerBase, ProtectedEnvelopeVerifierBase
):
    def __init__(self, keys: Mapping[str, object]):
        self._keys = dict(keys)

    def _key(self, reference: str) -> object:
        if reference not in self._keys:
            raise LookupError(f"unknown JOSE key: {reference}")
        return self._keys[reference]

    def protect(self, request: EnvelopeProtectionRequest, /) -> ProtectedEnvelope:
        headers = dict(request.protected_headers)
        validate_unencoded_payload_headers(headers)
        alg = headers.get("alg")
        protected = base64url_encode(
            json.dumps(headers, separators=(",", ":"), sort_keys=True).encode()
        )
        payload = base64url_encode(request.payload)
        signing_input = f"{protected}.{payload}".encode()
        key = self._key(request.key_reference)
        if alg == "HS256":
            signature = hmac.new(bytes(key), signing_input, hashlib.sha256).digest()
        elif alg == "EdDSA":
            private = (
                serialization.load_pem_private_key(bytes(key), password=None)
                if isinstance(key, (bytes, bytearray))
                else key
            )
            if not isinstance(private, ed25519.Ed25519PrivateKey):
                raise ValueError("EdDSA requires Ed25519 private key")
            signature = private.sign(signing_input)
        else:
            raise ValueError(f"unsupported JWS algorithm: {alg}")
        token = f"{protected}.{payload}.{base64url_encode(signature)}"
        return ProtectedEnvelope(request.kind, token, headers, payload=request.payload)

    def verify(
        self, request: EnvelopeVerificationRequest, /
    ) -> EnvelopeVerificationResult:
        try:
            parsed = parse_jws_compact(str(request.envelope.serialization))
            validate_unencoded_payload_headers(parsed.protected_headers)
            kid = parsed.protected_headers.get("kid")
            alg = parsed.protected_headers.get("alg")
            if not isinstance(kid, str):
                raise ValueError("JWS kid is required")
            key = self._key(kid)
            signing_input = parsed.signing_input(request.detached_payload)
            if alg == "HS256":
                valid = hmac.compare_digest(
                    parsed.signature,
                    hmac.new(bytes(key), signing_input, hashlib.sha256).digest(),
                )
            elif alg == "EdDSA":
                public = (
                    serialization.load_pem_public_key(bytes(key))
                    if isinstance(key, (bytes, bytearray))
                    else key
                )
                if isinstance(public, ed25519.Ed25519PrivateKey):
                    public = public.public_key()
                try:
                    public.verify(parsed.signature, signing_input)
                    valid = True
                except InvalidSignature:
                    valid = False
            else:
                raise ValueError(f"unsupported JWS algorithm: {alg}")
            return EnvelopeVerificationResult(
                valid,
                structural_valid=True,
                cryptographic_valid=valid,
                key_resolved=True,
                profile_valid=valid,
                payload=parsed.payload,
                key_reference=kid,
            )
        except Exception as exc:
            return EnvelopeVerificationResult(False, reason=str(exc))
