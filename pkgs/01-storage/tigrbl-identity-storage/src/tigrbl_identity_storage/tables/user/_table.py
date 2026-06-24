"""User model for the authentication service."""

from __future__ import annotations

import uuid
import datetime as dt
from typing import Any
from datetime import timezone

from tigrbl_identity_storage.framework import (
    UserBase,
    Bootstrappable,
    BaseModel,
    Depends,
    Field,
    HTTPException,
    JSONResponse,
    LargeBinary,
    Mapped,
    Boolean,
    RedirectResponse,
    Request,
    Response,
    String,
    TZDateTime,
    TigrblRouter,
    relationship,
    status,
    Header,
    F,
    IO,
    S,
    acol,
    ColumnSpec,
    constr,
)

from tigrbl_identity_jose.key_management import hash_pw
from .._ops import create_record, delete_record, first_record, list_records, read_record, record_id, update_record
from ..engine import get_db

DEFAULT_BOOTSTRAP_SUPERUSER_ID = uuid.UUID("FFFFFFFF-0000-0000-0000-000000000001")
DEFAULT_BOOTSTRAP_SUPERUSER_PASSWORD = "AdminPass123!"
_email = constr(strip_whitespace=True, min_length=3, max_length=120)
_password = constr(min_length=8, max_length=256)
_username = constr(strip_whitespace=True, min_length=3, max_length=80)


class AdminIdentityOut(BaseModel):
    id: str
    tenant_id: str
    username: str
    email: str
    is_active: bool = True
    is_admin: bool = False
    is_superuser: bool = False
    must_change_password: bool = False
    roles: list[str] = Field(default_factory=list)
    created_at: str | None = None
    updated_at: str | None = None


class AdminIdentityProvisionIn(BaseModel):
    tenant_id: str
    username: _username
    email: _email
    password: _password
    is_admin: bool = False
    is_superuser: bool = False
    must_change_password: bool = True


class AdminIdentityUpdateIn(BaseModel):
    username: _username | None = None
    email: _email | None = None
    password: _password | None = None
    is_active: bool | None = None
    is_admin: bool | None = None
    is_superuser: bool | None = None
    must_change_password: bool | None = None


class MyAccountProfileOut(BaseModel):
    id: str
    tenant_id: str
    username: str
    email: str
    is_active: bool = True
    must_change_password: bool = False
    roles: list[str] = Field(default_factory=list)
    created_at: str | None = None
    updated_at: str | None = None


class MyAccountProfileUpdateIn(BaseModel):
    username: _username | None = None
    email: _email | None = None


class MyAccountPasswordChangeIn(BaseModel):
    current_password: _password
    new_password: _password


class MyAccountMutationOut(BaseModel):
    status: str
    id: str | None = None


class CredsIn(BaseModel):
    identifier: constr(strip_whitespace=True, min_length=3, max_length=120)
    password: _password


class AdminPasswordResetRequestIn(BaseModel):
    identifier: constr(strip_whitespace=True, min_length=3, max_length=120)


class AdminPasswordResetCompleteIn(BaseModel):
    token: constr(strip_whitespace=True, min_length=16, max_length=256)
    password: _password


class AdminPasswordChangeIn(BaseModel):
    current_password: _password
    new_password: _password


class AdminSessionOut(BaseModel):
    authenticated: bool
    session_id: str | None = None
    user_id: str | None = None
    tenant_id: str | None = None
    username: str | None = None
    email: str | None = None
    is_admin: bool = False
    is_superuser: bool = False
    must_change_password: bool = False
    roles: list[str] = Field(default_factory=list)
    debug_reset_token: str | None = None


