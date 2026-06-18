from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from tigrbl_identity_jose.key_management import hash_pw
from tigrbl_identity_server.framework import (
    Depends,
    HTTPException,
    Request,
    TigrblRouter,
    status,
)
from tigrbl_identity_server.security.auth import get_current_principal
from tigrbl_identity_server.security.handler_records import list_handler_records, read_handler_record, update_handler_record
from tigrbl_identity_storage import ensure_identity_storage_importable
from tigrbl_identity_storage.tables.engine import get_db

ensure_identity_storage_importable()

from tigrbl_identity_storage.tables import AuthSession, Consent, User
from tigrbl_identity_storage.tables.auth_session import MyAccountSessionOut
from tigrbl_identity_storage.tables.consent import (
    MyAccountAuthorizedAppOut,
    MyAccountConsentOut,
)
from tigrbl_identity_storage.tables.user import (
    MyAccountMutationOut,
    MyAccountPasswordChangeIn,
    MyAccountProfileOut,
    MyAccountProfileUpdateIn,
)

api = router = TigrblRouter()
MY_ACCOUNT_TAGS = ["My Account"]


def _iso(value: datetime | None) -> str | None:
    if value is None:
        return None
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.isoformat()


def _profile_payload(user: User) -> MyAccountProfileOut:
    return MyAccountProfileOut(
        id=str(user.id),
        tenant_id=str(user.tenant_id),
        username=str(user.username),
        email=str(user.email),
        is_active=bool(user.is_active),
        must_change_password=bool(getattr(user, "must_change_password", False)),
        roles=list(getattr(user, "roles", ())),
        created_at=_iso(getattr(user, "created_at", None)),
        updated_at=_iso(getattr(user, "updated_at", None)),
    )


def _session_payload(session: AuthSession) -> MyAccountSessionOut:
    return MyAccountSessionOut(
        id=str(session.id),
        tenant_id=str(session.tenant_id),
        user_id=str(session.user_id),
        username=str(session.username),
        client_id=str(session.client_id) if session.client_id is not None else None,
        state=str(session.session_state or "active"),
        auth_time=_iso(getattr(session, "auth_time", None)),
        last_seen_at=_iso(getattr(session, "last_seen_at", None)),
        expires_at=_iso(getattr(session, "expires_at", None)),
        ended_at=_iso(getattr(session, "ended_at", None)),
    )


def _consent_payload(consent: Consent) -> MyAccountConsentOut:
    return MyAccountConsentOut(
        id=str(consent.id),
        tenant_id=str(consent.tenant_id),
        user_id=str(consent.user_id),
        client_id=str(consent.client_id),
        scope=str(consent.scope),
        claims=consent.claims,
        state=str(consent.state or "active"),
        granted_at=_iso(getattr(consent, "granted_at", None)),
        expires_at=_iso(getattr(consent, "expires_at", None)),
        revoked_at=_iso(getattr(consent, "revoked_at", None)),
    )


def _uuid(value: str, *, field: str) -> UUID:
    try:
        return UUID(str(value))
    except ValueError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"{field} not found") from exc


async def _current_user_row(current_user: User, db: Any) -> User:
    row = await read_handler_record(User, db, current_user.id)
    if (
        row is not None
        and str(getattr(row, "tenant_id", "")) != str(current_user.tenant_id)
    ):
        row = None
    if row is not None and not bool(getattr(row, "is_active", True)):
        row = None
    if row is None:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, "authenticated account required"
        )
    return row


@api.route(
    "/account/profile",
    methods=["GET"],
    response_model=MyAccountProfileOut,
    tags=MY_ACCOUNT_TAGS,
)
async def get_account_profile(
    current_user: User = Depends(get_current_principal),
    db: Any = Depends(get_db),
) -> MyAccountProfileOut:
    return _profile_payload(await _current_user_row(current_user, db))


@api.route(
    "/account/profile",
    methods=["PATCH"],
    response_model=MyAccountProfileOut,
    tags=MY_ACCOUNT_TAGS,
)
async def update_account_profile(
    request: Request,
    payload: MyAccountProfileUpdateIn | None = None,
    current_user: User = Depends(get_current_principal),
    db: Any = Depends(get_db),
) -> MyAccountProfileOut:
    if payload is None:
        body = await request.json() or {}
        payload = MyAccountProfileUpdateIn.model_validate(body)
    row = await _current_user_row(current_user, db)
    changes: dict[str, Any] = {}
    if payload.username is not None:
        changes["username"] = payload.username
    if payload.email is not None:
        changes["email"] = payload.email
    if changes:
        row = await update_handler_record(User, db, row.id, changes)
    return _profile_payload(row)


@api.route(
    "/account/sessions",
    methods=["GET"],
    response_model=list[MyAccountSessionOut],
    tags=MY_ACCOUNT_TAGS,
)
async def list_account_sessions(
    current_user: User = Depends(get_current_principal),
    db: Any = Depends(get_db),
) -> list[MyAccountSessionOut]:
    rows = await list_handler_records(
        AuthSession,
        db,
        {"user_id": current_user.id, "tenant_id": current_user.tenant_id},
    )
    return [_session_payload(row) for row in rows]


