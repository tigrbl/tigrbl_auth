from __future__ import annotations

__all__: list[str] = []

# BEGIN classmethod-to-op_ctx migration
from tigrbl import op_ctx as _table_op_ctx
from . import _table as _table_module

for _table_name in dir(_table_module):
    if not _table_name.startswith("__"):
        globals().setdefault(_table_name, getattr(_table_module, _table_name))

@_table_op_ctx(bind=SubjectAlias, alias="bind_alias", target="custom", rest=False)
async def bind_alias(
    cls,
    db: Any,
    *,
    principal_id: str,
    issuer: str,
    subject: str,
    tenant_id: str | None = None,
    verified: bool = False,
) -> "SubjectAlias":
    existing = await _lookup(cls, db, issuer=issuer, subject=subject, tenant_id=tenant_id)
    payload = {
        "principal_id": principal_id,
        "issuer": issuer,
        "subject": subject,
        "tenant_id": tenant_id,
        "verified": str(bool(verified)).lower(),
    }
    if existing is not None:
        return await update_record(cls, db, record_id(existing), payload)
    return await create_record(cls, db, payload)

async def _lookup(
    cls,
    db: Any,
    *,
    issuer: str,
    subject: str,
    tenant_id: str | None = None,
) -> "SubjectAlias | None":
    filters: dict[str, Any] = {"issuer": issuer, "subject": subject}
    if tenant_id is not None:
        filters["tenant_id"] = tenant_id
    return await first_record(cls, db, filters)

@_table_op_ctx(bind=SubjectAlias, alias="verify_alias", target="custom", rest=False)
async def verify_alias(cls, db: Any, *, issuer: str, subject: str, tenant_id: str | None = None) -> "SubjectAlias | None":
    row = await _lookup(cls, db, issuer=issuer, subject=subject, tenant_id=tenant_id)
    if row is None:
        return None
    return await update_record(cls, db, record_id(row), {"verified": "true"})

# END classmethod-to-op_ctx migration
