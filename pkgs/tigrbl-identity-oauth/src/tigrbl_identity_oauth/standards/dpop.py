"""Domain-organized RFC 9449 DPoP helpers.

The release/runtime path uses the dedicated Swarmauri DPoP signer when it is
available, but this module also exposes a dependency-light Ed25519 fallback so
checkpoint evidence and low-dependency tests can execute without the full
runtime stack.
"""

from __future__ import annotations

import asyncio
import base64
import hashlib
import json
import secrets
import threading
import time
from dataclasses import dataclass
from typing import Any, Dict, Final

try:
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
    from cryptography.hazmat.primitives.serialization import (
        Encoding,
        NoEncryption,
        PrivateFormat,
        PublicFormat,
        load_pem_private_key,
        load_pem_public_key,
    )
except Exception:  # pragma: no cover - cryptography is expected in release/runtime installs
    serialization = None  # type: ignore[assignment]
    Ed25519PrivateKey = None  # type: ignore[assignment]
    Ed25519PublicKey = None  # type: ignore[assignment]
    Encoding = None  # type: ignore[assignment]
    NoEncryption = None  # type: ignore[assignment]
    PrivateFormat = None  # type: ignore[assignment]
    PublicFormat = None  # type: ignore[assignment]
    load_pem_private_key = None  # type: ignore[assignment]
    load_pem_public_key = None  # type: ignore[assignment]

try:  # pragma: no cover - exercised in real runtime installs
    from swarmauri_signing_dpop import DpopSigner
except Exception:  # pragma: no cover - dependency-light checkpoint fallback
    DpopSigner = None  # type: ignore[assignment]

from tigrbl_auth.config.settings import settings

RFC9449_SPEC_URL: Final[str] = "https://www.rfc-editor.org/rfc/rfc9449"
_ALG_VALUE: Final[str] = "EdDSA"
_TYP_VALUE: Final[str] = "dpop+jwt"
_ALLOWED_SKEW: Final[int] = 300
_SIGNER = DpopSigner() if DpopSigner is not None else None


@dataclass(frozen=True, slots=True)
class DPoPProofClaims:
    jti: str
    htm: str
    htu: str
    iat: int | None
    nonce: str | None
    ath: str | None
    jkt: str

    def as_dict(self) -> dict[str, object]:
        return {
            "jti": self.jti,
            "htm": self.htm,
            "htu": self.htu,
            "iat": self.iat,
            "nonce": self.nonce,
            "ath": self.ath,
            "jkt": self.jkt,
        }


@dataclass(frozen=True, slots=True)
class DPoPNonceRecord:
    nonce: str
    expires_at: int


@dataclass(frozen=True, slots=True)
class StandardOwner:
    label: str
    title: str
    runtime_status: str
    public_surface: tuple[str, ...]
    notes: str


OWNER = StandardOwner(
    label="RFC 9449",
    title="OAuth 2.0 Demonstrating Proof-of-Possession at the Application Layer",
    runtime_status="dpop-runtime-integrated",
    public_surface=("/token", "/token/exchange", "/userinfo", "/introspect", "/revoke"),
    notes=(
        "DPoP proof verification is runtime-integrated with jkt binding, ath binding, optional nonce validation, "
        "iat freshness checks, and replay-safe jti tracking."
    ),
)


class DPoPReplayStore:
    def __init__(self) -> None:
        self._entries: dict[str, int] = {}
        self._lock = threading.RLock()

    def _purge(self, *, now: int) -> None:
        expired = [key for key, expiry in self._entries.items() if expiry <= now]
        for key in expired:
            self._entries.pop(key, None)

    def check_and_store(self, key: str, *, now: int | None = None, ttl_s: int = _ALLOWED_SKEW) -> bool:
        current = int(time.time()) if now is None else int(now)
        with self._lock:
            self._purge(now=current)
            if key in self._entries:
                return True
            self._entries[key] = current + max(int(ttl_s), 1)
            return False

    def snapshot(self) -> dict[str, int]:
        current = int(time.time())
        with self._lock:
            self._purge(now=current)
            return dict(self._entries)

    def clear(self) -> None:
        with self._lock:
            self._entries.clear()