@api.route(
    "/account/sessions/{session_id}",
    methods=["DELETE"],
    response_model=MyAccountMutationOut,
    tags=MY_ACCOUNT_TAGS,
)
async def revoke_account_session(
    session_id: str,
    current_user: User = Depends(get_current_principal),
    db: Any = Depends(get_db),
) -> MyAccountMutationOut:
    session_uuid = _uuid(session_id, field="session")
    row = await read_handler_record(AuthSession, db, session_uuid)
    if (
        row is not None
        and (
            str(getattr(row, "user_id", "")) != str(current_user.id)
            or str(getattr(row, "tenant_id", "")) != str(current_user.tenant_id)
        )
    ):
        row = None
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "session not found")
    now = datetime.now(timezone.utc)
    row = await update_handler_record(
        AuthSession,
        db,
        row.id,
        {
            "session_state": "revoked",
            "ended_at": row.ended_at or now,
            "logout_reason": row.logout_reason or "account_self_service",
        },
    )
    return MyAccountMutationOut(status="revoked", id=str(row.id))


@api.route(
    "/account/consents",
    methods=["GET"],
    response_model=list[MyAccountConsentOut],
    tags=MY_ACCOUNT_TAGS,
)
async def list_account_consents(
    current_user: User = Depends(get_current_principal),
    db: Any = Depends(get_db),
) -> list[MyAccountConsentOut]:
    rows = await list_handler_records(
        Consent,
        db,
        {"user_id": current_user.id, "tenant_id": current_user.tenant_id},
    )
    return [_consent_payload(row) for row in rows]


@api.route(
    "/account/consents/{consent_id}",
    methods=["DELETE"],
    response_model=MyAccountMutationOut,
    tags=MY_ACCOUNT_TAGS,
)
async def revoke_account_consent(
    consent_id: str,
    current_user: User = Depends(get_current_principal),
    db: Any = Depends(get_db),
) -> MyAccountMutationOut:
    consent_uuid = _uuid(consent_id, field="consent")
    row = await read_handler_record(Consent, db, consent_uuid)
    if (
        row is not None
        and (
            str(getattr(row, "user_id", "")) != str(current_user.id)
            or str(getattr(row, "tenant_id", "")) != str(current_user.tenant_id)
        )
    ):
        row = None
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "consent not found")
    row = await update_handler_record(
        Consent,
        db,
        row.id,
        {"state": "revoked", "revoked_at": row.revoked_at or datetime.now(timezone.utc)},
    )
    return MyAccountMutationOut(status="revoked", id=str(row.id))


@api.route(
    "/account/authorized-apps",
    methods=["GET"],
    response_model=list[MyAccountAuthorizedAppOut],
    tags=MY_ACCOUNT_TAGS,
)
async def list_account_authorized_apps(
    current_user: User = Depends(get_current_principal),
    db: Any = Depends(get_db),
) -> list[MyAccountAuthorizedAppOut]:
    rows = await list_handler_records(
        Consent,
        db,
        {"user_id": current_user.id, "tenant_id": current_user.tenant_id},
    )
    return [
        MyAccountAuthorizedAppOut(
            client_id=str(row.client_id),
            tenant_id=str(row.tenant_id),
            scope=str(row.scope),
            consent_state=str(row.state or "active"),
            granted_at=_iso(getattr(row, "granted_at", None)),
            revoked_at=_iso(getattr(row, "revoked_at", None)),
        )
        for row in rows
    ]


@api.route(
    "/account/authorized-apps/{client_id}",
    methods=["DELETE"],
    response_model=MyAccountMutationOut,
    tags=MY_ACCOUNT_TAGS,
)
async def revoke_account_authorized_app(
    client_id: str,
    current_user: User = Depends(get_current_principal),
    db: Any = Depends(get_db),
) -> MyAccountMutationOut:
    client_uuid = _uuid(client_id, field="client")
    rows = await list_handler_records(
        Consent,
        db,
        {
            "client_id": client_uuid,
            "user_id": current_user.id,
            "tenant_id": current_user.tenant_id,
        },
    )
    if not rows:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "authorized app not found")
    now = datetime.now(timezone.utc)
    for row in rows:
        await update_handler_record(
            Consent,
            db,
            row.id,
            {"state": "revoked", "revoked_at": row.revoked_at or now},
        )
    return MyAccountMutationOut(status="revoked", id=str(client_uuid))


@api.route(
    "/account/password/change",
    methods=["POST"],
    response_model=MyAccountMutationOut,
    tags=MY_ACCOUNT_TAGS,
)
async def change_account_password(
    request: Request,
    payload: MyAccountPasswordChangeIn | None = None,
    current_user: User = Depends(get_current_principal),
    db: Any = Depends(get_db),
) -> MyAccountMutationOut:
    if payload is None:
        body = await request.json() or {}
        payload = MyAccountPasswordChangeIn.model_validate(body)
    row = await _current_user_row(current_user, db)
    if not row.verify_password(payload.current_password):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "invalid current password")
    row = await update_handler_record(
        User,
        db,
        row.id,
        {
            "password_hash": hash_pw(payload.new_password),
            "must_change_password": False,
            "password_reset_token_hash": None,
            "password_reset_expires_at": None,
        },
    )
    return MyAccountMutationOut(status="changed", id=str(row.id))


__all__ = ["router", "api"]
