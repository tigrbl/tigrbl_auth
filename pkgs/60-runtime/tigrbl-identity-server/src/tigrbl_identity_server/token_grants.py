"""Grant-specific execution for the OAuth token endpoint runtime."""

from __future__ import annotations

from tigrbl_identity_contracts.tokens import RefreshTokenRedemptionRequest

from .token_runtime import (
    AuthCode,
    AuthSession,
    AuthorizationCodeGrantForm,
    DEVICE_CODE_GRANT_TYPE,
    HTTPException,
    ISSUER,
    InvalidRefreshTokenError,
    InvalidTokenError,
    JSONResponse,
    JWT_BEARER_GRANT_TYPE,
    PasswordGrantForm,
    RFC6749Error,
    RefreshTokenReuseError,
    UUID,
    User,
    ValidationError,
    _json_error,
    _jwt,
    _token_pair_payload,
    datetime,
    enforce_authorization_code_grant,
    enforce_password_grant,
    oidc_hash,
    status,
    timezone,
    validate_native_token_request,
)


async def dispatch_token_grant(
    *,
    grant_type,
    db,
    data,
    client,
    sender_constraint,
    request_audience,
    resource,
    deployment,
    policy,
    token_endpoint_audiences,
    token_service,
    issue_pair,
    jwt_kwargs,
    read_record,
    delete_record,
    authenticate_password_fn,
    mint_id_token_fn,
    validate_assertion_fn,
    append_audit_event_fn,
    device_code_handler,
    verify_code_challenge_fn,
):
    if grant_type == "client_credentials":
        access, refresh = await issue_pair(
            db,
            jwt=_jwt,
            sub=str(client.id),
            tid=str(client.tenant_id),
            client_id=str(client.id),
            cert_thumbprint=sender_constraint.cert_thumbprint,
            **jwt_kwargs(scope=data.get("scope"), audience=request_audience),
        )
        return _token_pair_payload(
            access, refresh, token_type=sender_constraint.token_type
        )

    if grant_type == "password":
        try:
            enforce_password_grant(data)
            parsed = PasswordGrantForm(**data)
        except RFC6749Error as exc:
            return JSONResponse(
                {"error": str(exc)}, status_code=status.HTTP_400_BAD_REQUEST
            )
        except ValidationError as exc:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, exc.errors())
        user = await authenticate_password_fn(parsed.username, parsed.password, db)
        if user is None:
            return JSONResponse(
                {"error": "invalid_grant"}, status_code=status.HTTP_400_BAD_REQUEST
            )
        access, refresh = await issue_pair(
            db,
            jwt=_jwt,
            sub=str(user.id),
            tid=str(user.tenant_id),
            client_id=str(client.id),
            cert_thumbprint=sender_constraint.cert_thumbprint,
            **jwt_kwargs(scope="openid profile email", audience=request_audience),
        )
        return _token_pair_payload(
            access, refresh, token_type=sender_constraint.token_type
        )

    if grant_type == "authorization_code":
        try:
            enforce_authorization_code_grant(data)
            parsed = AuthorizationCodeGrantForm(**data)
        except RFC6749Error as exc:
            return JSONResponse(
                {"error": str(exc)}, status_code=status.HTTP_400_BAD_REQUEST
            )
        except ValidationError as exc:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, exc.errors())
        try:
            code_uuid = UUID(parsed.code)
        except ValueError:
            return JSONResponse(
                {"error": "invalid_grant"}, status_code=status.HTTP_400_BAD_REQUEST
            )
        auth_code = await read_record(AuthCode, db, code_uuid)
        expires_at = auth_code.expires_at if auth_code else None
        if expires_at and getattr(expires_at, "tzinfo", None) is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        if (
            auth_code is None
            or str(auth_code.client_id) != parsed.client_id
            or auth_code.redirect_uri != parsed.redirect_uri
            or datetime.now(timezone.utc) > (expires_at or datetime.now(timezone.utc))
        ):
            return JSONResponse(
                {"error": "invalid_grant"}, status_code=status.HTTP_400_BAD_REQUEST
            )
        try:
            validate_native_token_request(
                redirect_uri=auth_code.redirect_uri,
                code_verifier=parsed.code_verifier,
            )
        except ValueError as exc:
            return JSONResponse(
                {"error": "invalid_grant", "error_description": str(exc)},
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        if auth_code.code_challenge and (
            not parsed.code_verifier
            or not verify_code_challenge_fn(
                parsed.code_verifier, auth_code.code_challenge
            )
        ):
            return JSONResponse(
                {"error": "invalid_grant"}, status_code=status.HTTP_400_BAD_REQUEST
            )
        auth_code_claims = dict(auth_code.claims or {})
        stored_resource = auth_code_claims.pop("_resource", None)
        initiating_dpop_jkt = auth_code_claims.pop("_dpop_jkt", None)
        initiating_mtls_thumbprint = auth_code_claims.pop("_mtls_thumbprint", None)
        if request_audience not in {
            None,
            "",
            stored_resource,
        } and stored_resource not in {None, ""}:
            return JSONResponse(
                {"error": "invalid_target"}, status_code=status.HTTP_400_BAD_REQUEST
            )
        if policy.fapi_mode and not (initiating_dpop_jkt or initiating_mtls_thumbprint):
            return JSONResponse(
                {
                    "error": "invalid_grant",
                    "error_description": "FAPI authorization codes must remain bound to the initiating sender constraint",
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        if initiating_dpop_jkt and sender_constraint.jkt != str(initiating_dpop_jkt):
            return JSONResponse(
                {
                    "error": "invalid_grant",
                    "error_description": "DPoP proof key continuity check failed",
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        if initiating_mtls_thumbprint and sender_constraint.cert_thumbprint != str(
            initiating_mtls_thumbprint
        ):
            return JSONResponse(
                {
                    "error": "invalid_grant",
                    "error_description": "mTLS certificate continuity check failed",
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        audience = stored_resource or request_audience
        authorization_details = auth_code_claims.pop("_authorization_details", None)
        access, refresh = await issue_pair(
            db,
            jwt=_jwt,
            sub=str(auth_code.user_id),
            tid=str(auth_code.tenant_id),
            client_id=str(client.id),
            cert_thumbprint=sender_constraint.cert_thumbprint,
            **jwt_kwargs(
                scope=auth_code.scope,
                audience=audience,
                extra={"authorization_details": authorization_details}
                if authorization_details
                else None,
            ),
        )
        extra_claims = {
            "tid": str(auth_code.tenant_id),
            "typ": "id",
            "at_hash": oidc_hash(access),
        }
        if auth_code.session_id is not None:
            extra_claims["sid"] = str(auth_code.session_id)
            session = await read_record(AuthSession, db, auth_code.session_id)
            auth_time = (
                getattr(session, "auth_time", None) if session is not None else None
            )
            if auth_time is not None:
                if getattr(auth_time, "tzinfo", None) is None:
                    auth_time = auth_time.replace(tzinfo=timezone.utc)
                extra_claims["auth_time"] = int(auth_time.timestamp())
        if auth_code.claims and "id_token" in auth_code.claims:
            user_obj = await read_record(User, db, auth_code.user_id)
            idc = auth_code.claims["id_token"]
            if "email" in idc:
                extra_claims["email"] = user_obj.email if user_obj else ""
            if any(key in idc for key in ("name", "preferred_username")):
                extra_claims["name"] = user_obj.username if user_obj else ""
        id_token = await mint_id_token_fn(
            sub=str(auth_code.user_id),
            aud=parsed.client_id,
            nonce=auth_code.nonce or "nonce",
            issuer=str(deployment.issuer or ISSUER),
            **extra_claims,
        )
        await delete_record(AuthCode, db, auth_code.id)
        return _token_pair_payload(
            access,
            refresh,
            token_type=sender_constraint.token_type,
            id_token=id_token,
        )

    if grant_type == "refresh_token":
        refresh_token = str(data.get("refresh_token") or "").strip()
        if not refresh_token:
            return _json_error(
                "invalid_request",
                status_code=status.HTTP_400_BAD_REQUEST,
                description="refresh_token is required",
            )
        try:
            issued = await token_service.refresh(
                RefreshTokenRedemptionRequest(
                    refresh_token=refresh_token,
                    tenant_id=str(client.tenant_id),
                    client_id=str(client.id),
                    certificate_thumbprint=sender_constraint.cert_thumbprint,
                    requested_audience=request_audience,
                    token_type=sender_constraint.token_type,
                )
            )
        except (RefreshTokenReuseError, InvalidRefreshTokenError) as exc:
            return _json_error(
                "invalid_grant",
                status_code=status.HTTP_400_BAD_REQUEST,
                description=str(exc),
            )
        return _token_pair_payload(
            issued.access_token,
            issued.refresh_token,
            token_type=issued.token_type,
        )

    if grant_type == JWT_BEARER_GRANT_TYPE:
        try:
            assertion_claims = validate_assertion_fn(
                data, audience=token_endpoint_audiences
            )
        except (InvalidTokenError, ValueError) as exc:
            return JSONResponse(
                {"error": "invalid_grant", "error_description": str(exc)},
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        subject = str(assertion_claims.get("sub") or "")
        if not subject:
            return JSONResponse(
                {"error": "invalid_grant"}, status_code=status.HTTP_400_BAD_REQUEST
            )
        scope = str(data.get("scope") or assertion_claims.get("scope") or "") or None
        tenant_id = str(assertion_claims.get("tid") or client.tenant_id)
        access, refresh = await issue_pair(
            db,
            jwt=_jwt,
            sub=subject,
            tid=tenant_id,
            client_id=str(client.id),
            cert_thumbprint=sender_constraint.cert_thumbprint,
            **jwt_kwargs(
                scope=scope,
                audience=request_audience,
                extra={
                    "assertion_issuer": assertion_claims.get("iss"),
                    "assertion_subject": subject,
                    "assertion_jti": assertion_claims.get("jti"),
                },
            ),
        )
        await append_audit_event_fn(
            db,
            tenant_id=UUID(str(client.tenant_id))
            if not isinstance(client.tenant_id, UUID)
            else client.tenant_id,
            actor_client_id=client.id if isinstance(client.id, UUID) else None,
            event_type="oauth2.assertion_grant.issued",
            target_type="token",
            target_id=str(client.id),
            details={
                "grant_type": JWT_BEARER_GRANT_TYPE,
                "client_id": str(client.id),
                "assertion_issuer": assertion_claims.get("iss"),
                "assertion_subject": subject,
                "audience": request_audience,
                "resource": resource,
                "scope": scope,
            },
        )
        return _token_pair_payload(
            access, refresh, token_type=sender_constraint.token_type
        )

    if grant_type == DEVICE_CODE_GRANT_TYPE:
        return await device_code_handler(
            db=db,
            data=data,
            client=client,
            sender_constraint=sender_constraint,
            request_audience=request_audience,
            resource=resource,
            jwt_kwargs=jwt_kwargs,
            issue_token_pair=issue_pair,
        )
    return _json_error(
        "unsupported_grant_type", status_code=status.HTTP_400_BAD_REQUEST
    )