class DPoPNonceStore:
    def __init__(self) -> None:
        self._entries: dict[str, int] = {}
        self._lock = threading.RLock()

    def _purge(self, *, now: int) -> None:
        expired = [key for key, expiry in self._entries.items() if expiry <= now]
        for key in expired:
            self._entries.pop(key, None)

    def issue(self, *, ttl_s: int = _ALLOWED_SKEW) -> str:
        nonce = secrets.token_urlsafe(24)
        self.register(nonce, ttl_s=ttl_s)
        return nonce

    def register(self, nonce: str, *, ttl_s: int = _ALLOWED_SKEW) -> str:
        current = int(time.time())
        with self._lock:
            self._purge(now=current)
            self._entries[str(nonce)] = current + max(int(ttl_s), 1)
        return str(nonce)

    def consume(self, nonce: str, *, now: int | None = None) -> bool:
        current = int(time.time()) if now is None else int(now)
        with self._lock:
            self._purge(now=current)
            expiry = self._entries.pop(str(nonce), None)
            return expiry is not None and expiry > current

    def snapshot(self) -> dict[str, DPoPNonceRecord]:
        current = int(time.time())
        with self._lock:
            self._purge(now=current)
            return {key: DPoPNonceRecord(nonce=key, expires_at=expiry) for key, expiry in self._entries.items()}

    def clear(self) -> None:
        with self._lock:
            self._entries.clear()


DEFAULT_REPLAY_STORE = DPoPReplayStore()
DEFAULT_NONCE_STORE = DPoPNonceStore()


def _run_async(coro: Any) -> Any:
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)
    result: dict[str, Any] = {}
    error: dict[str, BaseException] = {}

    def _runner() -> None:
        try:
            result["value"] = asyncio.run(coro)
        except BaseException as exc:  # pragma: no cover - propagated to caller
            error["exc"] = exc

    thread = threading.Thread(target=_runner)
    thread.start()
    thread.join()
    if error:
        raise error["exc"]
    return result.get("value")


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64url_decode(data: str) -> bytes:
    padded = str(data) + ("=" * (-len(str(data)) % 4))
    return base64.urlsafe_b64decode(padded)


