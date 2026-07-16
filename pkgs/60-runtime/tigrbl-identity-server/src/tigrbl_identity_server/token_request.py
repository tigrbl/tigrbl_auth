from __future__ import annotations
from . import token_runtime as _runtime
from .token_runtime import (
    DEVICE_CODE_GRANT_TYPE,
    HTTPException,
    ISSUER,
    JSONResponse,
    JWT_BEARER_GRANT_TYPE,
    OAuthPolicyViolation,
    PRIVATE_KEY_JWT_AUTH_METHOD,
    RFC6749Error,
    SUPPORTED_MTLS_AUTH_METHODS,
    _enforce_tls,
    _header,
    _json_error,
    _jwt,
    _load_client,
    _parse_request_form,
    authenticate_password,
    _registered_token_endpoint_auth_method,
    _resolve_request_deployment,
    _resource_selection,
    _token_endpoint_audiences,
    allowed_grant_types,
    append_audit_event_record,
    assert_token_request_allowed,
    authenticate_client_assertion,
    authenticate_mtls_client,
    base64,
    delete_handler_record,
    dpop_proof_from_request,
    enforce_grant_type,
    issue_token_pair_records,
    mint_id_token,
    presented_certificate_pem,
    presented_certificate_thumbprint,
    read_handler_record,
    runtime_security_profile,
    settings,
    status,
    validate_assertion_grant_request,
)
from tigrbl_auth_protocol_oauth.standards.oauth_security_bcp import (
    validate_sender_constraint_async,
)
from tigrbl_identity_contracts.tokens import (
    TokenPairIssueRequest,
)
from tigrbl_identity_storage_runtime.dpop_state import (
    check_and_store_dpop_replay,
    consume_dpop_nonce,
)
from tigrbl_client_secret_authentication_capability import ClientSecretAuthenticationCapability
from tigrbl_identity_storage_runtime.ops.clients import lookup_client

from .security.token_issuance import build_rfc6749_token_endpoint_service
from .token_device_grant import handle_device_code_grant
from .token_grants import dispatch_token_grant

_IMPORTED_ISSUE_TOKEN_PAIR_RECORDS = issue_token_pair_records
client_secret_authentication = ClientSecretAuthenticationCapability(lookup_client)
AuthCode = _runtime.AuthCode
AuthSession = _runtime.AuthSession
User = _runtime.User
verify_code_challenge = _runtime.verify_code_challenge
oidc_hash = _runtime.oidc_hash


def _token_pair_issuer():
    """Honor both the legacy module hook and the canonical runtime hook."""
    return (
        issue_token_pair_records
        if issue_token_pair_records is not _IMPORTED_ISSUE_TOKEN_PAIR_RECORDS
        else _runtime.issue_token_pair_records
    )


