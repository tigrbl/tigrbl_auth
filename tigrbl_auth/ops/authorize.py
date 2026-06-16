from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from typing import Any
from urllib.parse import urlencode
from uuid import UUID, uuid4

from tigrbl_auth.framework import HTMLResponse, HTTPException, RedirectResponse, status
from tigrbl_auth.api.rest.shared import _jwt, _require_tls
from tigrbl_auth.config.deployment import deployment_from_request
from tigrbl_auth.config.settings import settings
from tigrbl_auth.security.handler_records import (
    bind_browser_session_client_record,
    create_handler_record,
    first_handler_record,
    maybe_rotate_browser_session_cookie_record,
    read_handler_record,
    resolve_browser_session_record,
    update_handler_record,
)
from tigrbl_auth.standards.http.cookies import issue_session_cookie
from tigrbl_auth.oidc_id_token import mint_id_token, oidc_hash
from tigrbl_auth.standards.oidc.session_mgmt import (
    session_state_for_client,
)
from tigrbl_auth.standards.oauth2.native_apps import validate_native_authorization_request
from tigrbl_auth.standards.oauth2.jar import merge_request_object_params, parse_request_object
from tigrbl_auth.standards.oauth2.par import RFC9126_SPEC_URL, consume_pushed_authorization_request, validate_pushed_authorization_request_row
from tigrbl_auth.standards.oauth2.rar import normalize_authorization_details
from tigrbl_auth.standards.oauth2.resource_indicators import extract_resource
from tigrbl_auth.standards.oauth2.issuer_identification import authorization_response_issuer
from tigrbl_auth.standards.oauth2.rfc8414_metadata import ISSUER
from tigrbl_auth.standards.oauth2.rfc9700 import (
    OAuthPolicyViolation,
    assert_authorization_request_allowed,
    runtime_security_profile,
)
from tigrbl_auth.tables import AuthCode, Client, PushedAuthorizationRequest, User


def _coerce_multi_value(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, (list, tuple, set)):
        return [str(item) for item in value if str(item)]
    return [str(value)] if str(value) else []


async def _resolve_pushed_authorization_request(db, params: dict[str, Any]) -> tuple[dict[str, Any], PushedAuthorizationRequest | None]:
    request_uri = params.get("request_uri")
    if not request_uri:
        return params, None
    row = await first_handler_record(PushedAuthorizationRequest, db, {"request_uri": str(request_uri)})
    if row is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, {"error": "invalid_request_uri", "error_description": RFC9126_SPEC_URL})
    try:
        result = validate_pushed_authorization_request_row(
            row,
            client_id=str(params.get("client_id") or '') or None,
            request_uri=str(request_uri),
        )
    except Exception as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, {"error": "invalid_request_uri", "error_description": RFC9126_SPEC_URL}) from exc

    merged = dict(result.params or {})
    for key, value in params.items():
        if value in (None, "", [], (), {}):
            continue
        if key not in {"request_uri", "client_id"}:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, {"error": "invalid_request", "error_description": RFC9126_SPEC_URL})
        existing = merged.get(key)
        if existing not in (None, "", [], (), {}) and existing != value:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, {"error": "invalid_request_uri", "error_description": RFC9126_SPEC_URL})
        merged[key] = value
    return merged, row


async def _resolve_request_object(params: dict[str, Any], deployment) -> dict[str, Any]:
    request_object = params.get("request")
    if not request_object:
        return params
    if not deployment.flag_enabled("enable_rfc9101"):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, {"error": "invalid_request_object"})
    try:
        parsed = await parse_request_object(
            str(request_object),
            secret=settings.jwt_secret,
            algorithms=("HS256", "HS384", "HS512"),
            expected_client_id=str(params.get("client_id") or '') or None,
            expected_audience=str(deployment.issuer or ISSUER),
        )
        merged = merge_request_object_params(parsed, params)
    except Exception as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, {"error": "invalid_request_object"}) from exc
    return merged


