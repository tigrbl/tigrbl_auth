async def upsert_client_registration_async(
    *,
    client_id: UUID,
    tenant_id: UUID | None = None,
    metadata: dict[str, Any] | None = None,
    contacts: Iterable[str] | None = None,
    software_id: str | None = None,
    software_version: str | None = None,
    registration_access_token_hash: str | None = None,
    registration_client_uri: str | None = None,
) -> ClientRegistration:
    async with _session() as session:
        row = await session.scalar(select(ClientRegistration).where(ClientRegistration.client_id == client_id))
        if row is None:
            row = ClientRegistration(client_id=client_id, tenant_id=tenant_id)
            session.add(row)
        row.tenant_id = tenant_id or row.tenant_id
        row.registration_metadata = metadata or row.registration_metadata
        row.contacts = list(contacts) if contacts is not None else row.contacts
        row.software_id = software_id or row.software_id
        row.software_version = software_version or row.software_version
        row.registration_access_token_hash = registration_access_token_hash or row.registration_access_token_hash
        row.registration_client_uri = registration_client_uri or row.registration_client_uri
        row.issued_at = row.issued_at or datetime.now(timezone.utc)
        await session.commit()
        try:
            await session.refresh(row)
        except Exception:
            pass
        return row


async def append_audit_event_async(
    *,
    tenant_id: UUID | None = None,
    actor_user_id: UUID | None = None,
    actor_client_id: UUID | None = None,
    session_id: UUID | None = None,
    event_type: str,
    target_type: str | None = None,
    target_id: str | None = None,
    outcome: str = "success",
    request_id: str | None = None,
    details: dict[str, Any] | None = None,
) -> AuditEvent:
    async with _session() as session:
        effective_tenant_id = tenant_id
        if effective_tenant_id is None:
            effective_tenant_id = await session.scalar(select(Tenant.id))
        row = AuditEvent(
            tenant_id=effective_tenant_id,
            actor_user_id=actor_user_id,
            actor_client_id=actor_client_id,
            session_id=session_id,
            event_type=event_type,
            target_type=target_type,
            target_id=target_id,
            outcome=outcome,
            request_id=request_id,
            details=details,
            occurred_at=datetime.now(timezone.utc),
        )
        session.add(row)
        await session.commit()
        try:
            await session.refresh(row)
        except Exception:
            pass
        return row


# Sync wrappers used by existing helper/test surfaces.
record_token = upsert_token_record = lambda token, claims=None, token_kind=None, token_type_hint=None: _run(
    upsert_token_record_async(token, claims, token_kind=token_kind, token_type_hint=token_type_hint)
)
get_token_record = lambda token: _run(get_token_record_async(token))
unregister_token = lambda token: _run(remove_token_record_async(token))
revoke_token = lambda token, token_type_hint=None, reason=None: _run(
    revoke_token_async(token, token_type_hint=token_type_hint, reason=reason)
)
mark_token_used = lambda token, successor_token=None, reason="refresh_rotated": _run(
    mark_token_used_async(token, successor_token=successor_token, reason=reason)
)
revoke_refresh_family = lambda family_id, reason="refresh_token_reuse_detected", reuse_token=None: _run(
    revoke_refresh_family_async(family_id, reason=reason, reuse_token=reuse_token)
)
is_token_revoked = lambda token: bool(_run(is_token_revoked_async(token)))
introspect_token = lambda token: _run(introspect_token_async(token))
reset_token_state = lambda: _run(reset_token_state_async())
create_session = lambda **kwargs: _run(create_session_async(**kwargs))
touch_session = lambda session_id: _run(touch_session_async(session_id))
get_session = lambda session_id: _run(get_session_async(session_id))
get_active_session = lambda session_id: _run(get_active_session_async(session_id))
rotate_session_cookie_secret = lambda session_id, **kwargs: _run(rotate_session_cookie_secret_async(session_id, **kwargs))
bind_session_client = lambda session_id, **kwargs: _run(bind_session_client_async(session_id, **kwargs))
terminate_session = lambda session_id, **kwargs: _run(terminate_session_async(session_id, **kwargs))
get_latest_logout_for_session = lambda session_id: _run(get_latest_logout_for_session_async(session_id))
update_logout_metadata = lambda logout_id, **kwargs: _run(update_logout_metadata_async(logout_id, **kwargs))
mark_logout_channel = lambda logout_id, **kwargs: _run(mark_logout_channel_async(logout_id, **kwargs))
get_client_registration = lambda client_id: _run(get_client_registration_async(client_id))
record_consent = lambda **kwargs: _run(record_consent_async(**kwargs))
revoke_consent = lambda consent_id: _run(revoke_consent_async(consent_id))
upsert_client_registration = lambda **kwargs: _run(upsert_client_registration_async(**kwargs))
append_audit_event = lambda **kwargs: _run(append_audit_event_async(**kwargs))


# -----------------------------------------------------------------------------
# Operator-plane checkpoint helpers
# -----------------------------------------------------------------------------


def load_operator_records(resource: str, *, repo_root=None):
    from pathlib import Path
    from tigrbl_auth.services._operator_store import load_records

    root = Path(repo_root) if repo_root is not None else Path.cwd()
    return load_records(root, resource)


def operator_state_root(*, repo_root=None):
    from pathlib import Path
    from tigrbl_auth.services._operator_store import operator_state_root as _root

    root = Path(repo_root) if repo_root is not None else Path.cwd()
    return _root(root)


def append_operator_audit(event, *, repo_root=None):
    from pathlib import Path
    from tigrbl_auth.services._operator_store import append_jsonl, audit_log_path

    root = Path(repo_root) if repo_root is not None else Path.cwd()
    append_jsonl(audit_log_path(root), event)
    return event


__all__ = [
    "operator_state_root",
    "load_operator_records",
    "append_operator_audit",
    "append_audit_event",
    "append_audit_event_async",
    "create_session",
    "create_session_async",
    "get_token_record",
    "get_token_record_async",
    "get_session",
    "get_session_async",
    "get_active_session",
    "get_active_session_async",
    "introspect_token",
    "introspect_token_async",
    "is_token_revoked",
    "is_token_revoked_async",
    "mark_logout_channel",
    "mark_logout_channel_async",
    "record_consent",
    "record_consent_async",
    "record_token",
    "reset_token_state",
    "reset_token_state_async",
    "mark_token_used",
    "mark_token_used_async",
    "revoke_consent",
    "revoke_consent_async",
    "revoke_refresh_family",
    "revoke_refresh_family_async",
    "revoke_token",
    "revoke_token_async",
    "rotate_session_cookie_secret",
    "rotate_session_cookie_secret_async",
    "bind_session_client",
    "bind_session_client_async",
    "terminate_session",
    "terminate_session_async",
    "token_hash",
    "touch_session",
    "touch_session_async",
    "get_latest_logout_for_session",
    "get_latest_logout_for_session_async",
    "update_logout_metadata",
    "update_logout_metadata_async",
    "get_client_registration",
    "get_client_registration_async",
    "unregister_token",
    "upsert_client_registration",
    "upsert_client_registration_async",
    "upsert_token_record",
    "upsert_token_record_async",
]
