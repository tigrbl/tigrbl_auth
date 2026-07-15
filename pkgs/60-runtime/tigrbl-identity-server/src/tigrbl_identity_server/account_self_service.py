"""Durable runtime composition for current-account self-service."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from tigrbl_account_self_service import AccountSelfServiceCapability
from tigrbl_identity_contracts.account_self_service import (
    AccountAuthenticationError,
    AccountConsent,
    AccountMutation,
    AccountPrincipal,
    AccountProfile,
    AccountProfileUpdate,
    AccountSession,
    AccountValidationError,
)
from tigrbl_identity_storage.tables import AuthSession, User
from tigrbl_identity_storage_runtime.engine import get_db
from tigrbl_identity_storage_runtime.ops.common import (
    field_value,
    list_table_records,
    read_table_record,
    update_table_record,
)
from tigrbl_identity_storage_runtime.ops.consents import (
    list_consents_for_user,
    revoke_consent_for_user,
    revoke_consents_for_client,
)
from tigrbl_identity_storage_runtime.ops.sessions import terminate_session
from tigrbl_secret_hashing_bcrypt_provider import BcryptSecretHasher


_SECRET_HASHER = BcryptSecretHasher()


def _iso(value: Any) -> str | None:
    return value.isoformat() if value is not None else None


def account_principal(value: object) -> AccountPrincipal:
    if isinstance(value, AccountPrincipal):
        return value
    identity_id = field_value(value, "id")
    tenant_id = field_value(value, "tenant_id")
    if identity_id is None or tenant_id is None:
        raise AccountAuthenticationError("authenticated account required")
    return AccountPrincipal(str(identity_id), str(tenant_id))


def _profile(row: object) -> AccountProfile:
    return AccountProfile(
        identity_id=str(field_value(row, "id")),
        tenant_id=str(field_value(row, "tenant_id")),
        username=str(field_value(row, "username")),
        email=str(field_value(row, "email")),
        is_active=bool(field_value(row, "is_active", True)),
        must_change_password=bool(field_value(row, "must_change_password", False)),
        roles=tuple(field_value(row, "roles", ())),
        created_at=_iso(field_value(row, "created_at")),
        updated_at=_iso(field_value(row, "updated_at")),
    )


def _session(row: object) -> AccountSession:
    return AccountSession(
        session_id=str(field_value(row, "id")),
        tenant_id=str(field_value(row, "tenant_id")),
        identity_id=str(field_value(row, "user_id")),
        username=str(field_value(row, "username")),
        client_id=(
            str(field_value(row, "client_id"))
            if field_value(row, "client_id") is not None
            else None
        ),
        state=str(field_value(row, "session_state", "active")),
        auth_time=_iso(field_value(row, "auth_time")),
        last_seen_at=_iso(field_value(row, "last_seen_at")),
        expires_at=_iso(field_value(row, "expires_at")),
        ended_at=_iso(field_value(row, "ended_at")),
    )


def _consent(row: object) -> AccountConsent:
    return AccountConsent(
        consent_id=str(field_value(row, "id")),
        tenant_id=str(field_value(row, "tenant_id")),
        identity_id=str(field_value(row, "user_id")),
        client_id=str(field_value(row, "client_id")),
        scope=str(field_value(row, "scope", "")),
        claims=field_value(row, "claims"),
        state=str(field_value(row, "state", "active")),
        granted_at=field_value(row, "granted_at"),
        expires_at=field_value(row, "expires_at"),
        revoked_at=field_value(row, "revoked_at"),
    )


def _uuid(value: str) -> UUID | None:
    try:
        return UUID(str(value))
    except (TypeError, ValueError):
        return None


def build_account_self_service_capability(db: object) -> AccountSelfServiceCapability:
    async def user_row(principal: AccountPrincipal) -> object:
        identifier = _uuid(principal.identity_id)
        row = await read_table_record(User, db, identifier) if identifier else None
        if (
            row is None
            or str(field_value(row, "tenant_id", "")) != principal.tenant_id
            or not bool(field_value(row, "is_active", True))
        ):
            raise AccountAuthenticationError("authenticated account required")
        return row

    async def profile_reader(principal: AccountPrincipal) -> AccountProfile:
        return _profile(await user_row(principal))

    async def profile_updater(
        principal: AccountPrincipal, spec: AccountProfileUpdate
    ) -> AccountProfile:
        row = await user_row(principal)
        changes = {
            name: value
            for name in ("username", "email")
            if (value := getattr(spec, name)) is not None
        }
        if changes:
            row = await update_table_record(User, db, field_value(row, "id"), changes)
        return _profile(row)

    async def password_changer(
        principal: AccountPrincipal, current_password: str, new_password: str
    ) -> AccountMutation:
        row = await user_row(principal)
        verification = _SECRET_HASHER.verify_secret(
            current_password, field_value(row, "password_hash")
        )
        if not verification.verified:
            raise AccountValidationError("invalid current password")
        row = await update_table_record(
            User,
            db,
            field_value(row, "id"),
            {
                "password_hash": _SECRET_HASHER.hash_secret(new_password).encoded,
                "must_change_password": False,
                "password_reset_token_hash": None,
                "password_reset_expires_at": None,
            },
        )
        return AccountMutation("changed", str(field_value(row, "id")))

    async def session_lister(principal: AccountPrincipal) -> tuple[AccountSession, ...]:
        rows = await list_table_records(
            AuthSession,
            db,
            {
                "user_id": _uuid(principal.identity_id),
                "tenant_id": _uuid(principal.tenant_id),
            },
        )
        return tuple(_session(row) for row in rows)

    async def session_revoker(
        principal: AccountPrincipal, session_id: str
    ) -> AccountMutation | None:
        identifier = _uuid(session_id)
        if identifier is None:
            return None
        rows = await list_table_records(
            AuthSession,
            db,
            {
                "id": identifier,
                "user_id": _uuid(principal.identity_id),
                "tenant_id": _uuid(principal.tenant_id),
            },
        )
        if not rows:
            return None
        updated = await terminate_session(
            {
                "path_params": {"id": identifier},
                "payload": {
                    "session_id": identifier,
                    "session_state": "revoked",
                    "reason": "account_self_service",
                },
                "db": db,
            }
        )
        return AccountMutation("revoked", str(field_value(updated, "id")))

    async def consent_lister(principal: AccountPrincipal) -> tuple[AccountConsent, ...]:
        rows = await list_consents_for_user(
            {
                "payload": {
                    "user_id": principal.identity_id,
                    "tenant_id": principal.tenant_id,
                },
                "db": db,
            }
        )
        return tuple(_consent(row) for row in rows)

    async def consent_revoker(
        principal: AccountPrincipal, consent_id: str
    ) -> AccountConsent | None:
        row = await revoke_consent_for_user(
            {
                "path_params": {"id": consent_id},
                "payload": {
                    "user_id": principal.identity_id,
                    "tenant_id": principal.tenant_id,
                },
                "db": db,
            }
        )
        return _consent(row) if row is not None else None

    async def authorized_app_revoker(
        principal: AccountPrincipal, client_id: str
    ) -> tuple[AccountConsent, ...]:
        rows = await revoke_consents_for_client(
            {
                "path_params": {"client_id": client_id},
                "payload": {
                    "user_id": principal.identity_id,
                    "tenant_id": principal.tenant_id,
                },
                "db": db,
            }
        )
        return tuple(_consent(row) for row in rows)

    return AccountSelfServiceCapability(
        profile_reader=profile_reader,
        profile_updater=profile_updater,
        password_changer=password_changer,
        session_lister=session_lister,
        session_revoker=session_revoker,
        consent_lister=consent_lister,
        consent_revoker=consent_revoker,
        authorized_app_revoker=authorized_app_revoker,
    )


async def current_account_principal(
    request: object,
    *,
    authorization: str | None = None,
    api_key: str | None = None,
    dpop: str | None = None,
    db: object,
) -> AccountPrincipal:
    from tigrbl_identity_server.security.auth import get_current_principal

    row = await get_current_principal(
        request,
        authorization=authorization,
        api_key=api_key,
        dpop=dpop,
        db=db,
    )
    return account_principal(row)


def account_self_service_for_request(
    request: object, db: object
) -> AccountSelfServiceCapability:
    state = getattr(getattr(request, "app", None), "state", None)
    registry = getattr(state, "tigrbl_auth_capability_registry", None)
    if registry is not None:
        try:
            capability = registry.materialize("account.self-service", db)
        except KeyError:
            pass
        else:
            if not isinstance(capability, AccountSelfServiceCapability):
                raise TypeError("account factory returned an invalid capability")
            return capability
    return build_account_self_service_capability(db)


__all__ = [
    "account_principal",
    "account_self_service_for_request",
    "build_account_self_service_capability",
    "current_account_principal",
    "get_db",
]
