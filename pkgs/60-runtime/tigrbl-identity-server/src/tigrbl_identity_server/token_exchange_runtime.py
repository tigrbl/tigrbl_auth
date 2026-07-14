"""RFC 8693 token-exchange orchestration over normalized capabilities."""

from __future__ import annotations

import hashlib
from typing import Any, Dict, Final
from urllib.parse import parse_qs

from tigrbl import Request
from tigrbl.runtime.status import HTTPException, status
from tigrbl_identity_contracts.oauth.exchange import (
    TokenExchangeContext,
    TokenExchangeRequest,
    TokenExchangeResponse,
    TokenExchangeSenderConstraint,
)
from tigrbl_identity_runtime.settings import settings
from tigrbl_identity_runtime.deployment import deployment_from_request
from tigrbl_identity_core.errors import InvalidTokenError
from tigrbl_security_authorization_provenance_builder import (
    build_authorization_decision_trace,
    build_delegation_provenance,
)
from tigrbl_identity_jose.jwt_coder import JWTCoder
from tigrbl_auth_protocol_oauth.standards.resource_indicators import select_resource_indicator
from tigrbl_auth_protocol_oauth.standards.resource_verifier_contract import build_protected_resource_verifier_contract
from tigrbl_auth_protocol_oauth.standards.authorization_server_metadata import ISSUER
from tigrbl_auth_protocol_oauth.standards.oauth_security_bcp import (
    TOKEN_EXCHANGE_GRANT_TYPE,
    OAuthPolicyViolation,
    dpop_proof_from_request,
    validate_sender_constraint,
)
from tigrbl_token_exchange_capability import TokenExchangeCapability

from tigrbl_identity_storage_runtime.ops.audit import append_audit_event_async
from tigrbl_identity_storage_runtime.revocation import is_revoked_async
from tigrbl_identity_storage_runtime.token_persistence import upsert_token_record_async


RFC8693_SPEC_URL: Final[str] = 'https://www.rfc-editor.org/rfc/rfc8693'
SUPPORTED_REQUESTED_TOKEN_TYPES: Final[tuple[str, ...]] = (
    'urn:ietf:params:oauth:token-type:access_token',
    'access_token',
)




_jwt_coder: JWTCoder | None = None



async def _get_jwt_coder() -> JWTCoder:
    global _jwt_coder
    if _jwt_coder is not None:
        candidate = _jwt_coder
        if callable(candidate) and not hasattr(candidate, "async_decode"):
            candidate = candidate()
        if hasattr(candidate, "__await__"):
            candidate = await candidate
        return candidate
    _jwt_coder = await JWTCoder.async_default(
        revocation_checker=is_revoked_async,
    )
    return _jwt_coder



def _parse_form(request: Request) -> Dict[str, str | list[str]]:
    body = getattr(request, 'body', b'') or b''
    parsed = parse_qs(body.decode('utf-8'), keep_blank_values=True)
    payload: Dict[str, str | list[str]] = {}
    for key, values in parsed.items():
        payload[key] = values[-1] if len(values) == 1 else values
    return payload



def _normalize_requested_token_type(value: Any) -> str:
    requested = str(value or SUPPORTED_REQUESTED_TOKEN_TYPES[0])
    if requested not in SUPPORTED_REQUESTED_TOKEN_TYPES:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, {'error': 'invalid_request', 'error_description': 'unsupported requested_token_type'})
    return requested



def _actor_claim(actor_claims: dict[str, Any] | None) -> dict[str, str] | None:
    if not actor_claims:
        return None
    actor_sub = str(actor_claims.get('sub') or '')
    if not actor_sub:
        return None
    return {'sub': actor_sub}


