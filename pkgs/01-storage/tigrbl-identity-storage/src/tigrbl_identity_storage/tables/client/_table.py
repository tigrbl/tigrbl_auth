"""Client model for the authentication service."""

from __future__ import annotations

import re
import uuid
from typing import Final
from typing import Any
from urllib.parse import urlparse

from tigrbl_identity_storage.framework import (
    ClientBase,
    relationship,
    Mapped,
    String,
    ColumnSpec,
    F,
    IO,
    S,
    acol,
)
from tigrbl_identity_runtime.settings import settings
from tigrbl_identity_jose.key_management import hash_pw, verify_pw
from tigrbl_auth_protocol_oauth.standards.native_apps import (
    RFC8252_SPEC_URL,
    is_native_redirect_uri,
    validate_native_redirect_uri,
)

_CLIENT_ID_RE: Final[re.Pattern[str]] = re.compile(r"^[A-Za-z0-9\-_]{8,64}$")


class Client(ClientBase):
    __table_args__ = ({"schema": "authn"},)

    tenant = relationship("Tenant", back_populates="clients")

    grant_types: Mapped[str] = acol(
        spec=ColumnSpec(storage=S(String, nullable=False, default="authorization_code"), field=F(), io=IO())
    )
    response_types: Mapped[str] = acol(
        spec=ColumnSpec(storage=S(String, nullable=False, default="code"), field=F(), io=IO())
    )


    def verify_secret(self, plain: str) -> bool:
        return verify_pw(plain, self.client_secret_hash)


    async def rotate_secret(self, db: Any, *, client_secret: str):
        from .._ops import record_id, update_record

        return await update_record(type(self), db, record_id(self), {"client_secret_hash": hash_pw(client_secret)})

    async def enable(self, db: Any):
        from .._ops import record_id, update_record

        return await update_record(type(self), db, record_id(self), {"is_active": True})

    async def disable(self, db: Any):
        from .._ops import record_id, update_record

        return await update_record(type(self), db, record_id(self), {"is_active": False})


__all__ = ["Client", "_CLIENT_ID_RE"]
