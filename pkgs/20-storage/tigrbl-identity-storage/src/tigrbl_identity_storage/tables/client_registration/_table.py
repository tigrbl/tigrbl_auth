"""Durable dynamic client registration metadata."""

from __future__ import annotations

import datetime as dt
from pathlib import Path
from typing import Any

from tigrbl_identity_storage.framework import (
    Base,
    BaseModel,
    Depends,
    EmailStr,
    Field,
    TenantColumn,
    Timestamped,
    TigrblRouter,
    S,
    acol,
    JSON,
    Mapped,
    String,
    TZDateTime,
    GUIDPk,
    ForeignKeySpec,
    PgUUID,
    UUID,
    constr,
)
from .._ops import create_record, delete_record, first_record, record_id, update_record, utc_now
from ..engine import get_db

_tenant_slug = constr(strip_whitespace=True, min_length=3, max_length=120)


class DynamicClientRegistrationIn(BaseModel):
    tenant_slug: _tenant_slug = Field(default="public")
    redirect_uris: list[str]
    grant_types: list[str] = Field(default_factory=lambda: ["authorization_code"])
    response_types: list[str] = Field(default_factory=lambda: ["code"])
    token_endpoint_auth_method: str = Field(default="client_secret_basic")
    token_endpoint_auth_signing_alg: str | None = None
    tls_client_certificate_thumbprint: str | None = None
    self_signed_tls_client_certificate_thumbprint: str | None = None
    tls_client_auth_subject_dn: str | None = None
    tls_client_auth_san_dns: str | None = None
    tls_client_auth_san_uri: str | None = None
    tls_client_auth_san_ip: str | None = None
    tls_client_auth_san_email: str | None = None
    application_type: str | None = None
    scope: str | None = None
    client_name: str | None = None
    client_uri: str | None = None
    jwks_uri: str | None = None
    contacts: list[EmailStr] | None = None
    software_id: str | None = None
    software_version: str | None = None
    post_logout_redirect_uris: list[str] | None = None
    frontchannel_logout_uri: str | None = None
    frontchannel_logout_session_required: bool = True
    backchannel_logout_uri: str | None = None
    backchannel_logout_session_required: bool = True


class DynamicClientRegistrationOut(BaseModel):
    client_id: str
    client_secret: str | None = None
    client_id_issued_at: int
    client_secret_expires_at: int = 0
    redirect_uris: list[str]
    grant_types: list[str]
    response_types: list[str]
    token_endpoint_auth_method: str
    token_endpoint_auth_signing_alg: str | None = None
    tls_client_certificate_thumbprint: str | None = None
    self_signed_tls_client_certificate_thumbprint: str | None = None
    tls_client_auth_subject_dn: str | None = None
    tls_client_auth_san_dns: str | None = None
    tls_client_auth_san_uri: str | None = None
    tls_client_auth_san_ip: str | None = None
    tls_client_auth_san_email: str | None = None
    application_type: str | None = None
    scope: str | None = None
    client_name: str | None = None
    client_uri: str | None = None
    jwks_uri: str | None = None
    contacts: list[EmailStr] | None = None
    software_id: str | None = None
    software_version: str | None = None
    post_logout_redirect_uris: list[str] | None = None
    frontchannel_logout_uri: str | None = None
    frontchannel_logout_session_required: bool = True
    backchannel_logout_uri: str | None = None
    backchannel_logout_session_required: bool = True
    registration_access_token: str | None = None
    registration_client_uri: str | None = None


class DynamicClientRegistrationManagementIn(BaseModel):
    tenant_slug: _tenant_slug | None = None
    redirect_uris: list[str] | None = None
    grant_types: list[str] | None = None
    response_types: list[str] | None = None
    token_endpoint_auth_method: str | None = None
    token_endpoint_auth_signing_alg: str | None = None
    tls_client_certificate_thumbprint: str | None = None
    self_signed_tls_client_certificate_thumbprint: str | None = None
    tls_client_auth_subject_dn: str | None = None
    tls_client_auth_san_dns: str | None = None
    tls_client_auth_san_uri: str | None = None
    tls_client_auth_san_ip: str | None = None
    tls_client_auth_san_email: str | None = None
    application_type: str | None = None
    scope: str | None = None
    client_name: str | None = None
    client_uri: str | None = None
    jwks_uri: str | None = None
    contacts: list[EmailStr] | None = None
    software_id: str | None = None
    software_version: str | None = None
    post_logout_redirect_uris: list[str] | None = None
    frontchannel_logout_uri: str | None = None
    frontchannel_logout_session_required: bool | None = None
    backchannel_logout_uri: str | None = None
    backchannel_logout_session_required: bool | None = None


