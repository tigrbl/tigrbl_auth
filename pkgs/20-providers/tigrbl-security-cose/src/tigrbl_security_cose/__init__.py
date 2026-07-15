from collections.abc import Callable, Mapping
from dataclasses import dataclass

from .algorithms import COSE_ALGORITHMS, CoseAlgorithm, resolve_cose_algorithm
from .keys import decode_cose_key, load_cose_public_key
from .signatures import verify_detached_signature

CoseSigner = Callable[[bytes, Mapping[int | str, object], bytes], bytes]
CoseVerifier = Callable[[bytes, bytes, str], bool]


@dataclass(frozen=True, slots=True)
class CoseSign1Envelope:
    encoded: bytes
    payload: bytes
    protected_headers: Mapping[int | str, object]


class CoseSign1Provider:
    def __init__(
        self, signer: CoseSigner | None = None, verifier: CoseVerifier | None = None
    ):
        self._signer = signer
        self._verifier = verifier

    def sign1(
        self,
        payload: bytes,
        protected_headers: Mapping[int | str, object],
        external_aad: bytes = b"",
    ) -> CoseSign1Envelope:
        if self._signer is None:
            raise RuntimeError("COSE signing backend is not configured")
        if not payload or 1 not in protected_headers and "alg" not in protected_headers:
            raise ValueError(
                "COSE_Sign1 requires payload and protected algorithm header"
            )
        encoded = self._signer(payload, protected_headers, external_aad)
        if not isinstance(encoded, bytes) or not encoded:
            raise ValueError("COSE signer returned no encoded message")
        return CoseSign1Envelope(encoded, payload, dict(protected_headers))

    def verify1(self, encoded: bytes, external_aad: bytes, profile: str) -> bool:
        if self._verifier is None:
            raise RuntimeError("COSE verification backend is not configured")
        if not encoded or not profile:
            raise ValueError("COSE verification requires message and profile")
        return self._verifier(encoded, external_aad, profile)


__all__ = [
    "COSE_ALGORITHMS",
    "CoseAlgorithm",
    "CoseSign1Envelope",
    "CoseSign1Provider",
    "CoseSigner",
    "CoseVerifier",
    "decode_cose_key",
    "load_cose_public_key",
    "resolve_cose_algorithm",
    "verify_detached_signature",
]
