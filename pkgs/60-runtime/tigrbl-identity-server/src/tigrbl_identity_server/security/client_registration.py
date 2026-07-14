"""Runtime composition for durable client registration lifecycle operations."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from tigrbl_client_registration_capability import ClientRegistrationCapability
from tigrbl_identity_contracts.oauth import (
    ClientRegistrationCreateRequest,
    ClientRegistrationRecord,
    ClientRegistrationUpdateRequest,
)
from tigrbl_identity_storage_runtime.ops.audit import append_audit_event_record
from tigrbl_identity_storage_runtime.ops.common import field_value
from tigrbl_identity_storage_runtime.ops.oauth_state import (
    create_client_registration,
    disable_client_registration,
    read_client_registration,
    update_client_registration,
)


def _words(value: object, default: str) -> tuple[str, ...]:
    if isinstance(value, str):
        return tuple(value.split())
    if isinstance(value, (list, tuple)):
        return tuple(str(item) for item in value)
    return tuple(default.split())


def registration_record_from_aggregate(
    aggregate: Mapping[str, object] | None,
) -> ClientRegistrationRecord | None:
    """Normalize canonical table rows into the layer-02 registration contract."""

    if aggregate is None:
        return None
    client = aggregate.get("client")
    registration = aggregate.get("registration")
    if client is None or registration is None:
        raise TypeError("registration aggregate requires client and registration rows")
    metadata = dict(field_value(registration, "registration_metadata") or {})
    contacts = field_value(registration, "contacts") or ()
    return ClientRegistrationRecord(
        client_id=str(field_value(client, "id") or ""),
        tenant_id=str(field_value(client, "tenant_id") or ""),
        registration_id=str(field_value(registration, "id") or ""),
        redirect_uris=_words(field_value(client, "redirect_uris"), ""),
        grant_types=_words(
            field_value(client, "grant_types"),
            "authorization_code",
        ),
        response_types=_words(field_value(client, "response_types"), "code"),
        metadata=metadata,
        contacts=tuple(str(item) for item in contacts),
        software_id=field_value(registration, "software_id"),
        software_version=field_value(registration, "software_version"),
        registration_access_token_hash=field_value(
            registration, "registration_access_token_hash"
        ),
        registration_client_uri=field_value(
            registration, "registration_client_uri"
        ),
        issued_at=field_value(registration, "issued_at"),
        disabled_at=field_value(registration, "disabled_at"),
        client_active=bool(field_value(client, "is_active", True)),
    )


def build_client_registration_capability(db: Any) -> ClientRegistrationCapability:
    """Bind registration lifecycle and audit operations to one durable session."""

    async def create(
        request: ClientRegistrationCreateRequest,
    ) -> ClientRegistrationRecord:
        aggregate = await create_client_registration(
            {
                "payload": {
                    "client_id": request.client_id,
                    "tenant_id": request.tenant_id,
                    "client_secret_hash": request.client_secret_hash,
                    "redirect_uris": request.redirect_uris,
                    "grant_types": request.grant_types,
                    "response_types": request.response_types,
                    "metadata": dict(request.metadata),
                    "contacts": request.contacts,
                    "software_id": request.software_id,
                    "software_version": request.software_version,
                    "registration_access_token_hash": (
                        request.registration_access_token_hash
                    ),
                    "registration_client_uri": request.registration_client_uri,
                },
                "db": db,
            }
        )
        record = registration_record_from_aggregate(aggregate)
        if record is None:
            raise RuntimeError("registration creation returned no aggregate")
        return record

    async def get(client_id: str) -> ClientRegistrationRecord | None:
        aggregate = await read_client_registration(
            {"payload": {"client_id": client_id}, "db": db}
        )
        return registration_record_from_aggregate(aggregate)

    async def update(
        request: ClientRegistrationUpdateRequest,
    ) -> ClientRegistrationRecord:
        aggregate = await update_client_registration(
            {
                "payload": {
                    "client_id": request.client_id,
                    "redirect_uris": request.redirect_uris,
                    "grant_types": request.grant_types,
                    "response_types": request.response_types,
                    "metadata": dict(request.metadata),
                    "contacts": request.contacts,
                    "software_id": request.software_id,
                    "software_version": request.software_version,
                },
                "db": db,
            }
        )
        record = registration_record_from_aggregate(aggregate)
        if record is None:
            raise RuntimeError("registration update returned no aggregate")
        return record

    async def disable(client_id: str) -> ClientRegistrationRecord:
        aggregate = await disable_client_registration(
            {"payload": {"client_id": client_id}, "db": db}
        )
        record = registration_record_from_aggregate(aggregate)
        if record is None:
            raise RuntimeError("registration disable returned no aggregate")
        return record

    async def audit(event: Mapping[str, object]) -> None:
        await append_audit_event_record(
            {"payload": dict(event), "db": db}
        )

    return ClientRegistrationCapability(create, get, update, disable, audit)


__all__ = [
    "build_client_registration_capability",
    "registration_record_from_aggregate",
]
