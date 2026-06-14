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

from tigrbl_identity_runtime.settings import settings

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


