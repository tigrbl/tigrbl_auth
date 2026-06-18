"""Post-quantum JOSE primitives for the Tigrbl identity token plane."""

from __future__ import annotations

import base64
import hashlib
from dataclasses import dataclass
from typing import Any, Final, Mapping

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


@dataclass(frozen=True, slots=True)
class PQCSignatureKeyPair:
    algorithm: str
    public_key: bytes
    secret_key: bytes
    library: str = PQC_LIBRARY_NAME


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


__all__ = [
    "ML_DSA_65_ALG",
    "PQCError",
    "PQC_JWK_KTY",
    "PQC_LIBRARY_NAME",
    "PQC_REQUIRED_DEPENDENCY",
    "PQC_SIGNATURE_ALGS",
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