async def authorize_request(*, request, db, params: dict[str, Any]):
    deployment = deployment_from_request(request, settings)
    _require_tls(request, deployment=deployment)
    policy = runtime_security_profile(deployment)

    params = dict(params)
    params["_frontchannel_request"] = True
    params, par_row = await _resolve_pushed_authorization_request(db, params)
    params = await _resolve_request_object(params, deployment)

    try:
        assert_authorization_request_allowed(params, deployment)
    except OAuthPolicyViolation as exc:
        raise HTTPException(exc.status_code, {"error": exc.error, "error_description": exc.description}) from exc

    response_type = params.get("response_type")
    client_id = params.get("client_id")
    redirect_uri = params.get("redirect_uri")
    scope = params.get("scope")
    if not all((response_type, client_id, redirect_uri, scope)):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, {"error": "invalid_request"})

    response_mode = params.get("response_mode")
    state = params.get("state")
    nonce = params.get("nonce")
    code_challenge = params.get("code_challenge")
    code_challenge_method = params.get("code_challenge_method")
    prompt = params.get("prompt")
    max_age = params.get("max_age")
    login_hint = params.get("login_hint")
    claims = params.get("claims")
    authorization_details = params.get("authorization_details")
    resources = _coerce_multi_value(params.get("resource"))

    if max_age is not None:
        try:
            max_age = int(max_age)
        except (TypeError, ValueError) as exc:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, {"error": "invalid_request"}) from exc
        if max_age < 0:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, {"error": "invalid_request"})

    rts = set(str(response_type).split())
    allowed = {"code", "token", "id_token"}
    if not rts or not rts.issubset(allowed):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, {"error": "unsupported_response_type"})

    scopes = set(str(scope).split())
    if "openid" not in scopes:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, {"error": "invalid_scope"})
    if "id_token" in rts and not nonce:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, {"error": "invalid_request"})

    try:
        client_uuid = UUID(str(client_id))
    except ValueError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, {"error": "invalid_request"}) from exc

    client = await read_handler_record(Client, db, client_uuid)
    if client is None or redirect_uri not in (client.redirect_uris or "").split():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, {"error": "invalid_request"})

    if par_row is not None and par_row.client_id not in {None, client_uuid}:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, {"error": "invalid_request_uri"})

    session = await resolve_browser_session_record(db, request, deployment=deployment)
    if login_hint and session and session.username != login_hint:
        session = None
    prompts = set(str(prompt).split()) if prompt else set()
    if "login" in prompts:
        session = None
    if session is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, {"error": "login_required"})
    if max_age is not None:
        auth_time = session.auth_time
        if auth_time is not None and auth_time.tzinfo is None:
            auth_time = auth_time.replace(tzinfo=timezone.utc)
        if auth_time is None or datetime.now(timezone.utc) - auth_time > timedelta(seconds=max_age):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, {"error": "login_required"})

    try:
        validate_native_authorization_request(
            redirect_uri=str(redirect_uri),
            response_type=str(response_type),
            code_challenge=code_challenge,
            code_challenge_method=code_challenge_method,
        )
    except ValueError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, {"error": "invalid_request", "error_description": str(exc)}) from exc
    if code_challenge_method and code_challenge_method != "S256":
        raise HTTPException(status.HTTP_400_BAD_REQUEST, {"error": "invalid_request"})
    if policy.pkce_s256_required and (not code_challenge or code_challenge_method != "S256"):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            {"error": "invalid_request", "error_description": "FAPI authorization requests require PKCE S256"},
        )

    mode = response_mode or ("fragment" if rts & {"token", "id_token"} else "query")
    if mode not in {"query", "fragment", "form_post"}:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, {"error": "unsupported_response_mode"})

    requested_claims: dict[str, Any] | None = None
    if claims:
        try:
            if isinstance(claims, dict):
                parsed = claims
            else:
                parsed = json.loads(str(claims))
            if not isinstance(parsed, dict):
                raise ValueError
            requested_claims = parsed
        except Exception as exc:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, {"error": "invalid_request"}) from exc

    resource_audience: str | None = None
    if resources:
        try:
            resource_audience = extract_resource(resources)
        except ValueError as exc:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, {"error": "invalid_target"}) from exc

    parsed_authorization_details: list[dict[str, Any]] | None = None
    if authorization_details:
        if not deployment.flag_enabled("enable_rfc9396"):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, {"error": "invalid_request"})
        try:
            binding = normalize_authorization_details(
                authorization_details,
                resource=resource_audience,
                audience=resource_audience,
            )
            parsed_authorization_details = binding.details
            if resource_audience is None and binding.audience is not None:
                resource_audience = binding.audience
        except ValueError as exc:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, {"error": "invalid_request"}) from exc

    await bind_browser_session_client_record(db, session.id, client_id=client_uuid)
    session.client_id = client_uuid
    user_sub = str(session.user_id)
    tenant_id = str(session.tenant_id)
    scope_str = " ".join(sorted(scopes))
    params_out: list[tuple[str, str]] = []
    code: str | None = None
    access: str | None = None

    auth_code_claims: dict[str, Any] | None = dict(requested_claims or {})
    if resource_audience is not None:
        auth_code_claims["_resource"] = resource_audience
    if parsed_authorization_details is not None:
        auth_code_claims["_authorization_details"] = parsed_authorization_details
    if params.get("_dpop_jkt"):
        auth_code_claims["_dpop_jkt"] = str(params["_dpop_jkt"])
    if params.get("_mtls_thumbprint"):
        auth_code_claims["_mtls_thumbprint"] = str(params["_mtls_thumbprint"])

    if "code" in rts:
        code_uuid = uuid4()
        await create_handler_record(
            AuthCode,
            db,
            {
                "id": code_uuid,
                "user_id": UUID(user_sub),
                "tenant_id": UUID(tenant_id),
                "client_id": client_uuid,
                "session_id": session.id,
                "redirect_uri": str(redirect_uri),
                "code_challenge": code_challenge,
                "nonce": nonce,
                "scope": scope_str,
                "expires_at": datetime.now(timezone.utc) + timedelta(minutes=10),
                "claims": auth_code_claims or None,
            },
        )
        code = str(code_uuid)
        params_out.append(("code", code))

    if "token" in rts:
        jwt_kwargs: dict[str, Any] = {"scope": scope_str}
        if resource_audience is not None:
            jwt_kwargs["audience"] = resource_audience
        access = await _jwt.async_sign(sub=user_sub, tid=tenant_id, **jwt_kwargs)
        params_out.append(("access_token", access))
        params_out.append(("token_type", "bearer"))

    if "id_token" in rts:
        extra_claims: dict[str, Any] = {
            "tid": tenant_id,
            "typ": "id",
            "sid": str(session.id),
            "auth_time": int(session.auth_time.timestamp()),
        }
        if requested_claims and "id_token" in requested_claims:
            user_obj = await read_handler_record(User, db, UUID(user_sub))
            idc = requested_claims["id_token"]
            if "email" in idc:
                extra_claims["email"] = user_obj.email if user_obj else ""
            if any(k in idc for k in ("name", "preferred_username")):
                extra_claims["name"] = session.username
        if access:
            extra_claims["at_hash"] = oidc_hash(access)
        if code:
            extra_claims["c_hash"] = oidc_hash(code)
        id_token = await mint_id_token(sub=user_sub, aud=str(client_id), nonce=nonce, issuer=str(deployment.issuer or ISSUER), **extra_claims)
        params_out.append(("id_token", id_token))

    session_state = session_state_for_client(
        session,
        client_id=str(client_id),
        redirect_uri=str(redirect_uri),
        deployment=deployment,
    )
    if session_state:
        params_out.append(("session_state", session_state))
    if policy.authorization_response_iss_required:
        params_out.append(authorization_response_issuer(str(deployment.issuer or ISSUER)))
    if state:
        params_out.append(("state", str(state)))

    if par_row is not None and getattr(par_row, "consumed_at", None) is None:
        consume_pushed_authorization_request(par_row)
        await update_handler_record(
            PushedAuthorizationRequest,
            db,
            par_row.id,
            {"consumed_at": par_row.consumed_at},
        )

    rotated_secret = await maybe_rotate_browser_session_cookie_record(db, session)

    if mode == "fragment":
        response = RedirectResponse(f"{redirect_uri}#{urlencode(params_out)}" if params_out else redirect_uri)
    elif mode == "form_post":
        inputs = "".join(f'<input type="hidden" name="{k}" value="{v}" />' for k, v in params_out)
        body = "<!DOCTYPE html><html><body>" + f'<form method="post" action="{redirect_uri}">{inputs}</form>' + "<script>document.forms[0].submit()</script></body></html>"
        response = HTMLResponse(content=body)
    else:
        response = RedirectResponse(f"{redirect_uri}?{urlencode(params_out)}" if params_out else redirect_uri)

    if rotated_secret:
        issue_session_cookie(response, session_id=session.id, secret=rotated_secret, expires_at=session.expires_at)
    return response
