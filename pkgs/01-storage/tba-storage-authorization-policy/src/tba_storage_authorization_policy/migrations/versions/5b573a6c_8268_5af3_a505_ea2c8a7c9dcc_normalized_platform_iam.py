"""Add normalized RBAC and immutable policy publication records."""

from tigrbl_migrations import Migration
from tba_storage_authorization_policy.tables import (
    AuthorizationAction,
    AuthorizationGroup,
    AuthorizationGroupMembership,
    AuthorizationResourceType,
    PolicyApproval,
    PolicyPublication,
    RoleGrant,
    RolePermission,
)

REVISION = "5b573a6c-8268-5af3-a505-ea2c8a7c9dcc"
PARENT = "0ef0b038-e979-5ba7-b874-d36093292702"
MODELS = (
    AuthorizationResourceType,
    AuthorizationAction,
    AuthorizationGroup,
    AuthorizationGroupMembership,
    RolePermission,
    RoleGrant,
    PolicyApproval,
    PolicyPublication,
)


def upgrade(connection):
    for model in MODELS:
        model.__table__.create(bind=connection, checkfirst=True)


def downgrade(connection):
    for model in reversed(MODELS):
        model.__table__.drop(bind=connection, checkfirst=True)


MIGRATION = Migration(
    component="tigrbl.identity.storage.authorization-policy",
    revision=REVISION,
    parents=(PARENT,),
    kind="standard",
    reversible=True,
    upgrade=upgrade,
    downgrade=downgrade,
)
