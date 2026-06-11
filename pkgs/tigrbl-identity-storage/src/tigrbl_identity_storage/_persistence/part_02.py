async def introspect_token_async(token: str) -> dict[str, Any]:
    digest = token_hash(token)
    now = datetime.now(timezone.utc)
    try:
        async with _session() as session:
            record = await session.scalar(select(TokenRecord).where(TokenRecord.token_hash == digest))
            if record is None:
                return {"active": False}
            if record.expires_at is not None:
                expiry = record.expires_at if record.expires_at.tzinfo is not None else record.expires_at.replace(tzinfo=timezone.utc)
                if expiry <= now:
                    record.active = False
                    record.revoked_reason = record.revoked_reason or "expired"
                    await session.commit()
                    return {"active": False}
            revoked = await session.scalar(select(RevokedToken).where(RevokedToken.token_hash == digest))
            if revoked is not None or record.revoked_at is not None or not record.active:
                record.active = False
                record.last_introspected_at = now
                await session.commit()
                return {"active": False}
            record.last_introspected_at = now
            payload = dict(record.claims or {})
            payload.setdefault("sub", record.subject)
            if record.scope:
                payload.setdefault("scope", record.scope)
            if record.client_id is not None:
                payload.setdefault("client_id", str(record.client_id))
            if record.issuer:
                payload.setdefault("iss", record.issuer)
            if record.expires_at is not None:
                payload.setdefault("exp", int(record.expires_at.timestamp()))
            payload["active"] = True
            await session.commit()
            return payload
    except Exception:
        return {"active": False}


async def reset_token_state_async() -> None:
    try:
        async with _session() as session:
            await session.execute(delete(RevokedToken))
            await session.execute(delete(TokenRecord))
            await session.commit()
    except Exception:
        return None


async def create_session_async(
    *,
    user_id: UUID,
    tenant_id: UUID,
    username: str,
    client_id: UUID | None = None,
    expires_at: datetime | None = None,
    cookie_secret_hash: str | None = None,
    session_state_salt: str | None = None,
) -> AuthSession:
    async with _session() as session:
        now = datetime.now(timezone.utc)
        row = AuthSession(
            user_id=user_id,
            tenant_id=tenant_id,
            username=username,
            client_id=client_id,
            auth_time=now,
            session_state="active",
            session_state_salt=session_state_salt,
            cookie_secret_hash=cookie_secret_hash,
            cookie_issued_at=now if cookie_secret_hash else None,
            cookie_rotated_at=now if cookie_secret_hash else None,
            expires_at=expires_at,
            last_seen_at=now,
        )
        session.add(row)
        await session.commit()
        try:
            await session.refresh(row)
        except Exception:
            pass
        return row


async def touch_session_async(session_id: UUID) -> AuthSession | None:
    async with _session() as session:
        row = await session.scalar(select(AuthSession).where(AuthSession.id == session_id))
        if row is None:
            return None
        row.last_seen_at = datetime.now(timezone.utc)
        await session.commit()
        return row


async def terminate_session_async(
    session_id: UUID,
    *,
    initiated_by: str = "rp_logout",
    reason: str = "logout",
    frontchannel_required: bool = False,
    backchannel_required: bool = False,
    metadata: dict[str, Any] | None = None,
) -> LogoutState | None:
    now = datetime.now(timezone.utc)
    async with _session() as session:
        row = await session.scalar(select(AuthSession).where(AuthSession.id == session_id))
        if row is None:
            return None

        existing_rows = (await session.execute(select(LogoutState).where(LogoutState.session_id == session_id))).scalars().all()
        if existing_rows:
            existing_rows = sorted(existing_rows, key=lambda item: str(getattr(item, 'created_at', '') or getattr(item, 'id', '')), reverse=True)
            latest = existing_rows[0]
            current_meta = dict(getattr(latest, 'logout_metadata', {}) or {})
            if metadata:
                current_meta.update(metadata)
            latest.logout_metadata = current_meta or None
            latest.frontchannel_required = bool(latest.frontchannel_required or frontchannel_required)
            latest.backchannel_required = bool(latest.backchannel_required or backchannel_required)
            await session.commit()
            return latest

        row.session_state = "terminated"
        row.ended_at = now
        row.logout_reason = reason
        logout = LogoutState(
            session_id=row.id,
            sid=str(row.id),
            status="pending" if frontchannel_required or backchannel_required else "complete",
            initiated_by=initiated_by,
            reason=reason,
            frontchannel_required=frontchannel_required,
            backchannel_required=backchannel_required,
            propagated_at=None if frontchannel_required or backchannel_required else now,
            logout_metadata=metadata,
        )
        session.add(logout)
        await session.commit()
        try:
            await session.refresh(logout)
        except Exception:
            pass
        return logout