class User(UserBase, Bootstrappable):
    __table_args__ = ({"extend_existing": True, "schema": "authn"},)

    username: Mapped[str] = acol(
        spec=ColumnSpec(
            storage=S(String(32), nullable=False),
            field=F(constraints={"max_length": 32}, required_in=("create",)),
            io=IO(
                in_verbs=("create", "update", "replace"),
                out_verbs=("read", "list"),
                filter_ops=("eq", "ilike"),
                sortable=True,
            ),
        )
    )
    email: Mapped[str] = acol(
        spec=ColumnSpec(
            storage=S(String(120), nullable=False, unique=True),
            field=F(constraints={"max_length": 120}, required_in=("create",)),
            io=IO(
                in_verbs=("create", "update", "replace"),
                out_verbs=("read", "list"),
                filter_ops=("eq", "ilike"),
                sortable=True,
            ),
        )
    )
    password_hash: Mapped[bytes | None] = acol(
        spec=ColumnSpec(storage=S(LargeBinary(60)), io=IO(in_verbs=("create", "update", "replace")))
    )
    is_admin: Mapped[bool] = acol(
        spec=ColumnSpec(
            storage=S(Boolean, nullable=False, default=False),
            field=F(),
            io=IO(in_verbs=("create", "update", "replace"), out_verbs=("read", "list"), filter_ops=("eq",)),
        )
    )
    is_superuser: Mapped[bool] = acol(
        spec=ColumnSpec(
            storage=S(Boolean, nullable=False, default=False),
            field=F(),
            io=IO(in_verbs=("create", "update", "replace"), out_verbs=("read", "list"), filter_ops=("eq",)),
        )
    )
    must_change_password: Mapped[bool] = acol(
        spec=ColumnSpec(
            storage=S(Boolean, nullable=False, default=False),
            field=F(),
            io=IO(in_verbs=("create", "update", "replace"), out_verbs=("read", "list"), filter_ops=("eq",)),
        )
    )
    password_reset_token_hash: Mapped[str | None] = acol(
        spec=ColumnSpec(storage=S(String(128), nullable=True, index=True), io=IO(in_verbs=("update", "replace")))
    )
    password_reset_expires_at: Mapped[dt.datetime | None] = acol(
        spec=ColumnSpec(storage=S(TZDateTime, nullable=True), io=IO(in_verbs=("update", "replace"), out_verbs=("read",)))
    )

    tenant = relationship("Tenant", back_populates="users")


    def verify_password(self, plain: str) -> bool:
        from tigrbl_identity_jose.key_management import verify_pw
        if self.password_hash is None:
            return False
        return verify_pw(plain, self.password_hash)

    @property
    def roles(self) -> tuple[str, ...]:
        roles: list[str] = []
        if self.is_admin:
            roles.append("admin")
        if self.is_superuser:
            roles.append("superuser")
        return tuple(roles)

    @property
    def scopes(self) -> tuple[str, ...]:
        scopes: list[str] = []
        if self.is_admin:
            scopes.append("tigrbl_auth:admin")
        if self.is_superuser:
            scopes.append("tigrbl_auth:superuser")
        return tuple(scopes)

    DEFAULT_ROWS = [
        {
            "id": DEFAULT_BOOTSTRAP_SUPERUSER_ID,
            "tenant_id": uuid.UUID("FFFFFFFF-0000-0000-0000-000000000000"),
            "username": "admin",
            "email": "admin@example.com",
            "password_hash": hash_pw(DEFAULT_BOOTSTRAP_SUPERUSER_PASSWORD),
            "is_admin": True,
            "is_superuser": True,
            "must_change_password": True,
            "is_active": True,
        }
    ]


admin_api = admin_router = TigrblRouter()
account_api = account_router = TigrblRouter()
MY_ACCOUNT_TAGS = ["My Account"]
ADMIN_AUTH_TAGS = ["Admin Auth"]


from ._account_route import (  # noqa: E402
    _current_principal_dependency,
    _iso,
    _not_found_uuid,
    change_account_password,
    get_account_profile,
    update_account_profile,
)
from ._admin_auth_route import (  # noqa: E402
    admin_change_password,
    admin_forgot_password,
    admin_login,
    admin_login_browser_redirect,
    admin_logout,
    admin_reset_password,
    admin_session,
)
from ._admin_identity_route import (  # noqa: E402
    admin_create_identity,
    admin_delete_identity,
    admin_list_identities,
    admin_update_identity,
)


for _name, _func in {
    "admin_change_password": admin_change_password,
    "admin_create_identity": admin_create_identity,
    "admin_delete_identity": admin_delete_identity,
    "admin_forgot_password": admin_forgot_password,
    "admin_list_identities": admin_list_identities,
    "admin_login": admin_login,
    "admin_login_browser_redirect": admin_login_browser_redirect,
    "admin_logout": admin_logout,
    "admin_reset_password": admin_reset_password,
    "admin_session": admin_session,
    "admin_update_identity": admin_update_identity,
    "change_account_password": change_account_password,
    "get_account_profile": get_account_profile,
    "update_account_profile": update_account_profile,
}.items():
    setattr(User, _name, staticmethod(_func))


__all__ = [
    "AdminIdentityOut",
    "AdminIdentityProvisionIn",
    "AdminIdentityUpdateIn",
    "AdminPasswordChangeIn",
    "AdminPasswordResetCompleteIn",
    "AdminPasswordResetRequestIn",
    "AdminSessionOut",
    "CredsIn",
    "DEFAULT_BOOTSTRAP_SUPERUSER_ID",
    "DEFAULT_BOOTSTRAP_SUPERUSER_PASSWORD",
    "MyAccountMutationOut",
    "MyAccountPasswordChangeIn",
    "MyAccountProfileOut",
    "MyAccountProfileUpdateIn",
    "User",
    "admin_api",
    "admin_router",
    "admin_change_password",
    "account_api",
    "account_router",
    "admin_create_identity",
    "admin_delete_identity",
    "admin_forgot_password",
    "admin_list_identities",
    "admin_login",
    "admin_login_browser_redirect",
    "admin_logout",
    "admin_reset_password",
    "admin_session",
    "admin_update_identity",
    "change_account_password",
    "get_account_profile",
    "update_account_profile",
]