def _json_segment(payload: dict[str, Any]) -> str:
    return _b64url(json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8"))


def _compact_signing_input(header: dict[str, Any], payload: dict[str, Any]) -> str:
    return f"{_json_segment(header)}.{_json_segment(payload)}"


def _raw_public_bytes(public_key: Any) -> bytes:
    if isinstance(public_key, bytes):
        raw = public_key
    elif isinstance(public_key, str):
        raw = public_key.encode("utf-8")
    elif Ed25519PublicKey is not None and isinstance(public_key, Ed25519PublicKey):
        return public_key.public_bytes(Encoding.Raw, PublicFormat.Raw)
    elif hasattr(public_key, "public_bytes") and Encoding is not None and PublicFormat is not None:
        try:
            return public_key.public_bytes(Encoding.Raw, PublicFormat.Raw)
        except Exception:
            raw = b""
    else:
        raw = b""
    if raw.startswith(b"-----BEGIN"):
        if load_pem_public_key is None or Encoding is None or PublicFormat is None:
            raise RuntimeError("PEM public-key conversion requires cryptography serialization support")
        pub_obj = load_pem_public_key(raw)
        return pub_obj.public_bytes(Encoding.Raw, PublicFormat.Raw)
    if raw:
        return raw
    raise ValueError("public key material required for DPoP proof handling")


def _raw_private_bytes(keyref: Any) -> bytes:
    material = getattr(keyref, "material", keyref)
    if isinstance(material, str):
        return material.encode("utf-8")
    if isinstance(material, bytes):
        return material
    if Ed25519PrivateKey is not None and isinstance(material, Ed25519PrivateKey):
        return material.private_bytes(Encoding.Raw, PrivateFormat.Raw, NoEncryption())
    if hasattr(material, "private_bytes") and Encoding is not None and PrivateFormat is not None and NoEncryption is not None:
        try:
            return material.private_bytes(Encoding.Raw, PrivateFormat.Raw, NoEncryption())
        except Exception:
            pass
    raise ValueError("private key material required for DPoP proof generation")


def _load_private_key(keyref: Any) -> Any:
    if Ed25519PrivateKey is None:
        raise RuntimeError("cryptography Ed25519 support is unavailable")
    material = getattr(keyref, "material", keyref)
    if isinstance(material, Ed25519PrivateKey):
        return material
    if hasattr(material, "sign") and hasattr(material, "public_key"):
        return material
    raw = _raw_private_bytes(keyref)
    if raw.startswith(b"-----BEGIN"):
        if load_pem_private_key is None:
            raise RuntimeError("PEM private-key conversion requires cryptography serialization support")
        private_key = load_pem_private_key(raw, password=None)
        if not isinstance(private_key, Ed25519PrivateKey):
            raise ValueError("DPoP fallback only supports Ed25519 private keys")
        return private_key
    if len(raw) != 32:
        raise ValueError("DPoP fallback expects Ed25519 raw private key bytes")
    return Ed25519PrivateKey.from_private_bytes(raw)


# ---------------------------------------------------------------------------
# JWK helpers
# ---------------------------------------------------------------------------


def jwk_from_public_key(public_key: Any) -> Dict[str, str]:
    x = _b64url(_raw_public_bytes(public_key))
    return {"kty": "OKP", "crv": "Ed25519", "x": x}


def jwk_thumbprint(jwk: Dict[str, str]) -> str:
    data = json.dumps({k: jwk[k] for k in sorted(jwk)}, separators=(",", ":")).encode()
    digest = hashlib.sha256(data).digest()
    return _b64url(digest)


# ---------------------------------------------------------------------------
# Proof helpers
# ---------------------------------------------------------------------------


def ath_for_access_token(access_token: str) -> str:
    digest = hashlib.sha256(str(access_token).encode("utf-8")).digest()
    return _b64url(digest)


access_token_hash = ath_for_access_token


def _segments(proof: str) -> tuple[dict[str, Any], dict[str, Any]]:
    parts = str(proof).split(".")
    if len(parts) != 3:
        raise ValueError(f"malformed DPoP proof: {RFC9449_SPEC_URL}")
    try:
        header = json.loads(_b64url_decode(parts[0]).decode("utf-8"))
        payload = json.loads(_b64url_decode(parts[1]).decode("utf-8"))
    except Exception as exc:
        raise ValueError(f"invalid DPoP proof encoding: {RFC9449_SPEC_URL}") from exc
    if not isinstance(header, dict) or not isinstance(payload, dict):
        raise ValueError(f"invalid DPoP proof payload: {RFC9449_SPEC_URL}")
    return header, payload


def proof_claims(proof: str) -> DPoPProofClaims:
    header, payload = _segments(proof)
    jwk = header.get("jwk")
    if not isinstance(jwk, dict) or not jwk:
        raise ValueError(f"missing jwk in DPoP header: {RFC9449_SPEC_URL}")
    jti = str(payload.get("jti") or "").strip()
    if not jti:
        raise ValueError(f"missing jti in DPoP proof: {RFC9449_SPEC_URL}")
    htm = str(payload.get("htm") or "").upper().strip()
    htu = str(payload.get("htu") or "").strip()
    if not htm or not htu:
        raise ValueError(f"missing htm/htu in DPoP proof: {RFC9449_SPEC_URL}")
    iat_raw = payload.get("iat")
    if iat_raw is not None and not isinstance(iat_raw, int):
        raise ValueError(f"invalid iat in DPoP proof: {RFC9449_SPEC_URL}")
    nonce = payload.get("nonce")
    if nonce is not None and not isinstance(nonce, str):
        raise ValueError(f"invalid nonce in DPoP proof: {RFC9449_SPEC_URL}")
    ath = payload.get("ath")
    if ath is not None and not isinstance(ath, str):
        raise ValueError(f"invalid ath in DPoP proof: {RFC9449_SPEC_URL}")
    normalized_jwk = {str(key): str(value) for key, value in jwk.items()}
    return DPoPProofClaims(
        jti=jti,
        htm=htm,
        htu=htu,
        iat=iat_raw,
        nonce=nonce,
        ath=ath,
        jkt=jwk_thumbprint(normalized_jwk),
    )


def decode_proof(proof: str) -> dict[str, object]:
    return proof_claims(proof).as_dict()


def _verify_fallback_signature(proof: str, method: str, url: str, *, max_skew_s: int = _ALLOWED_SKEW) -> bool:
    if Ed25519PublicKey is None:
        raise RuntimeError("cryptography Ed25519 support is unavailable")
    header, payload = _segments(proof)
    alg = str(header.get("alg") or "")
    if alg != _ALG_VALUE:
        raise ValueError(f"unsupported DPoP alg: {RFC9449_SPEC_URL}")
    typ = str(header.get("typ") or "").lower().strip()
    if typ and typ != _TYP_VALUE:
        raise ValueError(f"invalid DPoP typ: {RFC9449_SPEC_URL}")
    jwk = header.get("jwk")
    if not isinstance(jwk, dict) or str(jwk.get("kty") or "") != "OKP" or str(jwk.get("crv") or "") != "Ed25519":
        raise ValueError(f"unsupported DPoP jwk: {RFC9449_SPEC_URL}")
    x = str(jwk.get("x") or "").strip()
    if not x:
        raise ValueError(f"missing DPoP jwk x: {RFC9449_SPEC_URL}")
    htm = str(payload.get("htm") or "").upper().strip()
    htu = str(payload.get("htu") or "").strip()
    if htm != method.upper() or htu != url:
        return False
    iat = payload.get("iat")
    if not isinstance(iat, int):
        raise ValueError(f"missing iat in DPoP proof: {RFC9449_SPEC_URL}")
    if abs(int(time.time()) - int(iat)) > max_skew_s:
        raise ValueError(f"stale DPoP proof: {RFC9449_SPEC_URL}")
    parts = str(proof).split(".")
    if len(parts) != 3:
        raise ValueError(f"malformed DPoP proof: {RFC9449_SPEC_URL}")
    public_key = Ed25519PublicKey.from_public_bytes(_b64url_decode(x))
    try:
        public_key.verify(_b64url_decode(parts[2]), f"{parts[0]}.{parts[1]}".encode("ascii"))
    except Exception:
        return False
    return True


def _verify_signature_requirements(proof: str, method: str, url: str, *, max_skew_s: int = _ALLOWED_SKEW) -> bool:
    if _SIGNER is not None:
        try:
            verified = bool(
                _run_async(
                    _SIGNER.verify_bytes(
                        b"",
                        [{"sig": proof}],
                        require={
                            "htm": method.upper(),
                            "htu": url,
                            "algs": [_ALG_VALUE],
                            "max_skew_s": max_skew_s,
                        },
                    )
                )
            )
            if verified:
                return True
        except Exception:
            pass
    return _verify_fallback_signature(proof, method, url, max_skew_s=max_skew_s)


def make_proof(
    keyref: Any,
    method: str,
    url: str,
    *,
    access_token: str | None = None,
    nonce: str | None = None,
    enabled: bool | None = None,
) -> str:
    if enabled is None:
        enabled = settings.enable_rfc9449
    if not enabled:
        return ""
    if _SIGNER is not None:
        priv = getattr(keyref, "material", b"") or b""
        if isinstance(priv, str):
            priv = priv.encode()
        opts: dict[str, Any] = {"htm": method.upper(), "htu": url}
        if access_token:
            opts["ath"] = ath_for_access_token(access_token)
        if nonce:
            opts["nonce"] = str(nonce)
        sigs = _run_async(
            _SIGNER.sign_bytes(
                {"kind": "pem", "priv": priv},
                b"",
                alg=_ALG_VALUE,
                opts=opts,
            )
        )
        proof = sigs[0]["sig"]
        try:
            claims = proof_claims(proof)
            expected_ath = ath_for_access_token(access_token) if access_token is not None else None
            if expected_ath is not None and claims.ath != expected_ath:
                raise ValueError("ath mismatch")
            if nonce is not None and claims.nonce != str(nonce):
                raise ValueError("nonce mismatch")
            return proof
        except Exception:
            # Fallback to local Ed25519 compact-JWT signer when the runtime signer
            # omits required claims (ath/nonce) in dependency-light environments.
            pass

    private_key = _load_private_key(keyref)
    public_material = getattr(keyref, "public", None)
    if public_material in {None, b"", ""}:
        public_material = private_key.public_key()
    jwk = jwk_from_public_key(public_material)
    header = {"typ": _TYP_VALUE, "alg": _ALG_VALUE, "jwk": jwk}
    payload: dict[str, Any] = {
        "jti": secrets.token_urlsafe(24),
        "htm": method.upper(),
        "htu": url,
        "iat": int(time.time()),
    }
    if access_token is not None:
        payload["ath"] = ath_for_access_token(access_token)
    if nonce is not None:
        payload["nonce"] = str(nonce)
    signing_input = _compact_signing_input(header, payload)
    signature = private_key.sign(signing_input.encode("ascii"))
    return f"{signing_input}.{_b64url(signature)}"


makeProof = make_proof
create_proof = make_proof


def issue_nonce(*, ttl_s: int = _ALLOWED_SKEW, store: DPoPNonceStore | None = None) -> str:
    return (store or DEFAULT_NONCE_STORE).issue(ttl_s=ttl_s)


def register_nonce(nonce: str, *, ttl_s: int = _ALLOWED_SKEW, store: DPoPNonceStore | None = None) -> str:
    return (store or DEFAULT_NONCE_STORE).register(nonce, ttl_s=ttl_s)


def consume_nonce(nonce: str, *, store: DPoPNonceStore | None = None, now: int | None = None) -> bool:
    return (store or DEFAULT_NONCE_STORE).consume(nonce, now=now)


def replay_store_snapshot(store: DPoPReplayStore | None = None) -> dict[str, int]:
    return (store or DEFAULT_REPLAY_STORE).snapshot()


def clear_runtime_state() -> None:
    DEFAULT_REPLAY_STORE.clear()
    DEFAULT_NONCE_STORE.clear()


def verify_proof(
    proof: str,
    method: str,
    url: str,
    *,
    jkt: str | None = None,
    access_token: str | None = None,
    expected_nonce: str | None = None,
    require_nonce: bool = False,
    enabled: bool | None = None,
    replay_store: DPoPReplayStore | None = None,
    nonce_store: DPoPNonceStore | None = None,
) -> str:
    if enabled is None:
        enabled = settings.enable_rfc9449
    if not enabled:
        return ""
    claims = proof_claims(proof)
    if claims.htm != method.upper():
        raise ValueError(f"htm mismatch: {RFC9449_SPEC_URL}")
    if claims.htu != url:
        raise ValueError(f"htu mismatch: {RFC9449_SPEC_URL}")
    if claims.iat is None:
        raise ValueError(f"missing iat in DPoP proof: {RFC9449_SPEC_URL}")
    if abs(int(time.time()) - int(claims.iat)) > _ALLOWED_SKEW:
        raise ValueError(f"stale DPoP proof: {RFC9449_SPEC_URL}")
    valid = _verify_signature_requirements(proof, method, url)
    if not valid:
        raise ValueError(f"invalid DPoP proof: {RFC9449_SPEC_URL}")
    if jkt and claims.jkt != jkt:
        raise ValueError(f"jkt mismatch: {RFC9449_SPEC_URL}")
    if access_token is not None:
        expected_ath = ath_for_access_token(access_token)
        if claims.ath != expected_ath:
            raise ValueError(f"ath mismatch: {RFC9449_SPEC_URL}")
    if expected_nonce is not None:
        if claims.nonce != expected_nonce:
            raise ValueError(f"nonce mismatch: {RFC9449_SPEC_URL}")
        store = nonce_store or DEFAULT_NONCE_STORE
        if not store.consume(expected_nonce):
            raise ValueError(f"invalid or expired nonce: {RFC9449_SPEC_URL}")
    elif require_nonce and not claims.nonce:
        raise ValueError(f"nonce required: {RFC9449_SPEC_URL}")
    replay_key = ":".join((claims.jkt, claims.jti, claims.htm, claims.htu, claims.ath or ""))
    if (replay_store or DEFAULT_REPLAY_STORE).check_and_store(
        replay_key,
        now=claims.iat,
        ttl_s=_ALLOWED_SKEW,
    ):
        raise ValueError(f"replayed DPoP proof: {RFC9449_SPEC_URL}")
    return claims.jkt


def describe() -> dict[str, object]:
    return {
        "label": OWNER.label,
        "title": OWNER.title,
        "runtime_status": OWNER.runtime_status,
        "public_surface": list(OWNER.public_surface),
        "notes": OWNER.notes,
        "spec_url": RFC9449_SPEC_URL,
        "signing_alg_values_supported": [_ALG_VALUE],
        "ath_supported": True,
        "nonce_supported": True,
        "replay_detection_supported": True,
    }


__all__ = [
    "RFC9449_SPEC_URL",
    "DPoPNonceRecord",
    "DPoPNonceStore",
    "DPoPProofClaims",
    "DPoPReplayStore",
    "StandardOwner",
    "OWNER",
    "access_token_hash",
    "ath_for_access_token",
    "clear_runtime_state",
    "consume_nonce",
    "create_proof",
    "decode_proof",
    "describe",
    "issue_nonce",
    "jwk_from_public_key",
    "jwk_thumbprint",
    "makeProof",
    "make_proof",
    "proof_claims",
    "register_nonce",
    "replay_store_snapshot",
    "verify_proof",
]
