from __future__ import annotations

import json
import secrets
import time
import inspect
from typing import Any

from tigrbl_identity_core.standards import describe_owner
from tigrbl_identity_runtime.settings import settings
from tigrbl_security_trust_contracts import DPoPNonceRecord, DPoPProofClaims

from .primitives import (
    OWNER,
    RFC9449_SPEC_URL,
    Ed25519PublicKey,
    StandardOwner,
    _ALG_VALUE,
    _ALLOWED_SKEW,
    _SIGNER,
    _TYP_VALUE,
    _b64url,
    _b64url_decode,
    _compact_signing_input,
    _load_private_key,
    _run_async,
    access_token_hash,
    ath_for_access_token,
    jwk_from_public_key,
    jwk_thumbprint,
)

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


async def _verify_signature_requirements_async(
    proof: str,
    method: str,
    url: str,
    *,
    max_skew_s: int = _ALLOWED_SKEW,
) -> bool:
    if _SIGNER is not None:
        try:
            verified = bool(
                await _SIGNER.verify_bytes(
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
            if verified:
                return True
        except Exception:
            pass
    return _verify_fallback_signature(proof, method, url, max_skew_s=max_skew_s)


async def _maybe_await(value: Any) -> Any:
    if inspect.isawaitable(value):
        return await value
    return value


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


def _require_callable(fn: Any | None, purpose: str) -> Any:
    if not callable(fn):
        raise RuntimeError(f"{purpose} requires an injected DPoP table-backed operation")
    return fn


def issue_nonce(*, ttl_s: int = _ALLOWED_SKEW, issuer: Any | None = None) -> str:
    return _require_callable(issuer, "issue_nonce")(ttl_s=ttl_s)


async def issue_nonce_async(*, ttl_s: int = _ALLOWED_SKEW, issuer: Any | None = None) -> str:
    return await _maybe_await(_require_callable(issuer, "issue_nonce_async")(ttl_s=ttl_s))


def register_nonce(nonce: str, *, ttl_s: int = _ALLOWED_SKEW, registrar: Any | None = None) -> str:
    return _require_callable(registrar, "register_nonce")(nonce, ttl_s=ttl_s)


async def register_nonce_async(nonce: str, *, ttl_s: int = _ALLOWED_SKEW, registrar: Any | None = None) -> str:
    return await _maybe_await(_require_callable(registrar, "register_nonce_async")(nonce, ttl_s=ttl_s))


def consume_nonce(nonce: str, *, consumer: Any | None = None, now: int | None = None) -> bool:
    return _require_callable(consumer, "consume_nonce")(nonce, now=now)


async def consume_nonce_async(nonce: str, *, consumer: Any | None = None, now: int | None = None) -> bool:
    return await _maybe_await(_require_callable(consumer, "consume_nonce_async")(nonce, now=now))


def replay_table_snapshot(snapshotter: Any | None = None) -> dict[str, int]:
    return _require_callable(snapshotter, "replay_table_snapshot")()


async def replay_table_snapshot_async(snapshotter: Any | None = None) -> dict[str, int]:
    return await _maybe_await(_require_callable(snapshotter, "replay_table_snapshot_async")())


def clear_runtime_state() -> None:
    raise RuntimeError("clear_runtime_state requires clearing the configured DPoP tables")


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
    replay_checker: Any | None = None,
    nonce_consumer: Any | None = None,
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
        consumer = _require_callable(nonce_consumer, "expected_nonce validation")
        if not consumer(expected_nonce):
            raise ValueError(f"invalid or expired nonce: {RFC9449_SPEC_URL}")
    elif require_nonce and not claims.nonce:
        raise ValueError(f"nonce required: {RFC9449_SPEC_URL}")
    checker = _require_callable(replay_checker, "verify_proof")
    if checker(claims, ttl_s=_ALLOWED_SKEW):
        raise ValueError(f"replayed DPoP proof: {RFC9449_SPEC_URL}")
    return claims.jkt


async def verify_proof_async(
    proof: str,
    method: str,
    url: str,
    *,
    jkt: str | None = None,
    access_token: str | None = None,
    expected_nonce: str | None = None,
    require_nonce: bool = False,
    enabled: bool | None = None,
    replay_checker: Any | None = None,
    nonce_consumer: Any | None = None,
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
    valid = await _verify_signature_requirements_async(proof, method, url)
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
        consumer = _require_callable(nonce_consumer, "expected_nonce validation")
        if not await _maybe_await(consumer(expected_nonce)):
            raise ValueError(f"invalid or expired nonce: {RFC9449_SPEC_URL}")
    elif require_nonce and not claims.nonce:
        raise ValueError(f"nonce required: {RFC9449_SPEC_URL}")

    checker = _require_callable(replay_checker, "verify_proof_async")
    replayed = await _maybe_await(checker(claims, ttl_s=_ALLOWED_SKEW))
    if replayed:
        raise ValueError(f"replayed DPoP proof: {RFC9449_SPEC_URL}")
    return claims.jkt


def describe() -> dict[str, object]:
    return describe_owner(
        OWNER,
        spec_url=RFC9449_SPEC_URL,
        signing_alg_values_supported=[_ALG_VALUE],
        ath_supported=True,
        nonce_supported=True,
        replay_detection_supported=True,
    )


__all__ = [
    "RFC9449_SPEC_URL",
    "DPoPNonceRecord",
    "DPoPProofClaims",
    "StandardOwner",
    "OWNER",
    "access_token_hash",
    "ath_for_access_token",
    "clear_runtime_state",
    "consume_nonce",
    "consume_nonce_async",
    "create_proof",
    "decode_proof",
    "describe",
    "issue_nonce",
    "issue_nonce_async",
    "jwk_from_public_key",
    "jwk_thumbprint",
    "makeProof",
    "make_proof",
    "proof_claims",
    "register_nonce",
    "register_nonce_async",
    "replay_table_snapshot",
    "replay_table_snapshot_async",
    "verify_proof_async",
    "verify_proof",
]
