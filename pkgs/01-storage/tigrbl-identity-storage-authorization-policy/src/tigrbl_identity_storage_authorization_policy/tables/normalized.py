"""Normalized RBAC, publication, and access-governance storage models."""

from tigrbl_identity_core.orm import Boolean, GUIDPk, JSON, Mapped, RestOltpTable, S, String, Timestamped, acol


class AuthorizationResourceType(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "authorization_resource_types"
    __table_args__ = ({"schema": "authn"},)
    key: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    tenant_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))

class AuthorizationAction(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "authorization_actions"
    __table_args__ = ({"schema": "authn"},)
    key: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    resource_type: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    required_acr: Mapped[str | None] = acol(storage=S(String(255), nullable=True))

class AuthorizationGroup(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "authorization_groups"
    __table_args__ = ({"schema": "authn"},)
    tenant_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    name: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="active", index=True))

class AuthorizationGroupMembership(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "authorization_group_memberships"
    __table_args__ = ({"schema": "authn"},)
    tenant_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    group_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    principal_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="active", index=True))

class RolePermission(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "role_permissions"
    __table_args__ = ({"schema": "authn"},)
    tenant_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    role_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    action_key: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    effect: Mapped[str] = acol(storage=S(String(16), nullable=False, default="allow", index=True))

class RoleGrant(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "role_grants"
    __table_args__ = ({"schema": "authn"},)
    tenant_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    principal_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    principal_type: Mapped[str] = acol(storage=S(String(32), nullable=False, index=True))
    role_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    resource_type: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    resource_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    valid_from: Mapped[str | None] = acol(storage=S(String(64), nullable=True))
    expires_at: Mapped[str | None] = acol(storage=S(String(64), nullable=True))
    revoked_at: Mapped[str | None] = acol(storage=S(String(64), nullable=True))
    conditions: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))

class PolicyApproval(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "policy_approvals"
    __table_args__ = ({"schema": "authn"},)
    tenant_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    policy_version_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    approver_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    decision: Mapped[str] = acol(storage=S(String(32), nullable=False, index=True))
    reason: Mapped[str | None] = acol(storage=S(String(2000), nullable=True))

class PolicyPublication(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "policy_publications"
    __table_args__ = ({"schema": "authn"},)
    tenant_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    policy_version_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    manifest_hash: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    active: Mapped[bool] = acol(storage=S(Boolean, nullable=False, default=True, index=True))
    supersedes_publication_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True))

__all__ = [
    "AuthorizationResourceType",
    "AuthorizationAction",
    "AuthorizationGroup",
    "AuthorizationGroupMembership",
    "RolePermission",
    "RoleGrant",
    "PolicyApproval",
    "PolicyPublication",
]
