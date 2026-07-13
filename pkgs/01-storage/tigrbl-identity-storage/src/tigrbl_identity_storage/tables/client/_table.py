"""Client model for the authentication service."""

from __future__ import annotations

import re
from typing import Final

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

_CLIENT_ID_RE: Final[re.Pattern[str]] = re.compile(r"^[A-Za-z0-9\-_]{8,64}$")


class Client(ClientBase):
    __table_args__ = ({"schema": "authn"},)

    tenant = relationship("Tenant", back_populates="clients")

    grant_types: Mapped[str] = acol(
        spec=ColumnSpec(
            storage=S(String, nullable=False, default="authorization_code"),
            field=F(),
            io=IO(),
        )
    )
    response_types: Mapped[str] = acol(
        spec=ColumnSpec(
            storage=S(String, nullable=False, default="code"), field=F(), io=IO()
        )
    )

__all__ = ["Client", "_CLIENT_ID_RE"]
