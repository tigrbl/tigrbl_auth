"""OAuth 2.0 JWT-Secured Authorization Request owner and runtime helpers.

The active repository profile keeps a deliberately bounded JAR implementation:

- compact JWS request objects only
- signed request objects only (`alg=none` is rejected)
- HMAC request-object signatures using `HS256` / `HS384` / `HS512`
- temporal validation for `exp`, `nbf`, and `iat` when present
- client and audience consistency checks when the caller provides expectations
- deterministic merge semantics between query/form parameters and request-object claims

The helpers stay dependency-light so targeted standards tests and evidence can run
without importing the full Tigrbl runtime stack.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
from datetime import datetime, timedelta, timezone
from typing import Any, Final, Iterable, Mapping, Sequence
from tigrbl_identity_core.standards import StandardOwner, describe_owner
from tigrbl_identity_contracts.oauth import RequestObjectPolicy

from tigrbl_identity_contracts.protocol_configuration import (
    protocol_settings as settings,
)

STATUS: Final[str] = "request-object-runtime"
RFC9101_SPEC_URL: Final[str] = "https://www.rfc-editor.org/rfc/rfc9101"
SUPPORTED_JAR_ALG_VALUES: Final[tuple[str, ...]] = ("HS256", "HS384", "HS512")
DEFAULT_REQUEST_OBJECT_LIFETIME_SECONDS: Final[int] = 300
DEFAULT_CLOCK_SKEW_SECONDS: Final[int] = 60


OWNER = StandardOwner(
    label="RFC 9101",
    title="OAuth 2.0 JWT-Secured Authorization Request (JAR)",
    runtime_status=STATUS,
    public_surface=("/authorize", "/par"),
    notes=(
        "Canonical standards-tree owner module for request-object signing, verification, "
        "temporal validation, and parameter-consistency enforcement wired into the "
        "authorization and PAR release path."
    ),
)

ACTIVE_REQUEST_OBJECT_POLICY: Final[RequestObjectPolicy] = RequestObjectPolicy()


class RequestObjectValidationError(ValueError):
    """Raised when a request object violates the active bounded JAR profile."""


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def _b64url_decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(value + padding)


def _json_dumps(payload: Mapping[str, Any]) -> str:
    return json.dumps(payload, separators=(",", ":"), sort_keys=True)


def _normalize_secret(secret: str | bytes | bytearray) -> bytes:
    if isinstance(secret, (bytes, bytearray)):
        return bytes(secret)
    return str(secret).encode("utf-8")


def _validate_algorithm(
    algorithm: str, *, policy: RequestObjectPolicy = ACTIVE_REQUEST_OBJECT_POLICY
) -> str:
    alg = str(algorithm or "").upper()
    if not alg:
        raise RequestObjectValidationError(
            f"missing JAR signing algorithm: {RFC9101_SPEC_URL}"
        )
    if alg == "NONE":
        raise RequestObjectValidationError(
            f"unsigned request objects are not accepted: {RFC9101_SPEC_URL}"
        )
    if alg not in policy.allowed_algs:
        raise RequestObjectValidationError(
            f"unsupported request-object signing algorithm {alg!r}; supported values: {', '.join(policy.allowed_algs)}"
        )
    return alg


def _hash_name_for_alg(algorithm: str) -> str:
    alg = _validate_algorithm(algorithm)
    if alg == "HS256":
        return "sha256"
    if alg == "HS384":
        return "sha384"
    return "sha512"


def _sign_compact_jws(
    payload: Mapping[str, Any], *, secret: str | bytes | bytearray, algorithm: str
) -> str:
    alg = _validate_algorithm(algorithm)
    header = {"alg": alg, "typ": "JWT"}
    signing_input = ".".join(
        (
            _b64url_encode(_json_dumps(header).encode("utf-8")),
            _b64url_encode(_json_dumps(dict(payload)).encode("utf-8")),
        )
    )
    signature = hmac.new(
        _normalize_secret(secret),
        signing_input.encode("ascii"),
        getattr(hashlib, _hash_name_for_alg(alg)),
    ).digest()
    return f"{signing_input}.{_b64url_encode(signature)}"


def _verify_compact_jws(
    token: str,
    *,
    secret: str | bytes | bytearray,
    algorithms: Iterable[str] | None = None,
    policy: RequestObjectPolicy = ACTIVE_REQUEST_OBJECT_POLICY,
) -> tuple[dict[str, Any], dict[str, Any]]:
    try:
        header_segment, payload_segment, signature_segment = token.split(".")
    except ValueError as exc:
        raise RequestObjectValidationError(
            f"invalid compact request object: {RFC9101_SPEC_URL}"
        ) from exc
    try:
        header = json.loads(_b64url_decode(header_segment).decode("utf-8"))
    except Exception as exc:
        raise RequestObjectValidationError(
            f"invalid request-object header encoding: {RFC9101_SPEC_URL}"
        ) from exc
    if not isinstance(header, dict):
        raise RequestObjectValidationError(
            f"invalid request-object header: {RFC9101_SPEC_URL}"
        )
    alg = _validate_algorithm(str(header.get("alg") or ""), policy=policy)
    allowlist = tuple(
        _validate_algorithm(item, policy=policy)
        for item in (algorithms or policy.allowed_algs)
    )
    if alg not in allowlist:
        raise RequestObjectValidationError(
            f"request-object signature algorithm {alg!r} is not permitted: {RFC9101_SPEC_URL}"
        )
    expected_sig = hmac.new(
        _normalize_secret(secret),
        f"{header_segment}.{payload_segment}".encode("ascii"),
        getattr(hashlib, _hash_name_for_alg(alg)),
    ).digest()
    try:
        actual_sig = _b64url_decode(signature_segment)
    except Exception as exc:
        raise RequestObjectValidationError(
            f"invalid request-object signature encoding: {RFC9101_SPEC_URL}"
        ) from exc
    if not hmac.compare_digest(expected_sig, actual_sig):
        raise RequestObjectValidationError(
            f"request-object signature verification failed: {RFC9101_SPEC_URL}"
        )
    try:
        payload = json.loads(_b64url_decode(payload_segment).decode("utf-8"))
    except Exception as exc:
        raise RequestObjectValidationError(
            f"invalid request-object payload encoding: {RFC9101_SPEC_URL}"
        ) from exc
    if not isinstance(payload, dict):
        raise RequestObjectValidationError(
            f"request-object payload must be a JSON object: {RFC9101_SPEC_URL}"
        )
    return header, payload


def _utc_now(now: datetime | None = None) -> datetime:
    value = now or datetime.now(timezone.utc)
    return value if value.tzinfo is not None else value.replace(tzinfo=timezone.utc)


def _as_timestamp(value: Any) -> int | None:
    if value in {None, ""}:
        return None
    if isinstance(value, bool):
        raise RequestObjectValidationError(
            f"invalid temporal claim type in request object: {RFC9101_SPEC_URL}"
        )
    try:
        return int(value)
    except Exception as exc:
        raise RequestObjectValidationError(
            f"invalid temporal claim in request object: {RFC9101_SPEC_URL}"
        ) from exc


def _audience_matches(expected_audience: str, aud_claim: Any) -> bool:
    if isinstance(aud_claim, str):
        return aud_claim == expected_audience
    if isinstance(aud_claim, Sequence) and not isinstance(
        aud_claim, (bytes, bytearray, str)
    ):
        return expected_audience in {str(item) for item in aud_claim}
    return False


def validate_request_object_claims(
    payload: Mapping[str, Any],
    *,
    expected_client_id: str | None = None,
    expected_audience: str | None = None,
    now: datetime | None = None,
    require_expiration: bool = False,
    policy: RequestObjectPolicy = ACTIVE_REQUEST_OBJECT_POLICY,
) -> dict[str, Any]:
    normalized = dict(payload)
    current = _utc_now(now)
    skew = timedelta(seconds=policy.max_clock_skew_seconds)

    exp = _as_timestamp(normalized.get("exp"))
    nbf = _as_timestamp(normalized.get("nbf"))
    iat = _as_timestamp(normalized.get("iat"))

    if require_expiration and exp is None:
        raise RequestObjectValidationError(
            f"request objects must include exp in the active profile: {RFC9101_SPEC_URL}"
        )
    if (
        exp is not None
        and datetime.fromtimestamp(exp, tz=timezone.utc) <= current - skew
    ):
        raise RequestObjectValidationError(
            f"stale request object rejected by temporal policy: {RFC9101_SPEC_URL}"
        )
    if (
        nbf is not None
        and datetime.fromtimestamp(nbf, tz=timezone.utc) > current + skew
    ):
        raise RequestObjectValidationError(
            f"request object is not yet valid: {RFC9101_SPEC_URL}"
        )
    if (
        iat is not None
        and datetime.fromtimestamp(iat, tz=timezone.utc) > current + skew
    ):
        raise RequestObjectValidationError(
            f"request object iat is in the future: {RFC9101_SPEC_URL}"
        )
    if exp is not None and iat is not None and exp <= iat:
        raise RequestObjectValidationError(
            f"request object exp must be greater than iat: {RFC9101_SPEC_URL}"
        )
    if exp is not None and nbf is not None and exp <= nbf:
        raise RequestObjectValidationError(
            f"request object exp must be greater than nbf: {RFC9101_SPEC_URL}"
        )

    if expected_client_id:
        claim_client_id = str(normalized.get("client_id") or "").strip() or None
        issuer = str(normalized.get("iss") or "").strip() or None
        subject = str(normalized.get("sub") or "").strip() or None
        if claim_client_id is not None and claim_client_id != expected_client_id:
            raise RequestObjectValidationError(
                f"request object client_id mismatch: {RFC9101_SPEC_URL}"
            )
        if issuer is not None and issuer != expected_client_id:
            raise RequestObjectValidationError(
                f"request object iss/client mismatch: {RFC9101_SPEC_URL}"
            )
        if subject is not None and subject != expected_client_id:
            raise RequestObjectValidationError(
                f"request object sub/client mismatch: {RFC9101_SPEC_URL}"
            )
    if expected_audience:
        aud = normalized.get("aud")
        if aud not in {None, ""} and not _audience_matches(expected_audience, aud):
            raise RequestObjectValidationError(
                f"request object audience mismatch: {RFC9101_SPEC_URL}"
            )
    return normalized


def merge_request_object_params(
    request_object_claims: Mapping[str, Any],
    request_params: Mapping[str, Any],
    *,
    allow_query_overrides: Iterable[str] = (),
) -> dict[str, Any]:
    merged = dict(request_object_claims)
    override_keys = {str(item) for item in allow_query_overrides}
    for key, value in request_params.items():
        if key == "request":
            continue
        if value in (None, "", [], (), {}):
            continue
        existing = merged.get(key)
        if key in override_keys:
            merged[key] = value
            continue
        if existing not in (None, "", [], (), {}) and existing != value:
            raise RequestObjectValidationError(
                f"conflicting query/form parameter {key!r} does not match request-object claim: {RFC9101_SPEC_URL}"
            )
        merged[key] = value
    return merged


async def make_request_object(
    params: dict[str, Any],
    *,
    secret: str,
    algorithm: str = "HS256",
    issuer: str | None = None,
    audience: str | None = None,
    lifetime_seconds: int = DEFAULT_REQUEST_OBJECT_LIFETIME_SECONDS,
) -> str:
    if not settings.enable_rfc9101:
        raise RuntimeError(f"RFC 9101 support disabled: {RFC9101_SPEC_URL}")
    payload = dict(params)
    now = _utc_now()
    payload.setdefault("iat", int(now.timestamp()))
    payload.setdefault(
        "exp", int((now + timedelta(seconds=max(1, int(lifetime_seconds)))).timestamp())
    )
    if issuer is not None:
        payload.setdefault("iss", issuer)
        payload.setdefault("sub", issuer)
    if audience is not None:
        payload.setdefault("aud", audience)
    return _sign_compact_jws(payload, secret=secret, algorithm=algorithm)


async def makeRequestObject(
    params: dict[str, Any],
    *,
    secret: str,
    algorithm: str = "HS256",
) -> str:
    return await make_request_object(params, secret=secret, algorithm=algorithm)


async def create_request_object(
    params: dict[str, Any],
    *,
    secret: str,
    algorithm: str = "HS256",
) -> str:
    return await makeRequestObject(params, secret=secret, algorithm=algorithm)


async def parse_request_object(
    token: str,
    *,
    secret: str,
    algorithms: Iterable[str] | None = None,
    expected_client_id: str | None = None,
    expected_audience: str | None = None,
    now: datetime | None = None,
    require_expiration: bool = False,
) -> dict[str, Any]:
    if not settings.enable_rfc9101:
        raise RuntimeError(f"RFC 9101 support disabled: {RFC9101_SPEC_URL}")
    _header, payload = _verify_compact_jws(token, secret=secret, algorithms=algorithms)
    return validate_request_object_claims(
        payload,
        expected_client_id=expected_client_id,
        expected_audience=expected_audience,
        now=now,
        require_expiration=require_expiration,
    )


def request_object_summary(payload: Mapping[str, Any]) -> dict[str, Any]:
    claims = dict(payload)
    return {
        "claim_keys": sorted(claims.keys()),
        "client_id": claims.get("client_id"),
        "iss": claims.get("iss"),
        "sub": claims.get("sub"),
        "aud": claims.get("aud"),
        "has_exp": "exp" in claims,
        "has_nbf": "nbf" in claims,
        "has_iat": "iat" in claims,
    }


def describe() -> dict[str, object]:
    return describe_owner(
        OWNER,
        allowed_algs=list(ACTIVE_REQUEST_OBJECT_POLICY.allowed_algs),
        require_signature=ACTIVE_REQUEST_OBJECT_POLICY.require_signature,
        clock_skew_seconds=ACTIVE_REQUEST_OBJECT_POLICY.max_clock_skew_seconds,
        spec_url=RFC9101_SPEC_URL,
    )


__all__ = [
    "STATUS",
    "RFC9101_SPEC_URL",
    "SUPPORTED_JAR_ALG_VALUES",
    "DEFAULT_REQUEST_OBJECT_LIFETIME_SECONDS",
    "StandardOwner",
    "RequestObjectPolicy",
    "RequestObjectValidationError",
    "OWNER",
    "ACTIVE_REQUEST_OBJECT_POLICY",
    "make_request_object",
    "makeRequestObject",
    "create_request_object",
    "parse_request_object",
    "validate_request_object_claims",
    "merge_request_object_params",
    "request_object_summary",
    "describe",
]
