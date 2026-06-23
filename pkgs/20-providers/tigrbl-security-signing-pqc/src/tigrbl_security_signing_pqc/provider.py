from __future__ import annotations

import base64
import hashlib
from typing import Any, Final, Mapping

from tigrbl_security_trust_domain_bases import SigningDomainBase, SigningProviderBase
from tigrbl_security_trust_contracts import (
    Artifact,
    CanonicalizeRequest,
    CapabilityMap,
    IssueRequest,
    ParsedArtifact,
    ParseRequest,
    PQCSignatureKeyPair,
    SignRequest,
    SignResult,
    VerifySignatureRequest,
    VerifySignatureResult,
    VerificationResult,
    VerifyRequest,
)

PQC_LIBRARY_NAME: Final[str] = "pqcrypto"
PQC_REQUIRED_DEPENDENCY: Final[str] = "pqcrypto==0.4.0"
ML_DSA_65_ALG: Final[str] = "ML-DSA-65"
PQC_SIGNATURE_ALGS: Final[frozenset[str]] = frozenset({ML_DSA_65_ALG})
PQC_JWK_KTY: Final[str] = "PQC"


class PQCError(RuntimeError):
    """Raised when a post-quantum signing operation cannot be completed."""


try:  # pragma: no cover - import success is exercised by runtime tests
    from pqcrypto.sign import ml_dsa_65 as _ml_dsa_65
except Exception as exc:  # pragma: no cover - dependency failure path
    _ml_dsa_65 = None  # type: ignore[assignment]
    _IMPORT_ERROR: BaseException | None = exc
else:
    _IMPORT_ERROR = None


def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def b64url_decode(value: str) -> bytes:
    return base64.urlsafe_b64decode((value + "=" * (-len(value) % 4)).encode("ascii"))


def normalize_pqc_algorithm(algorithm: str) -> str:
    normalized = str(algorithm or "").replace("_", "-").upper()
    if normalized in {"ML-DSA-65", "MLDSA65"}:
        return ML_DSA_65_ALG
    raise PQCError("unsupported post-quantum signature algorithm")


def is_pqc_algorithm(algorithm: str | None) -> bool:
    if algorithm is None:
        return False
    try:
        normalize_pqc_algorithm(algorithm)
    except PQCError:
        return False
    return True


def pqc_backend_available() -> bool:
    return _ml_dsa_65 is not None


def assert_pqc_backend_available() -> None:
    if _ml_dsa_65 is None:
        detail = f": {_IMPORT_ERROR}" if _IMPORT_ERROR is not None else ""
        raise PQCError(
            f"post-quantum signature backend unavailable; install {PQC_REQUIRED_DEPENDENCY}{detail}"
        )


def pqc_backend_report() -> dict[str, Any]:
    return {
        "library": PQC_LIBRARY_NAME,
        "required_dependency": PQC_REQUIRED_DEPENDENCY,
        "available": pqc_backend_available(),
        "registered_algs": sorted(PQC_SIGNATURE_ALGS) if pqc_backend_available() else [],
    }


def generate_pqc_signature_keypair(*, algorithm: str = ML_DSA_65_ALG) -> PQCSignatureKeyPair:
    alg = normalize_pqc_algorithm(algorithm)
    assert_pqc_backend_available()
    public_key, secret_key = _ml_dsa_65.generate_keypair()
    return PQCSignatureKeyPair(algorithm=alg, public_key=public_key, secret_key=secret_key)


def sign_pqc_payload(payload: bytes, secret_key: bytes, *, algorithm: str = ML_DSA_65_ALG) -> bytes:
    normalize_pqc_algorithm(algorithm)
    assert_pqc_backend_available()
    return _ml_dsa_65.sign(secret_key, bytes(payload))


def verify_pqc_signature(
    payload: bytes,
    signature: bytes,
    public_key: bytes,
    *,
    algorithm: str = ML_DSA_65_ALG,
) -> bool:
    normalize_pqc_algorithm(algorithm)
    assert_pqc_backend_available()
    try:
        return bool(_ml_dsa_65.verify(public_key, bytes(payload), bytes(signature)))
    except Exception:
        return False


def pqc_public_jwk(
    public_key: bytes,
    *,
    kid: str | None = None,
    algorithm: str = ML_DSA_65_ALG,
) -> dict[str, str]:
    alg = normalize_pqc_algorithm(algorithm)
    key_id = kid or f"pqc:{alg.lower()}:{hashlib.sha256(public_key).hexdigest()[:24]}"
    return {
        "kty": PQC_JWK_KTY,
        "crv": alg,
        "alg": alg,
        "kid": key_id,
        "x": b64url(public_key),
    }


def pqc_signing_jwk(
    secret_key: bytes,
    public_key: bytes,
    *,
    kid: str | None = None,
    algorithm: str = ML_DSA_65_ALG,
) -> dict[str, str]:
    jwk = pqc_public_jwk(public_key, kid=kid, algorithm=algorithm)
    jwk["d"] = b64url(secret_key)
    return jwk


def public_key_from_pqc_jwk(jwk: Mapping[str, Any]) -> bytes:
    if str(jwk.get("kty") or "") != PQC_JWK_KTY:
        raise PQCError("PQC JWK requires PQC key type")
    normalize_pqc_algorithm(str(jwk.get("alg") or jwk.get("crv") or ""))
    x = jwk.get("x")
    if not isinstance(x, str) or not x:
        raise PQCError("PQC JWK requires public key material")
    return b64url_decode(x)


