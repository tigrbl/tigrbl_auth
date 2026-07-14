"""Request-scoped composition for durable OAuth token issuance."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from copy import deepcopy
import inspect
from typing import Any, Protocol
from uuid import UUID, uuid4

from tigrbl_auth_protocol_oauth.standards.token_endpoint import (
    RFC6749TokenEndpointService,
)
from tigrbl_identity_contracts.tokens import (
    IssuedTokenPair,
    RefreshTokenRedemptionRequest,
    TokenPairIssueRequest,
)
from tigrbl_identity_core.digests import token_hash
from tigrbl_identity_core.errors import (
    InvalidRefreshTokenError,
    RefreshTokenReuseError,
)
from tigrbl_identity_storage_runtime.ops.audit import append_audit_event_record
from tigrbl_identity_storage_runtime.ops.common import field_value
from tigrbl_identity_storage_runtime.ops.oauth_state import (
    record_revoked_token_hash,
)
from tigrbl_identity_storage_runtime.ops.tokens import (
    mark_refresh_token_rotated,
    persist_issued_token,
    read_token_record,
    revoke_refresh_token_family,
)
from tigrbl_token_issuance_capability import TokenIssuanceCapability


class TokenCoder(Protocol):
    async def async_sign_pair(self, **kwargs: Any) -> tuple[str, str]: ...

    async def async_decode(self, token: str, **kwargs: Any) -> dict[str, Any]: ...


def _uuid_or_value(value: object) -> object:
    if isinstance(value, UUID):
        return value
    try:
        return UUID(str(value))
    except (TypeError, ValueError, AttributeError):
        return value


def _normalize_audience(value: object) -> str | list[str] | None:
    if value is None or value == "":
        return None
    if isinstance(value, str):
        return value
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [str(item) for item in value]
    return str(value)


def _audience_allows(stored: str | list[str] | None, requested: str | None) -> bool:
    if not requested or stored is None:
        return True
    if isinstance(stored, str):
        return stored == requested
    return requested in stored


async def _decode_issued_claims(coder: TokenCoder, token: str) -> dict[str, Any]:
    decode = coder.async_decode
    try:
        parameters = inspect.signature(decode).parameters
    except (TypeError, ValueError):
        parameters = {}
    supports_revocation_switch = "verify_revocation" in parameters or any(
        parameter.kind is inspect.Parameter.VAR_KEYWORD
        for parameter in parameters.values()
    )
    kwargs: dict[str, object] = {"verify_exp": False}
    if supports_revocation_switch:
        kwargs["verify_revocation"] = False
    return dict(await decode(token, **kwargs))


def build_token_issuance_capability(
    *,
    db: Any,
    token_coder: TokenCoder,
) -> TokenIssuanceCapability:
    """Bind cryptography and durable aliases to one request-scoped session."""

    async def issue(request: TokenPairIssueRequest) -> IssuedTokenPair:
        claims = dict(request.extra_claims)
        if request.scope:
            claims["scope"] = request.scope
        if request.audience is not None:
            claims["audience"] = request.audience
        claims["issuer"] = request.issuer
        if request.confirmation:
            claims["cnf"] = dict(request.confirmation)

        access_token, refresh_token = await token_coder.async_sign_pair(
            sub=request.subject,
            tid=request.tenant_id,
            cert_thumbprint=request.certificate_thumbprint,
            persist_token=False,
            **claims,
        )
        access_claims = await _decode_issued_claims(token_coder, access_token)
        refresh_claims = await _decode_issued_claims(token_coder, refresh_token)
        for issued_claims in (access_claims, refresh_claims):
            issued_claims["client_id"] = request.client_id
            for name in ("authorization_trace", "delegation_provenance"):
                if name in request.extra_claims:
                    issued_claims[name] = deepcopy(request.extra_claims[name])

        family_id = request.refresh_family_id or str(uuid4())
        parent_hash = (
            token_hash(request.refresh_parent_token)
            if request.refresh_parent_token
            else None
        )
        common = {
            "refresh_family_id": family_id,
            "refresh_parent_hash": parent_hash,
        }
        await persist_issued_token(
            {
                "payload": {
                    "token_hash": token_hash(access_token),
                    "claims": access_claims,
                    "token_kind": "access",
                    "token_profile": "oauth-access-token",
                    "token_type_hint": "access_token",
                    **common,
                },
                "db": db,
            }
        )
        await persist_issued_token(
            {
                "payload": {
                    "token_hash": token_hash(refresh_token),
                    "claims": refresh_claims,
                    "token_kind": "refresh",
                    "token_profile": "oauth-refresh-token",
                    "token_type_hint": "refresh_token",
                    **common,
                },
                "db": db,
            }
        )
        return IssuedTokenPair(access_token, refresh_token, request.token_type)

    async def redeem(request: RefreshTokenRedemptionRequest) -> IssuedTokenPair:
        digest = token_hash(request.refresh_token)
        record = await read_token_record(
            {"payload": {"token_hash": digest}, "db": db}
        )
        if record is None:
            raise InvalidRefreshTokenError(
                "refresh token was not issued by this repository"
            )
        if field_value(record, "token_kind") != "refresh":
            raise InvalidRefreshTokenError("presented token is not a refresh token")
        record_client_id = str(field_value(record, "client_id") or "")
        if record_client_id not in {"", request.client_id}:
            raise InvalidRefreshTokenError("refresh token client binding mismatch")

        family_id = str(field_value(record, "refresh_family_id") or "")
        if field_value(record, "used_at") is not None or field_value(
            record, "refresh_successor_hash"
        ):
            if family_id:
                rows = await revoke_refresh_token_family(
                    {
                        "payload": {
                            "refresh_family_id": family_id,
                            "reason": "refresh_token_reuse_detected",
                            "reuse_token_hash": digest,
                        },
                        "db": db,
                    }
                )
                for row in rows:
                    await record_revoked_token_hash(
                        {
                            "payload": {
                                "token_hash": field_value(row, "token_hash"),
                                "token_type_hint": field_value(
                                    row, "token_type_hint"
                                ),
                                "refresh_family_id": family_id,
                                "reason": "refresh_token_reuse_detected",
                                "subject": field_value(row, "subject"),
                                "tenant_id": field_value(row, "tenant_id"),
                                "client_id": field_value(row, "client_id"),
                                "expires_at": field_value(row, "expires_at"),
                            },
                            "db": db,
                        }
                    )
            raise RefreshTokenReuseError("refresh token replay detected")
        if not field_value(record, "active", False) or field_value(
            record, "revoked_at"
        ) is not None:
            raise InvalidRefreshTokenError("refresh token is inactive")

        claims = dict(
            await token_coder.async_decode(
                request.refresh_token,
                verify_exp=True,
                cert_thumbprint=request.certificate_thumbprint,
            )
        )
        if claims.get("typ") != "refresh":
            raise InvalidRefreshTokenError("presented token is not a refresh token")
        token_client_id = str(claims.get("client_id") or record_client_id or "")
        if token_client_id not in {"", request.client_id}:
            raise InvalidRefreshTokenError("refresh token client binding mismatch")

        stored_claims = field_value(record, "claims")
        recorded = dict(stored_claims) if isinstance(stored_claims, Mapping) else {}
        stored_audience = _normalize_audience(recorded.get("aud"))
        if not _audience_allows(stored_audience, request.requested_audience):
            raise InvalidRefreshTokenError(
                "refresh token audience cannot be widened or changed"
            )

        preserved = deepcopy(recorded or claims)
        for name in (
            "iat",
            "exp",
            "nbf",
            "jti",
            "typ",
            "sub",
            "tid",
            "client_id",
            "cnf",
        ):
            preserved.pop(name, None)
        next_audience = request.requested_audience or _normalize_audience(
            preserved.pop("aud", None)
        )
        next_scope = preserved.pop("scope", None)
        next_issuer = str(preserved.pop("iss", None) or claims.get("iss") or "")
        confirmation = claims.get("cnf")

        result = await issue(
            TokenPairIssueRequest(
                subject=str(claims.get("sub") or field_value(record, "subject") or ""),
                tenant_id=str(
                    claims.get("tid")
                    or field_value(record, "tenant_id")
                    or request.tenant_id
                ),
                client_id=request.client_id,
                issuer=next_issuer,
                scope=str(next_scope) if next_scope is not None else None,
                audience=next_audience,
                certificate_thumbprint=request.certificate_thumbprint,
                confirmation=(
                    dict(confirmation) if isinstance(confirmation, Mapping) else None
                ),
                refresh_family_id=family_id or None,
                refresh_parent_token=request.refresh_token,
                token_type=request.token_type,
                extra_claims=preserved,
            )
        )
        await mark_refresh_token_rotated(
            {
                "payload": {
                    "token_hash": digest,
                    "successor_hash": (
                        token_hash(result.refresh_token)
                        if result.refresh_token
                        else None
                    ),
                    "reason": "refresh_rotated",
                },
                "db": db,
            }
        )
        return result

    async def audit(event: Mapping[str, object]) -> None:
        details = event.get("details")
        await append_audit_event_record(
            {
                "payload": {
                    "tenant_id": _uuid_or_value(event.get("tenant_id")),
                    "actor_client_id": _uuid_or_value(
                        event.get("actor_client_id")
                    ),
                    "event_type": str(event.get("event_type") or "token.issued"),
                    "target_type": str(event.get("target_type") or "token"),
                    "target_id": str(event.get("target_id") or ""),
                    "details": (
                        dict(details) if isinstance(details, Mapping) else {}
                    ),
                },
                "db": db,
            }
        )

    return TokenIssuanceCapability(issue, redeem, audit)


def build_rfc6749_token_endpoint_service(
    *,
    db: Any,
    token_coder: TokenCoder,
    enabled: bool = True,
) -> RFC6749TokenEndpointService:
    return RFC6749TokenEndpointService(
        build_token_issuance_capability(db=db, token_coder=token_coder),
        enabled=enabled,
    )


__all__ = [
    "TokenCoder",
    "build_rfc6749_token_endpoint_service",
    "build_token_issuance_capability",
]
