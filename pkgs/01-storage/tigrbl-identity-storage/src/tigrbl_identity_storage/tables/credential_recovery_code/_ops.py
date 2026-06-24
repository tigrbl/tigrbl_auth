from __future__ import annotations

# BEGIN classmethod-to-op_ctx migration
from tigrbl import op_ctx as _table_op_ctx
from . import _table as _table_module

for _table_name in dir(_table_module):
    if not _table_name.startswith("__"):
        globals().setdefault(_table_name, getattr(_table_module, _table_name))

async def _lookup_active(cls, db: Any, *, code_digest: str) -> "CredentialRecoveryCode | None":
    return await first_record(cls, db, {"code_digest": code_digest, "status": "active"})

@_table_op_ctx(bind=CredentialRecoveryCode, alias="consume", target="custom", rest=False)
async def consume(cls, db: Any, *, code_digest: str) -> "CredentialRecoveryCode | None":
    row = await _lookup_active(cls, db, code_digest=code_digest)
    if row is None:
        return None
    return await update_record(cls, db, record_id(row), {"status": "consumed", "consumed_at": utc_now()})

@_table_op_ctx(bind=CredentialRecoveryCode, alias="revoke", target="custom", rest=False)
async def revoke(cls, db: Any, *, credential_id: str) -> list["CredentialRecoveryCode"]:
    rows = await list_records(cls, db, {"credential_id": credential_id})
    revoked = []
    for row in rows:
        revoked.append(await update_record(cls, db, record_id(row), {"status": "revoked"}))
    return revoked

# END classmethod-to-op_ctx migration
