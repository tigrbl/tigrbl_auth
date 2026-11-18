import json
import os
from collections.abc import Mapping
from cryptography.hazmat.primitives.asymmetric.x448 import X448PrivateKey, X448PublicKey
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from tba_primitives_identity.base64url import base64url_encode
from tba_concrete_jwe import parse_jwe_compact
from tba_bases_protected_envelope import (
    ProtectedEnvelopeIssuerBase,
    ProtectedEnvelopeVerifierBase,
)
from tba_contracts_protected_envelope import (
    EnvelopeProtectionRequest,
    EnvelopeVerificationRequest,
    EnvelopeVerificationResult,
    ProtectedEnvelope,
)
from tba_contracts_security_trust import ICipherPolicy

from ._x448 import content_key, load_public_jwk, public_jwk


class JweCryptographyProvider(
    ProtectedEnvelopeIssuerBase, ProtectedEnvelopeVerifierBase
):
    def __init__(
        self,
        keys: Mapping[str, bytes] | None = None,
        *,
        cipher_policy: ICipherPolicy | None = None,
        x448_public_keys: Mapping[str, X448PublicKey] | None = None,
        x448_private_keys: Mapping[str, X448PrivateKey] | None = None,
    ) -> None:
        self._keys = {k: bytes(v) for k, v in (keys or {}).items()}
        self._cipher_policy = cipher_policy
        self._x448_public_keys = dict(x448_public_keys or {})
        self._x448_private_keys = dict(x448_private_keys or {})

    def _key(self, reference: str) -> bytes:
        try:
            key = self._keys[reference]
        except KeyError as exc:
            raise LookupError(f"unknown JWE key: {reference}") from exc
        if len(key) != 32:
            raise ValueError("A256GCM requires a 256-bit key")
        return key

    def _key_algorithm(self, headers: Mapping[str, object]) -> str:
        alg, enc = headers.get("alg"), headers.get("enc")
        if enc != "A256GCM":
            raise ValueError("JWE provider requires A256GCM")
        if alg == "dir":
            return "dir"
        if alg != "ECDH-ES":
            raise ValueError("unsupported JWE key management algorithm")
        if self._cipher_policy is None:
            raise ValueError("ECDH-ES requires an explicit X448 cipher policy")
        if "zip" in headers or "crit" in headers:
            raise ValueError("X448 compact JWE requires unextended serialization")
        return "ECDH-ES"

    def _check_x448_policy(self, kid: str) -> None:
        assert self._cipher_policy is not None
        decision = self._cipher_policy.normalize(
            op="key_agreement",
            alg="ECDH-ES",
            key={"kid": kid, "kty": "OKP", "crv": "X448"},
            params={"enc": "A256GCM"},
            dialect="jwa",
        )
        if decision.alg != "ECDH-ES" or decision.params.get("enc") != "A256GCM":
            raise ValueError("X448 cipher policy must select ECDH-ES/A256GCM")

    def protect(self, request: EnvelopeProtectionRequest, /) -> ProtectedEnvelope:
        if request.external_aad:
            raise ValueError("compact JWE does not support external AAD")
        headers = dict(request.protected_headers)
        kid = request.key_reference
        if headers.setdefault("kid", kid) != kid:
            raise ValueError("JWE kid must match the recipient key reference")
        if self._key_algorithm(headers) == "dir":
            key = self._key(kid)
        else:
            self._check_x448_policy(kid)
            recipient = self._x448_public_keys.get(kid)
            if not isinstance(recipient, X448PublicKey):
                raise LookupError(f"unknown X448 recipient public key: {kid}")
            ephemeral = X448PrivateKey.generate()
            headers["epk"] = public_jwk(ephemeral.public_key())
            key = content_key(ephemeral.exchange(recipient), headers)
        protected = base64url_encode(
            json.dumps(headers, separators=(",", ":"), sort_keys=True).encode()
        )
        iv = os.urandom(12)
        result = AESGCM(key).encrypt(iv, request.payload, protected.encode("ascii"))
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
            if request.external_aad:
                raise ValueError("compact JWE does not support external AAD")
            parsed = parse_jwe_compact(str(request.envelope.serialization))
            headers = parsed.protected_headers
            kid = headers.get("kid")
            if not isinstance(kid, str):
                raise ValueError("JWE kid is required")
            if parsed.encrypted_key_segment:
                raise ValueError("direct JWE requires an empty Encrypted Key field")
            if len(parsed.iv) != 12 or len(parsed.authentication_tag) != 16:
                raise ValueError("A256GCM requires a 96-bit IV and a 128-bit tag")
            if self._key_algorithm(headers) == "dir":
                key = self._key(kid)
            else:
                self._check_x448_policy(kid)
                recipient = self._x448_private_keys.get(kid)
                if not isinstance(recipient, X448PrivateKey):
                    raise LookupError(f"unknown X448 recipient private key: {kid}")
                key = content_key(
                    recipient.exchange(load_public_jwk(headers.get("epk"))), headers
                )
            payload = AESGCM(key).decrypt(
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