class ClientRegistration(Base, GUIDPk, Timestamped, TenantColumn):
    __tablename__ = "client_registrations"
    __table_args__ = ({"schema": "authn"},)

    client_id: Mapped[UUID] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.clients.id"), nullable=False, unique=True, index=True)
    )
    software_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    software_version: Mapped[str | None] = acol(storage=S(String(128), nullable=True))
    contacts: Mapped[list[str] | None] = acol(storage=S(JSON, nullable=True))
    registration_metadata: Mapped[dict[str, Any] | None] = acol(storage=S(JSON, nullable=True))
    registration_access_token_hash: Mapped[str | None] = acol(
        storage=S(String(128), nullable=True, unique=True, index=True)
    )
    registration_client_uri: Mapped[str | None] = acol(storage=S(String(1000), nullable=True))
    issued_at: Mapped[dt.datetime] = acol(
        storage=S(TZDateTime, nullable=False, default=lambda: dt.datetime.now(dt.timezone.utc))
    )
    rotated_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True))
    disabled_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))

    @classmethod
    async def register_client(cls, db: Any, **payload: Any) -> "ClientRegistration":
        payload.setdefault("issued_at", utc_now())
        return await create_record(cls, db, payload)

    @classmethod
    async def read_registration(cls, db: Any, *, client_id: UUID) -> "ClientRegistration | None":
        return await first_record(cls, db, {"client_id": client_id})

    @classmethod
    async def update_registration(cls, db: Any, *, client_id: UUID, **payload: Any) -> "ClientRegistration | None":
        row = await cls.read_registration(db, client_id=client_id)
        if row is None:
            return None
        return await update_record(cls, db, record_id(row), payload)

    @classmethod
    async def delete_registration(cls, db: Any, *, client_id: UUID) -> Any:
        row = await cls.read_registration(db, client_id=client_id)
        if row is None:
            return None
        return await delete_record(cls, db, record_id(row))


api = router = TigrblRouter()


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[5]


def _sync_client_registration(command: str, registration: Any) -> None:
    from tigrbl_identity_storage.operator_store import OperationContext
    from tigrbl_identity_operator.operator_service import create_resource, delete_resource, update_resource

    if isinstance(registration, dict):
        payload = dict(registration)
    elif hasattr(registration, "model_dump"):
        payload = registration.model_dump(mode="json")
    else:
        payload = dict(getattr(registration, "__dict__", {}))
    client_id = str(payload.get("client_id") or payload.get("id"))
    if not client_id:
        return
    context = OperationContext(repo_root=_repo_root(), command=command, resource="client", actor="rest")
    patch = {
        "client_id": client_id,
        "tenant_id": payload.get("tenant_id"),
        "metadata": payload,
        "contacts": payload.get("contacts") or [],
        "software_id": payload.get("software_id"),
        "software_version": payload.get("software_version"),
        "registration_access_token_hash": payload.get("registration_access_token_hash"),
        "registration_client_uri": payload.get("registration_client_uri"),
    }
    if command.endswith(".delete"):
        try:
            delete_resource(context, record_id=client_id, if_missing="skip")
        except Exception:
            pass
        return
    existing_command = update_resource if command.endswith(".update") else create_resource
    try:
        existing_command(
            context,
            record_id=client_id,
            patch=patch,
            if_missing="create" if command.endswith(".update") else "error",
            if_exists="update" if command.endswith(".create") else "error",
        )
    except TypeError:
        if command.endswith(".update"):
            update_resource(context, record_id=client_id, patch=patch, if_missing="create")
        else:
            create_resource(context, record_id=client_id, patch=patch, if_exists="update")


@api.route("/register", methods=["POST"], response_model=DynamicClientRegistrationOut)
async def register(request: Any, db: Any = Depends(get_db)) -> Any:
    from ._route_op import register_client as register_client_request

    result = await register_client_request(request=request, db=db)
    _sync_client_registration("client.registration.create", result)
    return result


@api.route("/register/{client_id}", methods=["GET"], response_model=DynamicClientRegistrationOut)
async def register_get(request: Any, client_id: str, db: Any = Depends(get_db)) -> Any:
    from ._route_op import get_registered_client

    return await get_registered_client(request=request, db=db, client_id=client_id)


@api.route("/register/{client_id}", methods=["PUT"], response_model=DynamicClientRegistrationOut)
async def register_put(request: Any, client_id: str, db: Any = Depends(get_db)) -> Any:
    from ._route_op import update_registered_client

    result = await update_registered_client(request=request, db=db, client_id=client_id)
    _sync_client_registration("client.registration.update", result)
    return result


@api.route("/register/{client_id}", methods=["DELETE"])
async def register_delete(request: Any, client_id: str, db: Any = Depends(get_db)) -> Any:
    from ._route_op import delete_registered_client

    result = await delete_registered_client(request=request, db=db, client_id=client_id)
    _sync_client_registration("client.registration.delete", {"client_id": client_id})
    return result


ClientRegistration.register = staticmethod(register)  # type: ignore[attr-defined]
ClientRegistration.register_get = staticmethod(register_get)  # type: ignore[attr-defined]
ClientRegistration.register_put = staticmethod(register_put)  # type: ignore[attr-defined]
ClientRegistration.register_delete = staticmethod(register_delete)  # type: ignore[attr-defined]


__all__ = [
    "ClientRegistration",
    "DynamicClientRegistrationIn",
    "DynamicClientRegistrationManagementIn",
    "DynamicClientRegistrationOut",
    "api",
    "router",
    "register",
    "register_get",
    "register_put",
    "register_delete",
]
