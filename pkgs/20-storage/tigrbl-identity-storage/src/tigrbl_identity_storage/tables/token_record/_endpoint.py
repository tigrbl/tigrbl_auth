from __future__ import annotations

from ._op import (
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
    OAuthPolicyViolation,
    PRIVATE_KEY_JWT_AUTH_METHOD,
    PasswordGrantForm,
    RFC6749Error,
    RefreshTokenReuseError,
    SUPPORTED_MTLS_AUTH_METHODS,
    UUID,
    User,
    ValidationError,
    _enforce_tls,
    _header,
    _json_error,
    _jwt,
    _load_client,
    _parse_request_form,
    _pwd_backend,
    _registered_token_endpoint_auth_method,
    _resolve_request_deployment,
    _resource_selection,
    _token_endpoint_audiences,
    _token_pair_payload,
    allowed_grant_types,
    append_audit_event_record,
    assert_token_request_allowed,
    authenticate_client_assertion,
    authenticate_mtls_client,
    base64,
    datetime,
    delete_handler_record,
    dpop_proof_from_request,
    enforce_authorization_code_grant,
    enforce_grant_type,
    enforce_password_grant,
    handle_device_code_grant,
    inspect,
    issue_token_pair_records,
    mint_id_token,
    oidc_hash,
    presented_certificate_pem, presented_certificate_thumbprint,
    read_handler_record,
    redeem_refresh_token,
    runtime_security_profile,
    settings,
    status,
    timezone,
    validate_assertion_grant_request,
    validate_native_token_request,
    validate_sender_constraint,
    verify_code_challenge,
)