def _header_value(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        stripped = value.strip()
        return stripped or None
    return None


def _hash_token(value: str | None) -> str | None:
    if not value:
        return None
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


async def token_exchange(
    request: Request,
    dpop: str | None = None,
) -> dict[str, object]:
    """Materialize an RFC 8693 request and delegate normalized execution."""

    deployment = deployment_from_request(request, settings)
    if not deployment.flag_enabled('enable_rfc8693'):
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'RFC 8693 disabled: {RFC8693_SPEC_URL}')
    data = _parse_form(request)
    if data.get('grant_type') != TOKEN_EXCHANGE_GRANT_TYPE:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, {'error': 'unsupported_grant_type'})
    requested_token_type = _normalize_requested_token_type(data.get('requested_token_type'))
    try:
        resources = data.get('resource', ())
        resource_values = (
            tuple(str(item) for item in resources)
            if isinstance(resources, list)
            else ((str(resources),) if resources else ())
        )
        exchange_request = TokenExchangeRequest(
            subject_token=str(data.get('subject_token') or ''),
            subject_token_type=str(data.get('subject_token_type') or ''),
            actor_token=str(data.get('actor_token') or '') or None,
            actor_token_type=str(data.get('actor_token_type') or '') or None,
            resources=resource_values,
            audience=str(data.get('audience') or '') or None,
            scope=str(data.get('scope') or '') or None,
            requested_token_type=requested_token_type,
            delegation_grant_id=(
                str(data.get('delegation_grant_id') or '').strip() or None
            ),
        )
    except ValueError as exc:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            {'error': 'invalid_request', 'error_description': str(exc)},
        ) from exc

    try:
        if exchange_request.resources:
            select_resource_indicator(
                list(exchange_request.resources),
                audience=exchange_request.audience,
            )
    except ValueError as exc:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            {'error': 'invalid_target'},
        ) from exc

    try:
        sender_constraint = validate_sender_constraint(
            request,
            deployment,
            dpop_proof=_header_value(dpop) or dpop_proof_from_request(request),
        )
    except OAuthPolicyViolation as exc:
        raise HTTPException(exc.status_code, {'error': exc.error, 'error_description': exc.description}) from exc
    except ValueError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, {'error': 'invalid_dpop_proof'}) from exc

    verifier_contract = build_protected_resource_verifier_contract(deployment)
    protected_resource_identifier = (
        getattr(deployment, 'protected_resource_identifier', None)
        or settings.protected_resource_identifier
    )
    context = TokenExchangeContext(
        issuer=str(deployment.issuer or ISSUER),
        protected_resource_identifier=(
            str(protected_resource_identifier)
            if protected_resource_identifier
            else None
        ),
        sender_constraint=TokenExchangeSenderConstraint(
            mechanism=sender_constraint.mechanism,
            token_type=sender_constraint.token_type,
            confirmation_claim=sender_constraint.confirmation_claim,
            certificate_thumbprint=sender_constraint.cert_thumbprint,
        ),
        verifier_logic_id=verifier_contract.verifier_logic_id,
        required_claims=tuple(verifier_contract.required_claims),
    )
    result = await token_exchange_capability.exchange(
        exchange_request,
        context=context,
    )
    return result.to_mapping()


def _audience_claim(claims: dict[str, Any]) -> str | None:
    value = claims.get('aud')
    if isinstance(value, str):
        return value or None
    if isinstance(value, (list, tuple)):
        return str(value[0]) if value else None
    return str(value) if value is not None else None


