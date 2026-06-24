from __future__ import annotations

__all__: list[str] = []

# BEGIN classmethod-to-op_ctx migration
from tigrbl import op_ctx as _table_op_ctx
from . import _table as _table_module

for _table_name in dir(_table_module):
    if not _table_name.startswith("__"):
        globals().setdefault(_table_name, getattr(_table_module, _table_name))

async def _create_grant(cls, db: Any, **payload: Any) -> "DelegationGrant":
    payload.setdefault("status", "active")
    payload.setdefault("effective_at", utc_now())
    return await create_record(cls, db, payload)

async def _inspect_grant(cls, db: Any, *, grant_id: uuid.UUID) -> "DelegationGrant | None":
    return await first_record(cls, db, {"id": grant_id})

@_table_op_ctx(bind=DelegationGrant, alias="activate_grant", target="custom", rest=False)
async def activate_grant(
    cls,
    db: Any,
    *,
    grant_id: uuid.UUID,
    effective_at: dt.datetime | None = None,
) -> "DelegationGrant | None":
    row = await _inspect_grant(cls, db, grant_id=grant_id)
    if row is None:
        return None
    return await update_record(
        cls,
        db,
        record_id(row),
        {"status": "active", "effective_at": effective_at or utc_now()},
    )

@_table_op_ctx(bind=DelegationGrant, alias="revoke_grant", target="custom", rest=False)
async def revoke_grant(
    cls,
    db: Any,
    *,
    grant_id: uuid.UUID,
    revoked_by: str | None = None,
    reason: str | None = None,
    collapse_descendants: bool = False,
) -> "DelegationGrant | None":
    row = await _inspect_grant(cls, db, grant_id=grant_id)
    if row is None:
        return None
    revoked = await update_record(
        cls,
        db,
        record_id(row),
        {"status": "revoked", "revoked_at": utc_now(), "revoked_by": revoked_by, "revoked_reason": reason},
    )
    if collapse_descendants:
        children = await _list_grants(cls, db, parent_grant_id=record_id(row))
        for child in children:
            if field(child, "status") not in TERMINAL_GRANT_STATUSES:
                await cls.revoke_grant(
                    db,
                    grant_id=record_id(child),
                    revoked_by=revoked_by,
                    reason="ancestor-revoked",
                    collapse_descendants=True,
                )
        await DelegationGrantEdge.deactivate_children(db, parent_grant_id=record_id(row))
    return revoked

@_table_op_ctx(bind=DelegationGrant, alias="expire_grant", target="custom", rest=False)
async def expire_grant(
    cls,
    db: Any,
    *,
    grant_id: uuid.UUID,
    expires_at: dt.datetime | None = None,
) -> "DelegationGrant | None":
    row = await _inspect_grant(cls, db, grant_id=grant_id)
    if row is None:
        return None
    return await update_record(
        cls,
        db,
        record_id(row),
        {"status": "expired", "expires_at": expires_at or utc_now()},
    )

@_table_op_ctx(bind=DelegationGrant, alias="replace_grant", target="custom", rest=False)
async def replace_grant(
    cls,
    db: Any,
    *,
    grant_id: uuid.UUID,
    replaced_by: str | None = None,
    reason: str = "replaced",
    **payload: Any,
) -> "DelegationGrant | None":
    current = await _inspect_grant(cls, db, grant_id=grant_id)
    if current is None:
        return None
    replacement_payload = {
        "tenant_id": field(current, "tenant_id"),
        "realm": field(current, "realm", ""),
        "delegator_subject": field(current, "delegator_subject"),
        "delegate_subject": field(current, "delegate_subject"),
        "delegate_type": field(current, "delegate_type", "subject"),
        "parent_grant_id": record_id(current),
        "source_authority_ref": field(current, "source_authority_ref"),
        "policy_version": field(current, "policy_version"),
        "provenance_id": field(current, "provenance_id"),
        "constraints": field(current, "constraints"),
        "expires_at": field(current, "expires_at"),
    }
    replacement_payload.update(payload)
    replacement = await _create_grant(cls, db, **replacement_payload)
    await update_record(
        cls,
        db,
        record_id(current),
        {
            "status": "replaced",
            "revoked_at": utc_now(),
            "revoked_by": replaced_by,
            "revoked_reason": reason,
            "replaced_by_grant_id": record_id(replacement),
        },
    )
    return replacement

async def _list_grants(
    cls,
    db: Any,
    *,
    tenant_id: uuid.UUID | None = None,
    delegator_subject: str | None = None,
    delegate_subject: str | None = None,
    parent_grant_id: uuid.UUID | None = None,
    status: str | None = None,
) -> list["DelegationGrant"]:
    filters = {
        key: value
        for key, value in {
            "tenant_id": tenant_id,
            "delegator_subject": delegator_subject,
            "delegate_subject": delegate_subject,
            "parent_grant_id": parent_grant_id,
            "status": status,
        }.items()
        if value is not None
    }
    return await list_records(cls, db, filters)

@_table_op_ctx(bind=DelegationGrantEdge, alias="link_edge", target="custom", rest=False)
async def link_edge(cls, db: Any, **payload: Any) -> "DelegationGrantEdge":
    payload.setdefault("active", True)
    return await create_record(cls, db, payload)

async def _list_children(cls, db: Any, *, parent_grant_id: uuid.UUID) -> list["DelegationGrantEdge"]:
    return await list_records(cls, db, {"parent_grant_id": parent_grant_id})

@_table_op_ctx(bind=DelegationGrantEdge, alias="deactivate_children", target="custom", rest=False)
async def deactivate_children(cls, db: Any, *, parent_grant_id: uuid.UUID) -> list["DelegationGrantEdge"]:
    updated: list["DelegationGrantEdge"] = []
    for edge in await _list_children(cls, db, parent_grant_id=parent_grant_id):
        updated.append(await update_record(cls, db, record_id(edge), {"active": False}))
    return updated

# END classmethod-to-op_ctx migration
