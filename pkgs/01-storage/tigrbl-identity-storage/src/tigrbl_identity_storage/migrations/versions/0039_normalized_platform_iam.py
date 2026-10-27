"""Create normalized platform IAM tables before component ownership adoption."""

from tigrbl_identity_storage_authorization_policy.tables import AuthorizationAction, AuthorizationGroup, AuthorizationGroupMembership, AuthorizationResourceType, PolicyApproval, PolicyPublication, RoleGrant, RolePermission

revision = "0039_normalized_platform_iam"
down_revision = "0037_operator_tables"
branch_labels = None
depends_on = None
MODELS = (AuthorizationResourceType, AuthorizationAction, AuthorizationGroup, AuthorizationGroupMembership, RolePermission, RoleGrant, PolicyApproval, PolicyPublication)

def upgrade(conn) -> None:
    for model in MODELS:
        model.__table__.create(bind=conn, checkfirst=True)

def downgrade(conn) -> None:
    for model in reversed(MODELS):
        model.__table__.drop(bind=conn, checkfirst=True)
