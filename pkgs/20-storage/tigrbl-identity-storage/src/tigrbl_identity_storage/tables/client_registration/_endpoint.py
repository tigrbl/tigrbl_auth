from __future__ import annotations

from ._op import (
    Client,
    ClientRegistration,
    DynamicClientRegistrationIn,
    DynamicClientRegistrationManagementIn,
    HTTPException,
    Tenant,
    _merge_registration_metadata,
    _registration_response,
    _require_registration_access,
    _validated_registration_payload,
    append_audit_event_record,
    create_handler_record,
    datetime,
    deployment_from_request,
    read_handler_record,
    runtime_security_profile,
    secrets,
    settings,
    status,
    timezone,
    token_hash,
    update_handler_record,
    uuid4,
)


async def register_client(*, request, db, payload: DynamicClientRegistrationIn | None = None):
    if not settings.enable_rfc7591:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'dynamic client registration disabled')
    if payload is None:
        body = await request.json() if hasattr(request, 'json') else {}
        payload = DynamicClientRegistrationIn(**body)

    deployment = deployment_from_request(request, settings)
    tenant, derived_metadata = await _validated_registration_payload(db=db, payload=payload, deployment=deployment)
    policy = runtime_security_profile(deployment)

    client_id = str(uuid4())
    client_secret = secrets.token_urlsafe(32)
    client_seed = Client.new(tenant.id, client_id, client_secret, list(payload.redirect_uris))
    client = await create_handler_record(
        Client,
        db,
        {
            'id': client_seed.id,
            'tenant_id': tenant.id,
            'client_secret_hash': client_seed.client_secret_hash,
            'redirect_uris': client_seed.redirect_uris,
            'grant_types': ' '.join(payload.grant_types),
            'response_types': ' '.join(payload.response_types),
        },
    )

    registration_access_token = None
    registration_client_uri = None
    registration_access_token_hash = None
    if settings.enable_rfc7592:
        registration_access_token = secrets.token_urlsafe(32)
        registration_access_token_hash = token_hash(registration_access_token)
        registration_client_uri = f"{str(deployment.issuer or settings.issuer).rstrip('/')}/register/{client_id}"

    metadata = _merge_registration_metadata(payload, derived_metadata=derived_metadata)
    registration = await create_handler_record(
        ClientRegistration,
        db,
        {
            'client_id': client.id,
            'tenant_id': tenant.id,
            'registration_metadata': metadata,
            'contacts': payload.contacts,
            'software_id': payload.software_id,
            'software_version': payload.software_version,
            'registration_access_token_hash': registration_access_token_hash,
            'registration_client_uri': registration_client_uri,
        },
    )
    await append_audit_event_record(
        db,
        tenant_id=tenant.id,
        actor_client_id=client.id,
        event_type='client.registration.created',
        target_type='client',
        target_id=str(client.id),
        details={
            'redirect_uris': list(payload.redirect_uris),
            'grant_types': list(payload.grant_types),
            'response_types': list(payload.response_types),
            'token_endpoint_auth_method': payload.token_endpoint_auth_method,
            'token_endpoint_auth_signing_alg': payload.token_endpoint_auth_signing_alg,
            'tls_client_certificate_thumbprint': payload.tls_client_certificate_thumbprint,
            'self_signed_tls_client_certificate_thumbprint': payload.self_signed_tls_client_certificate_thumbprint,
            'tls_client_auth_subject_dn': payload.tls_client_auth_subject_dn,
            'tls_client_auth_san_dns': payload.tls_client_auth_san_dns,
            'tls_client_auth_san_uri': payload.tls_client_auth_san_uri,
            'tls_client_auth_san_ip': payload.tls_client_auth_san_ip,
            'tls_client_auth_san_email': payload.tls_client_auth_san_email,
            'application_type': metadata.get('application_type'),
            'native_application': metadata.get('native_application', False),
            'pkce_required': metadata.get('pkce_required', False),
            'post_logout_redirect_uris': payload.post_logout_redirect_uris,
            'frontchannel_logout_uri': payload.frontchannel_logout_uri,
            'backchannel_logout_uri': payload.backchannel_logout_uri,
        },
    )

    return await _registration_response(
        db=db,
        client=client,
        registration=registration,
        registration_access_token=registration_access_token,
        client_secret=None if policy.fapi_mode and payload.token_endpoint_auth_method in set(policy.allowed_client_auth_methods) else client_secret,
    )