def secret_key_from_pqc_jwk(jwk: Mapping[str, Any]) -> bytes:
    public_key_from_pqc_jwk(jwk)
    d = jwk.get("d")
    if not isinstance(d, str) or not d:
        raise PQCError("PQC signing JWK requires secret key material")
    return b64url_decode(d)


class PQCSigningProvider(SigningProviderBase, SigningDomainBase):
    """Concrete ML-DSA-65 signing provider implementing the signing trust-domain base."""

    def supports(self) -> CapabilityMap:
        return CapabilityMap(
            ops={"sign": (ML_DSA_65_ALG,), "verify": (ML_DSA_65_ALG,)},
            formats=("raw-signature", "pqc-jwk"),
            algs=(ML_DSA_65_ALG,),
            features=("post-quantum", "ml-dsa-65"),
        )

    async def canonicalize(self, request: CanonicalizeRequest) -> bytes:
        payload = request.payload
        if isinstance(payload, bytes):
            return payload
        if isinstance(payload, bytearray):
            return bytes(payload)
        if isinstance(payload, str):
            return payload.encode("utf-8")
        raise PQCError("PQC signing payload must be bytes or text")

    async def issue(self, request: IssueRequest) -> Artifact:
        if request.key is None:
            raise PQCError("PQC signing requires secret key material")
        payload = await self.canonicalize(
            CanonicalizeRequest(payload=request.payload, canon=request.canon, format=request.format)
        )
        key = request.key
        if isinstance(key, Mapping):
            secret = secret_key_from_pqc_jwk(key)
        elif isinstance(key, bytes):
            secret = key
        else:
            raise PQCError("PQC signing key must be bytes or signing JWK")
        alg = normalize_pqc_algorithm(request.alg or ML_DSA_65_ALG)
        signature = sign_pqc_payload(payload, secret, algorithm=alg)
        return Artifact(
            kind="signature",
            format="raw-signature",
            bytes_value=signature,
            meta={"alg": alg, "provider": "tigrbl-security-signing-pqc"},
        )

    async def sign(self, request: SignRequest) -> SignResult:
        artifact = await self.issue(
            IssueRequest(
                op="sign",
                payload=request.payload,
                key=request.key,
                alg=request.alg,
                context=request.context,
                opts=request.opts,
            )
        )
        return SignResult(
            signature=artifact.bytes_value or b"",
            alg=str(artifact.meta.get("alg")) if artifact.meta.get("alg") else request.alg,
            format=artifact.format,
            meta=artifact.meta,
        )

    async def verify(self, request: VerifyRequest) -> VerificationResult:
        artifact = request.artifact
        if artifact.bytes_value is None:
            return VerificationResult(valid=False, reason="missing signature bytes")
        if request.key is None:
            return VerificationResult(valid=False, reason="missing public key")
        payload = await self.canonicalize(CanonicalizeRequest(payload=request.payload))
        key = request.key
        if isinstance(key, Mapping):
            public = public_key_from_pqc_jwk(key)
        elif isinstance(key, bytes):
            public = key
        else:
            return VerificationResult(valid=False, reason="PQC verification key must be bytes or public JWK")
        alg = normalize_pqc_algorithm(str(artifact.meta.get("alg") or ML_DSA_65_ALG))
        valid = verify_pqc_signature(payload, artifact.bytes_value, public, algorithm=alg)
        return VerificationResult(valid=valid, reason=None if valid else "invalid PQC signature")

    async def verify_signature(
        self,
        request: VerifySignatureRequest,
    ) -> VerifySignatureResult:
        signature = request.signature
        if isinstance(signature, Artifact):
            artifact = signature
        else:
            artifact = Artifact(
                kind="signature",
                format="raw-signature",
                bytes_value=signature if isinstance(signature, bytes) else str(signature).encode("utf-8"),
                meta={"alg": request.alg or ML_DSA_65_ALG},
            )
        result = await self.verify(
            VerifyRequest(
                artifact=artifact,
                payload=request.payload,
                key=request.key,
                context=request.context,
                opts=request.opts,
            )
        )
        return VerifySignatureResult(valid=result.valid, reason=result.reason, meta=result.meta)

    async def parse(self, request: ParseRequest) -> ParsedArtifact:
        return ParsedArtifact(
            kind=request.artifact.kind,
            format=request.artifact.format,
            meta=dict(request.artifact.meta),
        )


__all__ = [
    "ML_DSA_65_ALG",
    "PQCError",
    "PQC_JWK_KTY",
    "PQC_LIBRARY_NAME",
    "PQC_REQUIRED_DEPENDENCY",
    "PQC_SIGNATURE_ALGS",
    "PQCSigningProvider",
    "PQCSignatureKeyPair",
    "assert_pqc_backend_available",
    "b64url",
    "b64url_decode",
    "generate_pqc_signature_keypair",
    "is_pqc_algorithm",
    "normalize_pqc_algorithm",
    "pqc_backend_available",
    "pqc_backend_report",
    "pqc_public_jwk",
    "pqc_signing_jwk",
    "public_key_from_pqc_jwk",
    "secret_key_from_pqc_jwk",
    "sign_pqc_payload",
    "verify_pqc_signature",
]
