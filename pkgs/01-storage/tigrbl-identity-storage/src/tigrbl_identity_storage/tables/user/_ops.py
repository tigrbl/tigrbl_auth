from __future__ import annotations

__all__: list[str] = []

# BEGIN classmethod-to-op_ctx migration
from tigrbl import op_ctx as _table_op_ctx

import uuid
from .._ops import first_record, list_records, record_id, update_record
from ._table import User
from tigrbl_identity_jose.key_management import hash_pw
from typing import Any

@_table_op_ctx(bind=User, alias="new", target="custom", rest=False)
def new(cls, *, tenant_id: uuid.UUID, username: str, email: str, password: str):
    return cls(
        tenant_id=tenant_id,
        username=username,
        email=email,
        password_hash=hash_pw(password) if password is not None else None,
    )

@_table_op_ctx(bind=User, alias="update_user", target="custom", rest=False)
async def update_user(cls, db: Any, *, user_id: uuid.UUID, **payload: Any) -> "User | None":
    if "password" in payload and "password_hash" not in payload:
        payload["password_hash"] = hash_pw(str(payload.pop("password")))
    row = await first_record(cls, db, {"id": user_id})
    if row is None:
        return None
    return await update_record(cls, db, record_id(row), payload)

@_table_op_ctx(bind=User, alias="disable_user", target="custom", rest=False)
async def disable_user(cls, db: Any, *, user_id: uuid.UUID) -> "User | None":
    return await cls.update_user(db, user_id=user_id, is_active=False)

@_table_op_ctx(bind=User, alias="lookup_by_identifier", target="custom", rest=False)
async def lookup_by_identifier(cls, db: Any, *, identifier: str) -> "User | None":
    for row in await list_records(cls, db, {"username": identifier}):
        if getattr(row, "is_active", True):
            return row
    for row in await list_records(cls, db, {"email": identifier}):
        if getattr(row, "is_active", True):
            return row
    return None

# END classmethod-to-op_ctx migration