async def mark_logout_channel_async(
    logout_id: UUID,
    *,
    channel: str,
    status: str = "complete",
    reason: str | None = None,
    retry_after_seconds: int | None = None,
    metadata: dict[str, Any] | None = None,
) -> LogoutState | None:
    now = datetime.now(timezone.utc)
    now_iso = now.replace(microsecond=0).isoformat()
    async with _session() as session:
        row = await session.scalar(select(LogoutState).where(LogoutState.id == logout_id))
        if row is None:
            return None
        current_meta = dict(row.logout_metadata or {})
        channel_meta = dict(current_meta.get(channel) or {})
        if metadata:
            channel_meta.update(dict(metadata))
        delivery = dict(channel_meta.get("delivery") or {})
        prior_attempts = int(delivery.get("attempts", 0) or 0)
        delivery["channel"] = channel
        delivery["status"] = str(status)
        delivery["attempts"] = max(prior_attempts + 1, 1)
        delivery["updated_at"] = now_iso
        if reason is not None:
            delivery["reason"] = str(reason)
        if retry_after_seconds is not None:
            delivery["retry_after_seconds"] = int(retry_after_seconds)
        if status == "complete":
            delivery["completed_at"] = now_iso
        channel_meta["delivery"] = delivery
        channel_meta["status"] = delivery["status"]
        current_meta[channel] = channel_meta
        current_meta[f"{channel}_delivery"] = dict(delivery)
        row.logout_metadata = current_meta or None
        if channel == "frontchannel" and status == "complete":
            row.frontchannel_completed_at = now
        elif channel == "backchannel" and status == "complete":
            row.backchannel_completed_at = now
        if (not row.frontchannel_required or row.frontchannel_completed_at is not None) and (
            not row.backchannel_required or row.backchannel_completed_at is not None
        ):
            row.status = "complete"
            row.propagated_at = now
        else:
            row.status = "pending" if status != "complete" else row.status
        await session.commit()
        return row


async def get_session_async(session_id: UUID) -> AuthSession | None:
    async with _session() as session:
        return await session.scalar(select(AuthSession).where(AuthSession.id == session_id))


async def get_active_session_async(session_id: UUID) -> AuthSession | None:
    async with _session() as session:
        row = await session.scalar(select(AuthSession).where(AuthSession.id == session_id))
        if row is None:
            return None
        if row.ended_at is not None or str(row.session_state).lower() in {"terminated", "ended", "revoked"}:
            return None
        if row.expires_at is not None:
            expiry = row.expires_at if row.expires_at.tzinfo is not None else row.expires_at.replace(tzinfo=timezone.utc)
            if expiry <= datetime.now(timezone.utc):
                row.session_state = "expired"
                row.ended_at = row.ended_at or datetime.now(timezone.utc)
                await session.commit()
                return None
        return row


async def rotate_session_cookie_secret_async(session_id: UUID, *, cookie_secret_hash: str) -> AuthSession | None:
    async with _session() as session:
        row = await session.scalar(select(AuthSession).where(AuthSession.id == session_id))
        if row is None:
            return None
        now = datetime.now(timezone.utc)
        row.cookie_secret_hash = cookie_secret_hash
        row.cookie_rotated_at = now
        row.cookie_issued_at = row.cookie_issued_at or now
        row.last_seen_at = now
        await session.commit()
        return row


async def bind_session_client_async(session_id: UUID, *, client_id: UUID | None) -> AuthSession | None:
    async with _session() as session:
        row = await session.scalar(select(AuthSession).where(AuthSession.id == session_id))
        if row is None:
            return None
        row.client_id = client_id
        row.last_seen_at = datetime.now(timezone.utc)
        await session.commit()
        return row


async def get_latest_logout_for_session_async(session_id: UUID) -> LogoutState | None:
    async with _session() as session:
        rows = (await session.execute(select(LogoutState).where(LogoutState.session_id == session_id))).scalars().all()
        if not rows:
            return None
        rows = sorted(rows, key=lambda item: str(getattr(item, 'created_at', '') or getattr(item, 'id', '')), reverse=True)
        return rows[0]


async def update_logout_metadata_async(logout_id: UUID, *, metadata: dict[str, Any] | None = None, status: str | None = None) -> LogoutState | None:
    async with _session() as session:
        row = await session.scalar(select(LogoutState).where(LogoutState.id == logout_id))
        if row is None:
            return None
        current = dict(row.logout_metadata or {})
        if metadata:
            current.update(metadata)
        row.logout_metadata = current or None
        if status is not None:
            row.status = status
        await session.commit()
        return row


async def get_client_registration_async(client_id: UUID) -> ClientRegistration | None:
    async with _session() as session:
        return await session.scalar(select(ClientRegistration).where(ClientRegistration.client_id == client_id))


async def record_consent_async(
    *,
    user_id: UUID,
    tenant_id: UUID,
    client_id: UUID,
    scope: str,
    claims: dict[str, Any] | None = None,
    expires_at: datetime | None = None,
) -> Consent:
    async with _session() as session:
        row = Consent(
            user_id=user_id,
            tenant_id=tenant_id,
            client_id=client_id,
            scope=scope,
            claims=claims,
            granted_at=datetime.now(timezone.utc),
            expires_at=expires_at,
            state="active",
        )
        session.add(row)
        await session.commit()
        try:
            await session.refresh(row)
        except Exception:
            pass
        return row


async def revoke_consent_async(consent_id: UUID) -> Consent | None:
    async with _session() as session:
        row = await session.scalar(select(Consent).where(Consent.id == consent_id))
        if row is None:
            return None
        row.state = "revoked"
        row.revoked_at = datetime.now(timezone.utc)
        await session.commit()
        return row


