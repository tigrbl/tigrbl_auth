"""Client model for the authentication service."""

from __future__ import annotations

import re
import uuid
from typing import Final
from urllib.parse import urlparse

from tigrbl_auth.framework import (
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
from tigrbl_auth.config.settings import settings
from tigrbl_auth.services.key_management import hash_pw, verify_pw
from tigrbl_auth.standards.oauth2.native_apps import (
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

    @classmethod
    def new(
        cls,
        tenant_id: uuid.UUID,
        client_id: str,
        client_secret: str,
        redirects: list[str],
    ):
        if not _CLIENT_ID_RE.fullmatch(client_id):
            raise ValueError("invalid client_id format")
        if settings.enforce_rfc8252:
            for uri in redirects:
                parsed = urlparse(uri)
                if is_native_redirect_uri(uri):
                    validate_native_redirect_uri(uri)
                elif parsed.scheme == "http":
                    raise ValueError(
                        f"redirect URI not permitted for native apps per RFC 8252: {RFC8252_SPEC_URL}"
                    )
        secret_hash = hash_pw(client_secret)
        try:
            obj_id: uuid.UUID | str = uuid.UUID(client_id)
        except ValueError:
            obj_id = client_id
        return cls(
            tenant_id=tenant_id,
            id=obj_id,
            client_secret_hash=secret_hash,
            redirect_uris=" ".join(redirects),
        )

    def verify_secret(self, plain: str) -> bool:
        return verify_pw(plain, self.client_secret_hash)


__all__ = ["Client", "_CLIENT_ID_RE"]