async def token_request(*, request, db):
    deployment = _resolve_request_deployment(request)
    _enforce_tls(request, deployment)
    data, resources = await _parse_request_form(request)
    auth = _header(request, "Authorization")
    dpop_proof = dpop_proof_from_request(request)
    token_endpoint_audiences = _token_endpoint_audiences(deployment)

    client_assertion = str(data.get("client_assertion") or "").strip()
    client_assertion_type = str(data.get("client_assertion_type") or "").strip()
    client_id = None
    client_secret = None
    client_assertion_claims: dict[str, object] | None = None

    if auth and auth.startswith("Basic "):
        try:
            decoded = base64.b64decode(auth.split()[1]).decode()
            client_id, client_secret = decoded.split(":", 1)
        except Exception:
            return _json_error(
                "invalid_client",
                status_code=status.HTTP_401_UNAUTHORIZED,
                headers={"WWW-Authenticate": "Basic"},
            )
    elif client_assertion:
        provisional_client_id = str(data.get("client_id") or "").strip() or None
        try:
            client_assertion_claims = authenticate_client_assertion(
                client_assertion_type=client_assertion_type,
                client_assertion=client_assertion,
                audience=token_endpoint_audiences,
                client_id=provisional_client_id,
            )
        except ValueError as exc:
            return _json_error(
                "invalid_client",
                status_code=status.HTTP_401_UNAUTHORIZED,
                description=str(exc),
            )
        client_id = str(client_assertion_claims.get("iss") or "")
    else:
        client_id = data.get("client_id")
        client_secret = data.get("client_secret")
    if not client_id:
        return _json_error(
            "invalid_client",
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Basic"},
        )

    client, registration = await _load_client(db, str(client_id))
    if not client:
        return _json_error(
            "invalid_client",
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Basic"},
        )

    registered_auth_method = _registered_token_endpoint_auth_method(registration)
    registration_metadata: dict[str, object] = {}
    if registration is not None:
        raw_registration_metadata = getattr(registration, "registration_metadata", None)
        if isinstance(raw_registration_metadata, dict):
            registration_metadata = dict(raw_registration_metadata)
    policy = runtime_security_profile(deployment)
    if policy.fapi_mode and registered_auth_method not in set(
        policy.allowed_client_auth_methods
    ):
        return _json_error(
            "invalid_client",
            status_code=status.HTTP_401_UNAUTHORIZED,
            description="FAPI clients must authenticate with private_key_jwt or mTLS",
        )
    if registered_auth_method == PRIVATE_KEY_JWT_AUTH_METHOD:
        if not client_assertion:
            return _json_error(
                "invalid_client",
                status_code=status.HTTP_401_UNAUTHORIZED,
                description="client_assertion required for private_key_jwt clients",
            )
        try:
            client_assertion_claims = authenticate_client_assertion(
                client_assertion_type=client_assertion_type,
                client_assertion=client_assertion,
                audience=str(deployment.issuer or ISSUER)
                if policy.fapi_mode
                else token_endpoint_audiences,
                client_id=str(client.id),
                token_endpoint_auth_method=registered_auth_method,
            )
        except ValueError as exc:
            return _json_error(
                "invalid_client",
                status_code=status.HTTP_401_UNAUTHORIZED,
                description=str(exc),
            )
    elif registered_auth_method in SUPPORTED_MTLS_AUTH_METHODS:
        if client_assertion:
            return _json_error(
                "invalid_client",
                status_code=status.HTTP_401_UNAUTHORIZED,
                description="client is not configured for JWT client authentication",
            )
        if client_secret:
            return _json_error(
                "invalid_client",
                status_code=status.HTTP_401_UNAUTHORIZED,
                description="client_secret authentication is not permitted for mTLS-authenticated clients",
            )
        try:
            authenticate_mtls_client(
                registration_metadata,
                presented_certificate_thumbprint(request),
                presented_certificate_pem=presented_certificate_pem(request),
                token_endpoint_auth_method=registered_auth_method,
            )
        except ValueError as exc:
            return _json_error(
                "invalid_client",
                status_code=status.HTTP_401_UNAUTHORIZED,
                description=str(exc),
            )
    elif client_assertion:
        return _json_error(
            "invalid_client",
            status_code=status.HTTP_401_UNAUTHORIZED,
            description="client is not configured for JWT client authentication",
        )
    elif client_secret:
        if policy.fapi_mode:
            return _json_error(
                "invalid_client",
                status_code=status.HTTP_401_UNAUTHORIZED,
                description="FAPI rejects shared-secret client authentication",
            )
        secret_authentication = client_secret_authentication.verify_client_record(
            client,
            client_secret,
        )
        if not secret_authentication.authenticated:
            return _json_error(
                "invalid_client",
                status_code=status.HTTP_401_UNAUTHORIZED,
                headers={"WWW-Authenticate": "Basic"},
            )

    if data.get("client_id") and data["client_id"] != str(client_id):
        return _json_error(
            "invalid_client",
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Basic"},
        )
    data["client_id"] = str(client_id)
    data.pop("client_secret", None)

    grant_type = data.get("grant_type")
    if not settings.enable_rfc6749 and grant_type not in {
        "client_credentials",
        "password",
        "authorization_code",
        "refresh_token",
        JWT_BEARER_GRANT_TYPE,
        DEVICE_CODE_GRANT_TYPE,
    }:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            [
                {
                    "loc": ["body", "grant_type"],
                    "msg": "unsupported grant_type",
                    "type": "value_error",
                }
            ],
        )
    allowed = allowed_grant_types(settings)
    if DEVICE_CODE_GRANT_TYPE not in allowed:
        allowed = [*allowed, DEVICE_CODE_GRANT_TYPE]
    try:
        enforce_grant_type(grant_type, allowed)
        assert_token_request_allowed(data, deployment)
    except RFC6749Error as exc:
        return JSONResponse(
            {"error": str(exc)}, status_code=status.HTTP_400_BAD_REQUEST
        )
    except OAuthPolicyViolation as exc:
        return JSONResponse(
            {"error": exc.error, "error_description": exc.description},
            status_code=exc.status_code,
        )

    selection = _resource_selection(resources, str(data.get("audience") or "") or None)
    if isinstance(selection, JSONResponse):
        return selection
    resource = selection.resource if selection is not None else None
    request_audience = (
        selection.audience
        if selection is not None
        else (str(data.get("audience") or "") or None)
    )

    try:
        sender_constraint = await validate_sender_constraint_async(
            request,
            deployment,
            dpop_proof=dpop_proof,
            replay_checker=lambda claims, ttl_s=300: check_and_store_dpop_replay(
                db, claims, ttl_s=ttl_s
            ),
            nonce_consumer=lambda nonce, now=None: consume_dpop_nonce(
                db, nonce, now=now
            ),
        )
    except OAuthPolicyViolation as exc:
        return JSONResponse(
            {"error": exc.error, "error_description": exc.description},
            status_code=exc.status_code,
        )
    except ValueError:
        return _json_error(
            "invalid_dpop_proof", status_code=status.HTTP_400_BAD_REQUEST
        )

    token_service = build_rfc6749_token_endpoint_service(
        db=db,
        token_coder=_jwt,
    )

    async def _issue_pair(
        _db,
        *,
        jwt,
        sub: str,
        tid: str,
        client_id: str,
        cert_thumbprint: str | None = None,
        **claims,
    ) -> tuple[str, str | None]:
        legacy_issuer = _token_pair_issuer()
        if legacy_issuer is not _IMPORTED_ISSUE_TOKEN_PAIR_RECORDS:
            return await legacy_issuer(
                _db,
                jwt=jwt,
                sub=sub,
                tid=tid,
                client_id=client_id,
                cert_thumbprint=cert_thumbprint,
                **claims,
            )
        issuer = str(claims.pop("issuer", None) or deployment.issuer or ISSUER)
        scope = claims.pop("scope", None)
        audience = claims.pop("audience", None)
        confirmation = claims.pop("cnf", None)
        issued = await token_service.issue(
            TokenPairIssueRequest(
                subject=sub,
                tenant_id=tid,
                client_id=client_id,
                issuer=issuer,
                scope=str(scope) if scope is not None else None,
                audience=audience,
                certificate_thumbprint=cert_thumbprint,
                confirmation=(
                    dict(confirmation) if isinstance(confirmation, dict) else None
                ),
                token_type=sender_constraint.token_type,
                extra_claims=claims,
            )
        )
        return issued.access_token, issued.refresh_token

    def _jwt_kwargs(
        *,
        scope: str | None = None,
        audience: str | None = None,
        extra: dict | None = None,
    ) -> dict:
        payload: dict = {"issuer": str(deployment.issuer or ISSUER)}
        if scope:
            payload["scope"] = scope
        effective_audience = audience
        if effective_audience in {None, ""} and policy.fapi_mode:
            effective_audience = str(
                deployment.protected_resource_identifier
                or settings.protected_resource_identifier
            )
        if effective_audience is not None:
            payload["audience"] = effective_audience
        elif settings.enable_rfc9068:
            payload["audience"] = settings.protected_resource_identifier
        if sender_constraint.confirmation_claim:
            payload["cnf"] = sender_constraint.confirmation_claim
        if extra:
            payload.update(extra)
        return payload

    return await dispatch_token_grant(
        grant_type=grant_type,
        db=db,
        data=data,
        client=client,
        sender_constraint=sender_constraint,
        request_audience=request_audience,
        resource=resource,
        deployment=deployment,
        policy=policy,
        token_endpoint_audiences=token_endpoint_audiences,
        token_service=token_service,
        issue_pair=_issue_pair,
        jwt_kwargs=_jwt_kwargs,
        read_record=read_handler_record,
        delete_record=delete_handler_record,
        authenticate_password_fn=authenticate_password,
        mint_id_token_fn=mint_id_token,
        validate_assertion_fn=validate_assertion_grant_request,
        append_audit_event_fn=append_audit_event_record,
        device_code_handler=handle_device_code_grant,
        verify_code_challenge_fn=verify_code_challenge,
    )
