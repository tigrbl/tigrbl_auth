from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def enabled_tenant_record(repo_root: Path, tenant_slug: str) -> dict[str, Any] | None:
    record_path = Path(repo_root) / ".operator-state" / "tenant" / f"{tenant_slug}.json"
    if not record_path.exists():
        return None

    record = json.loads(record_path.read_text(encoding="utf-8"))
    if record is None:
        return None

    status = str(record.get("status") or "").lower()
    if status in {"deleted", "disabled", "revoked"}:
        return None
    if record.get("enabled") is False:
        return None
    return record


__all__ = ["enabled_tenant_record"]

# BEGIN classmethod-to-op_ctx migration
from tigrbl import op_ctx as _table_op_ctx
from . import _table as _table_module

for _table_name in dir(_table_module):
    if not _table_name.startswith("__"):
        globals().setdefault(_table_name, getattr(_table_module, _table_name))

@_table_op_ctx(bind=Tenant, alias="update_tenant", target="custom", rest=False)
async def update_tenant(cls, db: Any, *, tenant_id: uuid.UUID, **payload: Any) -> "Tenant | None":
    row = await first_record(cls, db, {"id": tenant_id})
    if row is None:
        return None
    return await update_record(cls, db, record_id(row), payload)

@_table_op_ctx(bind=Tenant, alias="disable_tenant", target="custom", rest=False)
async def disable_tenant(cls, db: Any, *, tenant_id: uuid.UUID) -> "Tenant | None":
    return await cls.update_tenant(db, tenant_id=tenant_id, is_active=False)

# END classmethod-to-op_ctx migration