async def _exchange_token(
    request: TokenExchangeRequest,
    context: TokenExchangeContext,
) -> TokenExchangeResponse:
    """Execute normalized exchange semantics and durable observation."""

    jwt = await _get_jwt_coder()
    try:
        subject_claims = await jwt.async_decode(request.subject_token, verify_exp=True)
    except (InvalidTokenError, ValueError) as exc:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            {'error': 'invalid_request', 'error_description': 'invalid subject_token'},
        ) from exc

    actor_claims: dict[str, Any] | None = None
    if request.actor_token:
        try:
            actor_claims = await jwt.async_decode(request.actor_token, verify_exp=True)
        except (InvalidTokenError, ValueError) as exc:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                {'error': 'invalid_request', 'error_description': 'invalid actor_token'},
            ) from exc

    try:
        selection = (
            select_resource_indicator(
                list(request.resources),
                audience=request.audience,
            )
            if request.resources
            else None
        )
    except ValueError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, {'error': 'invalid_target'}) from exc

    scope = request.scope or str(subject_claims.get('scope') or '') or None
    audience = (
        (selection.audience if selection is not None else None)
        or request.audience
        or _audience_claim(subject_claims)
        or context.protected_resource_identifier
    )
    actor = _actor_claim(actor_claims)
    exchange_mode = 'delegation' if actor and actor.get('sub') != str(subject_claims.get('sub') or '') else 'impersonation'
    authorization_trace = build_authorization_decision_trace(
        tenant_id=str(subject_claims.get('tid') or ''),
        subject=str(subject_claims.get('sub') or ''),
        issuer=context.issuer,
        audience=audience,
        resource=selection.resource if selection is not None else None,
        scope=scope,
        subject_token_type=request.subject_token_type,
        requested_token_type=str(request.requested_token_type),
        exchange_mode=exchange_mode,
        actor_subject=actor.get('sub') if actor else None,
        source_issuer=str(subject_claims.get('iss') or ''),
        sender_constraint=context.sender_constraint.mechanism,
        verifier_logic_id=context.verifier_logic_id,
        required_claims=context.required_claims,
    )
    delegation_provenance = build_delegation_provenance(
        subject_token=request.subject_token,
        actor_token=request.actor_token,
        subject_claims=subject_claims,
        actor_claims=actor_claims,
        authorization_trace=authorization_trace,
        audience=audience,
        resource=selection.resource if selection is not None else None,
        exchange_mode=exchange_mode,
        sender_constraint=context.sender_constraint.mechanism,
    )
    delegation_grant_id = (
        str(request.delegation_grant_id or subject_claims.get("delegation_grant_id") or "").strip()
        or None
    )
    delegation_token_linkage: dict[str, Any] | None = None
    if delegation_grant_id:
        delegation_token_linkage = {
            "delegation_grant_id": delegation_grant_id,
            "authorization_trace_id": authorization_trace["decision_key"],
            "delegation_provenance_id": delegation_provenance["lineage_id"],
            "actor_subject": actor.get("sub") if actor else None,
            "subject": str(subject_claims.get("sub") or ""),
            "exchange_mode": exchange_mode,
            "source_token_hash": _hash_token(request.subject_token),
            "actor_token_hash": _hash_token(request.actor_token),
        }
    jwt_kwargs: Dict[str, Any] = {
        'scope': scope,
        'act': actor,
        'subject_token_type': request.subject_token_type,
        'requested_token_type': request.requested_token_type,
        'issuer': context.issuer,
        'audience': audience,
        'exchange_mode': exchange_mode,
        'source_issuer': subject_claims.get('iss'),
    }
    if context.sender_constraint.confirmation_claim:
        jwt_kwargs['cnf'] = context.sender_constraint.confirmation_claim
    access_token = await jwt.async_sign(
        sub=str(subject_claims.get('sub')),
        tid=str(subject_claims.get('tid')) if subject_claims.get('tid') is not None else None,
        cert_thumbprint=context.sender_constraint.certificate_thumbprint,
        **jwt_kwargs,
    )
    persisted_claims: Dict[str, Any] = {
        'sub': str(subject_claims.get('sub') or ''),
        'tid': str(subject_claims.get('tid')) if subject_claims.get('tid') is not None else None,
        'scope': scope,
        'iss': context.issuer,
        'aud': audience,
        'kind': 'access',
        'requested_token_type': request.requested_token_type,
        'subject_token_type': request.subject_token_type,
        'source_issuer': subject_claims.get('iss'),
        'exchange_mode': exchange_mode,
        'authorization_trace': authorization_trace,
        'delegation_provenance': delegation_provenance,
    }
    if delegation_token_linkage is not None:
        persisted_claims["delegation_token_linkage"] = delegation_token_linkage
        persisted_claims["delegation_grant_id"] = delegation_grant_id
        delegation_provenance["delegation_grant_id"] = delegation_grant_id
    if actor is not None:
        persisted_claims['act'] = actor
    if context.sender_constraint.confirmation_claim:
        persisted_claims['cnf'] = context.sender_constraint.confirmation_claim
    await upsert_token_record_async(
        access_token,
        persisted_claims,
        token_kind='access',
        token_type_hint='access_token',
    )
    await append_audit_event_async(
        tenant_id=None,
        actor_client_id=None,
        event_type='oauth2.token_exchange.issued',
        target_type='token',
        target_id=str(subject_claims.get('sub') or ''),
        details={
            'subject_token_type': request.subject_token_type,
            'requested_token_type': request.requested_token_type,
            'audience': audience,
            'resource': selection.resource if selection is not None else None,
            'resources': list(selection.resources) if selection is not None else [],
            'exchange_mode': exchange_mode,
            'actor_subject': actor.get('sub') if actor else None,
            'subject_issuer': subject_claims.get('iss'),
            'sender_constraint': context.sender_constraint.mechanism,
            'authorization_trace_decision_key': authorization_trace['decision_key'],
            'authorization_trace_request_hash': authorization_trace['request_hash'],
            'delegation_lineage_id': delegation_provenance['lineage_id'],
            'delegation_grant_id': delegation_grant_id,
            'delegation_token_linkage': delegation_token_linkage,
        },
        request_id=authorization_trace['request_hash'],
    )
    return TokenExchangeResponse(
        access_token=access_token,
        issued_token_type=str(request.requested_token_type),
        token_type=context.sender_constraint.token_type,
        scope=scope,
        audience=audience,
        exchange_mode=exchange_mode,
    )


token_exchange_capability = TokenExchangeCapability(_exchange_token)


__all__ = [
    'RFC8693_SPEC_URL',
    'SUPPORTED_REQUESTED_TOKEN_TYPES',
    'TOKEN_EXCHANGE_GRANT_TYPE',
    'TokenExchangeCapability',
    'token_exchange',
    'token_exchange_capability',
]