async def token_request(*, request, db):
    deployment = _resolve_request_deployment(request)
    _enforce_tls(request, deployment)
    data, resources = await _parse_request_form(request)
    auth = _header(request, 'Authorization')
    dpop_proof = dpop_proof_from_request(request)
    token_endpoint_audiences = _token_endpoint_audiences(deployment)

    client_assertion = str(data.get('client_assertion') or '').strip()
    client_assertion_type = str(data.get('client_assertion_type') or '').strip()
    client_id = None
    client_secret = None
    client_assertion_claims: dict[str, object] | None = None

    if auth and auth.startswith('Basic '):
        try:
            decoded = base64.b64decode(auth.split()[1]).decode()
            client_id, client_secret = decoded.split(':', 1)
        except Exception:
            return _json_error('invalid_client', status_code=status.HTTP_401_UNAUTHORIZED, headers={'WWW-Authenticate': 'Basic'})
    elif client_assertion:
        provisional_client_id = str(data.get('client_id') or '').strip() or None
        try:
            client_assertion_claims = authenticate_client_assertion(
                client_assertion_type=client_assertion_type,
                client_assertion=client_assertion,
                audience=token_endpoint_audiences,
                client_id=provisional_client_id,
            )
        except ValueError as exc:
            return _json_error('invalid_client', status_code=status.HTTP_401_UNAUTHORIZED, description=str(exc))
        client_id = str(client_assertion_claims.get('iss') or '')
    else:
        client_id = data.get('client_id')
        client_secret = data.get('client_secret')
    if not client_id:
        return _json_error('invalid_client', status_code=status.HTTP_401_UNAUTHORIZED, headers={'WWW-Authenticate': 'Basic'})

    client, registration = await _load_client(db, str(client_id))
    if not client:
        return _json_error('invalid_client', status_code=status.HTTP_401_UNAUTHORIZED, headers={'WWW-Authenticate': 'Basic'})

    registered_auth_method = _registered_token_endpoint_auth_method(registration)
    registration_metadata: dict[str, object] = {}
    if registration is not None:
        raw_registration_metadata = getattr(registration, 'registration_metadata', None)
        if isinstance(raw_registration_metadata, dict):
            registration_metadata = dict(raw_registration_metadata)
    policy = runtime_security_profile(deployment)
    if policy.fapi_mode and registered_auth_method not in set(policy.allowed_client_auth_methods):
        return _json_error(
            'invalid_client',
            status_code=status.HTTP_401_UNAUTHORIZED,
            description='FAPI clients must authenticate with private_key_jwt or mTLS',
        )
    if registered_auth_method == PRIVATE_KEY_JWT_AUTH_METHOD:
        if not client_assertion:
            return _json_error('invalid_client', status_code=status.HTTP_401_UNAUTHORIZED, description='client_assertion required for private_key_jwt clients')
        try:
            client_assertion_claims = authenticate_client_assertion(
                client_assertion_type=client_assertion_type,
                client_assertion=client_assertion,
                audience=str(deployment.issuer or ISSUER) if policy.fapi_mode else token_endpoint_audiences,
                client_id=str(client.id),
                token_endpoint_auth_method=registered_auth_method,
            )
        except ValueError as exc:
            return _json_error('invalid_client', status_code=status.HTTP_401_UNAUTHORIZED, description=str(exc))
    elif registered_auth_method in SUPPORTED_MTLS_AUTH_METHODS:
        if client_assertion:
            return _json_error('invalid_client', status_code=status.HTTP_401_UNAUTHORIZED, description='client is not configured for JWT client authentication')
        if client_secret:
            return _json_error('invalid_client', status_code=status.HTTP_401_UNAUTHORIZED, description='client_secret authentication is not permitted for mTLS-authenticated clients')
        try:
            authenticate_mtls_client(
                registration_metadata,
                presented_certificate_thumbprint(request),
                presented_certificate_pem=presented_certificate_pem(request),
                token_endpoint_auth_method=registered_auth_method,
            )
        except ValueError as exc:
            return _json_error('invalid_client', status_code=status.HTTP_401_UNAUTHORIZED, description=str(exc))
    elif client_assertion:
        return _json_error('invalid_client', status_code=status.HTTP_401_UNAUTHORIZED, description='client is not configured for JWT client authentication')
    elif client_secret:
        if policy.fapi_mode:
            return _json_error('invalid_client', status_code=status.HTTP_401_UNAUTHORIZED, description='FAPI rejects shared-secret client authentication')
        secret_valid = client.verify_secret(client_secret)
        if inspect.isawaitable(secret_valid):
            secret_valid = await secret_valid
        if not secret_valid:
            return _json_error('invalid_client', status_code=status.HTTP_401_UNAUTHORIZED, headers={'WWW-Authenticate': 'Basic'})

    if data.get('client_id') and data['client_id'] != str(client_id):
        return _json_error('invalid_client', status_code=status.HTTP_401_UNAUTHORIZED, headers={'WWW-Authenticate': 'Basic'})
    data['client_id'] = str(client_id)
    data.pop('client_secret', None)

    grant_type = data.get('grant_type')
    if not settings.enable_rfc6749 and grant_type not in {'client_credentials', 'password', 'authorization_code', 'refresh_token', JWT_BEARER_GRANT_TYPE, DEVICE_CODE_GRANT_TYPE}:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            [{"loc": ["body", "grant_type"], "msg": "unsupported grant_type", "type": "value_error"}],
        )
    allowed = allowed_grant_types(settings)
    if DEVICE_CODE_GRANT_TYPE not in allowed:
        allowed = [*allowed, DEVICE_CODE_GRANT_TYPE]
    try:
        enforce_grant_type(grant_type, allowed)
        assert_token_request_allowed(data, deployment)
    except RFC6749Error as exc:
        return JSONResponse({'error': str(exc)}, status_code=status.HTTP_400_BAD_REQUEST)
    except OAuthPolicyViolation as exc:
        return JSONResponse({'error': exc.error, 'error_description': exc.description}, status_code=exc.status_code)

    selection = _resource_selection(resources, str(data.get('audience') or '') or None)
    if isinstance(selection, JSONResponse):
        return selection
    resource = selection.resource if selection is not None else None
    request_audience = selection.audience if selection is not None else (str(data.get('audience') or '') or None)

    try:
        sender_constraint = validate_sender_constraint(request, deployment, dpop_proof=dpop_proof)
    except OAuthPolicyViolation as exc:
        return JSONResponse({'error': exc.error, 'error_description': exc.description}, status_code=exc.status_code)
    except ValueError:
        return _json_error('invalid_dpop_proof', status_code=status.HTTP_400_BAD_REQUEST)

    def _jwt_kwargs(*, scope: str | None = None, audience: str | None = None, extra: dict | None = None) -> dict:
        payload: dict = {'issuer': str(deployment.issuer or ISSUER)}
        if scope:
            payload['scope'] = scope
        effective_audience = audience
        if effective_audience in {None, ''} and policy.fapi_mode:
            effective_audience = str(deployment.protected_resource_identifier or settings.protected_resource_identifier)
        if effective_audience is not None:
            payload['audience'] = effective_audience
        elif settings.enable_rfc9068:
            payload['audience'] = settings.protected_resource_identifier
        if sender_constraint.confirmation_claim:
            payload['cnf'] = sender_constraint.confirmation_claim
        if extra:
            payload.update(extra)
        return payload

    if grant_type == 'client_credentials':
        access, refresh = await issue_token_pair_records(
            db,
            jwt=_jwt,
            sub=str(client_id),
            tid=str(client.tenant_id),
            client_id=str(client.id),
            cert_thumbprint=sender_constraint.cert_thumbprint,
            **_jwt_kwargs(scope=data.get('scope'), audience=request_audience),
        )
        return _token_pair_payload(access, refresh, token_type=sender_constraint.token_type)

    if grant_type == 'password':
        try:
            enforce_password_grant(data)
            parsed = PasswordGrantForm(**data)
        except RFC6749Error as exc:
            return JSONResponse({'error': str(exc)}, status_code=status.HTTP_400_BAD_REQUEST)
        except ValidationError as exc:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, exc.errors())
        user = await _pwd_backend.authenticate(db, parsed.username, parsed.password)
        access, refresh = await issue_token_pair_records(
            db,
            jwt=_jwt,
            sub=str(user.id),
            tid=str(user.tenant_id),
            client_id=str(client.id),
            cert_thumbprint=sender_constraint.cert_thumbprint,
            **_jwt_kwargs(scope='openid profile email', audience=request_audience),
        )
        return _token_pair_payload(access, refresh, token_type=sender_constraint.token_type)

    if grant_type == 'authorization_code':
        try:
            enforce_authorization_code_grant(data)
            parsed = AuthorizationCodeGrantForm(**data)
        except RFC6749Error as exc:
            return JSONResponse({'error': str(exc)}, status_code=status.HTTP_400_BAD_REQUEST)
        except ValidationError as exc:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, exc.errors())
        try:
            code_uuid = UUID(parsed.code)
        except ValueError:
            return JSONResponse({'error': 'invalid_grant'}, status_code=status.HTTP_400_BAD_REQUEST)
        auth_code = await read_handler_record(AuthCode, db, code_uuid)
        expires_at = auth_code.expires_at if auth_code else None
        if expires_at and getattr(expires_at, 'tzinfo', None) is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        if auth_code is None or str(auth_code.client_id) != parsed.client_id or auth_code.redirect_uri != parsed.redirect_uri or datetime.now(timezone.utc) > (expires_at or datetime.now(timezone.utc)):
            return JSONResponse({'error': 'invalid_grant'}, status_code=status.HTTP_400_BAD_REQUEST)
        try:
            validate_native_token_request(redirect_uri=auth_code.redirect_uri, code_verifier=parsed.code_verifier)
        except ValueError as exc:
            return JSONResponse({'error': 'invalid_grant', 'error_description': str(exc)}, status_code=status.HTTP_400_BAD_REQUEST)
        if auth_code.code_challenge:
            if not parsed.code_verifier or not verify_code_challenge(parsed.code_verifier, auth_code.code_challenge):
                return JSONResponse({'error': 'invalid_grant'}, status_code=status.HTTP_400_BAD_REQUEST)
        auth_code_claims = dict(auth_code.claims or {})
        stored_resource = auth_code_claims.pop('_resource', None)
        initiating_dpop_jkt = auth_code_claims.pop('_dpop_jkt', None)
        initiating_mtls_thumbprint = auth_code_claims.pop('_mtls_thumbprint', None)
        if request_audience not in {None, '', stored_resource} and stored_resource not in {None, ''}:
            return JSONResponse({'error': 'invalid_target'}, status_code=status.HTTP_400_BAD_REQUEST)
        if policy.fapi_mode and not (initiating_dpop_jkt or initiating_mtls_thumbprint):
            return JSONResponse(
                {'error': 'invalid_grant', 'error_description': 'FAPI authorization codes must remain bound to the initiating sender constraint'},
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        if initiating_dpop_jkt and sender_constraint.jkt != str(initiating_dpop_jkt):
            return JSONResponse(
                {'error': 'invalid_grant', 'error_description': 'DPoP proof key continuity check failed'},
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        if initiating_mtls_thumbprint and sender_constraint.cert_thumbprint != str(initiating_mtls_thumbprint):
            return JSONResponse(
                {'error': 'invalid_grant', 'error_description': 'mTLS certificate continuity check failed'},
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        audience = stored_resource or request_audience
        authorization_details = auth_code_claims.pop('_authorization_details', None)
        access, refresh = await issue_token_pair_records(
            db,
            jwt=_jwt,
            sub=str(auth_code.user_id),
            tid=str(auth_code.tenant_id),
            client_id=str(client.id),
            cert_thumbprint=sender_constraint.cert_thumbprint,
            **_jwt_kwargs(scope=auth_code.scope, audience=audience, extra={'authorization_details': authorization_details} if authorization_details else None),
        )
        extra_claims = {'tid': str(auth_code.tenant_id), 'typ': 'id', 'at_hash': oidc_hash(access)}
        if auth_code.session_id is not None:
            extra_claims['sid'] = str(auth_code.session_id)
            session = await read_handler_record(AuthSession, db, auth_code.session_id)
            auth_time = getattr(session, 'auth_time', None) if session is not None else None
            if auth_time is not None:
                if getattr(auth_time, 'tzinfo', None) is None:
                    auth_time = auth_time.replace(tzinfo=timezone.utc)
                extra_claims['auth_time'] = int(auth_time.timestamp())
        if auth_code.claims and 'id_token' in auth_code.claims:
            user_obj = await read_handler_record(User, db, auth_code.user_id)
            idc = auth_code.claims['id_token']
            if 'email' in idc:
                extra_claims['email'] = user_obj.email if user_obj else ''
            if any(k in idc for k in ('name', 'preferred_username')):
                extra_claims['name'] = user_obj.username if user_obj else ''
        id_token = await mint_id_token(
            sub=str(auth_code.user_id),
            aud=parsed.client_id,
            nonce=auth_code.nonce or 'nonce',
            issuer=str(deployment.issuer or ISSUER),
            **extra_claims,
        )
        await delete_handler_record(AuthCode, db, auth_code.id)
        return _token_pair_payload(access, refresh, token_type=sender_constraint.token_type, id_token=id_token)

    if grant_type == 'refresh_token':
        refresh_token = str(data.get('refresh_token') or '').strip()
        if not refresh_token:
            return _json_error('invalid_request', status_code=status.HTTP_400_BAD_REQUEST, description='refresh_token is required')
        try:
            payload = await redeem_refresh_token(
                jwt=_jwt,
                refresh_token=refresh_token,
                client_id=str(client.id),
                cert_thumbprint=sender_constraint.cert_thumbprint,
                requested_audience=request_audience,
                token_type=sender_constraint.token_type,
            )
        except RefreshTokenReuseError as exc:
            return _json_error('invalid_grant', status_code=status.HTTP_400_BAD_REQUEST, description=str(exc))
        except InvalidRefreshTokenError as exc:
            return _json_error('invalid_grant', status_code=status.HTTP_400_BAD_REQUEST, description=str(exc))
        return payload

    if grant_type == JWT_BEARER_GRANT_TYPE:
        try:
            assertion_claims = validate_assertion_grant_request(data, audience=token_endpoint_audiences)
        except (InvalidTokenError, ValueError) as exc:
            return JSONResponse({'error': 'invalid_grant', 'error_description': str(exc)}, status_code=status.HTTP_400_BAD_REQUEST)
        subject = str(assertion_claims.get('sub') or '')
        if not subject:
            return JSONResponse({'error': 'invalid_grant'}, status_code=status.HTTP_400_BAD_REQUEST)
        scope = str(data.get('scope') or assertion_claims.get('scope') or '') or None
        tenant_id = str(assertion_claims.get('tid') or client.tenant_id)
        access, refresh = await issue_token_pair_records(
            db,
            jwt=_jwt,
            sub=subject,
            tid=tenant_id,
            client_id=str(client.id),
            cert_thumbprint=sender_constraint.cert_thumbprint,
            **_jwt_kwargs(
                scope=scope,
                audience=request_audience,
                extra={
                    'assertion_issuer': assertion_claims.get('iss'),
                    'assertion_subject': subject,
                    'assertion_jti': assertion_claims.get('jti'),
                },
            ),
        )
        await append_audit_event_record(
            db,
            tenant_id=UUID(str(client.tenant_id)) if not isinstance(client.tenant_id, UUID) else client.tenant_id,
            actor_client_id=client.id if isinstance(client.id, UUID) else None,
            event_type='oauth2.assertion_grant.issued',
            target_type='token',
            target_id=str(client.id),
            details={
                'grant_type': JWT_BEARER_GRANT_TYPE,
                'client_id': str(client.id),
                'assertion_issuer': assertion_claims.get('iss'),
                'assertion_subject': subject,
                'audience': request_audience,
                'resource': resource,
                'scope': scope,
            },
        )
        return _token_pair_payload(access, refresh, token_type=sender_constraint.token_type)

    if grant_type == DEVICE_CODE_GRANT_TYPE:
        return await handle_device_code_grant(
            db=db,
            data=data,
            client=client,
            sender_constraint=sender_constraint,
            request_audience=request_audience,
            resource=resource,
            jwt_kwargs=_jwt_kwargs,
        )
    return _json_error('unsupported_grant_type', status_code=status.HTTP_400_BAD_REQUEST)