async def get_registered_client(*, request, db, client_id: str):
    _, client, registration, bearer = await _require_registration_access(request=request, db=db, client_id=client_id)
    return await _registration_response(db=db, client=client, registration=registration, registration_access_token=bearer)


async def update_registered_client(*, request, db, client_id: str, payload: DynamicClientRegistrationManagementIn | None = None):
    _, client, registration, bearer = await _require_registration_access(request=request, db=db, client_id=client_id)
    if payload is None:
        body = await request.json() if hasattr(request, 'json') else {}
        payload = DynamicClientRegistrationManagementIn(**body)

    current = dict(registration.registration_metadata or {})
    tenant = await read_handler_record(Tenant, db, client.tenant_id)
    current.setdefault('tenant_slug', tenant.slug if tenant is not None else 'public')
    current.setdefault('redirect_uris', (client.redirect_uris or '').split())
    current.setdefault('grant_types', (client.grant_types or 'authorization_code').split())
    current.setdefault('response_types', (client.response_types or 'code').split())
    current.setdefault('token_endpoint_auth_method', 'client_secret_basic')

    incoming = payload.model_dump(exclude_none=True)
    current.update(incoming)
    validated = DynamicClientRegistrationIn(**current)
    deployment = deployment_from_request(request, settings)
    _, derived_metadata = await _validated_registration_payload(db=db, payload=validated, deployment=deployment)

    client = await update_handler_record(
        Client,
        db,
        client.id,
        {
            'redirect_uris': ' '.join(validated.redirect_uris),
            'grant_types': ' '.join(validated.grant_types),
            'response_types': ' '.join(validated.response_types),
        },
    )

    metadata = _merge_registration_metadata(validated, derived_metadata=derived_metadata)
    registration = await update_handler_record(
        ClientRegistration,
        db,
        registration.id,
        {
            'registration_metadata': metadata,
            'contacts': validated.contacts,
            'software_id': validated.software_id,
            'software_version': validated.software_version,
            'registration_access_token_hash': registration.registration_access_token_hash,
            'registration_client_uri': registration.registration_client_uri,
        },
    )
    await append_audit_event_record(
        db,
        tenant_id=client.tenant_id,
        actor_client_id=client.id,
        event_type='client.registration.updated',
        target_type='client',
        target_id=str(client.id),
        details={
            'updated_fields': sorted(incoming.keys()),
            'token_endpoint_auth_method': metadata.get('token_endpoint_auth_method'),
            'token_endpoint_auth_signing_alg': metadata.get('token_endpoint_auth_signing_alg'),
            'tls_client_certificate_thumbprint': metadata.get('tls_client_certificate_thumbprint'),
            'self_signed_tls_client_certificate_thumbprint': metadata.get('self_signed_tls_client_certificate_thumbprint'),
            'tls_client_auth_subject_dn': metadata.get('tls_client_auth_subject_dn'),
            'tls_client_auth_san_dns': metadata.get('tls_client_auth_san_dns'),
            'tls_client_auth_san_uri': metadata.get('tls_client_auth_san_uri'),
            'tls_client_auth_san_ip': metadata.get('tls_client_auth_san_ip'),
            'tls_client_auth_san_email': metadata.get('tls_client_auth_san_email'),
            'application_type': metadata.get('application_type'),
            'native_application': metadata.get('native_application', False),
            'pkce_required': metadata.get('pkce_required', False),
        },
    )
    return await _registration_response(db=db, client=client, registration=registration, registration_access_token=bearer)


async def delete_registered_client(*, request, db, client_id: str):
    _, client, registration, _ = await _require_registration_access(request=request, db=db, client_id=client_id)
    disabled_at = datetime.now(timezone.utc)
    await update_handler_record(ClientRegistration, db, registration.id, {'disabled_at': disabled_at})
    await update_handler_record(Client, db, client.id, {'is_active': False})
    await append_audit_event_record(
        db,
        tenant_id=client.tenant_id,
        actor_client_id=None,
        event_type='client.registration.deleted',
        target_type='client',
        target_id=str(client.id),
        details={'registration_client_uri': registration.registration_client_uri},
    )
    return {'status': 'deleted', 'client_id': str(client.id)}
