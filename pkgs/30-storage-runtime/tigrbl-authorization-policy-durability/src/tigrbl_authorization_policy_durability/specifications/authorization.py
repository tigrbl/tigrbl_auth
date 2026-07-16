"""Authorization table aliases and executable runtime specifications."""

from tigrbl_identity_storage.tables import (
    AttributePolicy,
    DelegatedAdminScope,
    Role,
    TenantMembership,
)

from tigrbl_table_durability import deriveRuntimeTableSpec
from tigrbl_table_durability import makeRuntimeOperation
from tigrbl_authorization_policy_durability.operations.authorization import (
    assign_role,
    delegated_scope_for_subject,
    grant_delegated_scope,
    grant_membership,
    list_active_attribute_policies,
    list_active_delegated_scopes,
    list_roles_for_tenant,
    revoke_delegated_scope,
    role_names_for_principal,
    upsert_role,
    upsert_attribute_policy,
)

TenantMembershipTable = TenantMembership
DelegatedAdminScopeTable = DelegatedAdminScope
RoleTable = Role
AttributePolicyTable = AttributePolicy

AttributePolicyRuntimeSpec = deriveRuntimeTableSpec(
    AttributePolicyTable,
    operations=(
        makeRuntimeOperation(
            alias="upsert_with_conditions", handler=upsert_attribute_policy
        ),
        makeRuntimeOperation(
            alias="list_active_with_conditions",
            handler=list_active_attribute_policies,
            tx_scope="read_only",
            persist="skip",
        ),
    ),
)

RoleRuntimeSpec = deriveRuntimeTableSpec(
    RoleTable,
    operations=(
        makeRuntimeOperation(alias="create_role", handler=upsert_role),
        makeRuntimeOperation(
            alias="list_for_tenant",
            handler=list_roles_for_tenant,
            tx_scope="read_only",
            persist="skip",
        ),
    ),
)

TenantMembershipRuntimeSpec = deriveRuntimeTableSpec(
    TenantMembershipTable,
    operations=(
        makeRuntimeOperation(alias="grant_membership", handler=grant_membership),
        makeRuntimeOperation(alias="assign_role", handler=assign_role),
        makeRuntimeOperation(
            alias="role_names_for_principal",
            handler=role_names_for_principal,
            tx_scope="read_only",
            persist="skip",
        ),
    ),
)
DelegatedAdminScopeRuntimeSpec = deriveRuntimeTableSpec(
    DelegatedAdminScopeTable,
    operations=(
        makeRuntimeOperation(alias="grant_scope", handler=grant_delegated_scope),
        makeRuntimeOperation(alias="revoke_scope", handler=revoke_delegated_scope),
        makeRuntimeOperation(
            alias="lookup",
            handler=delegated_scope_for_subject,
            tx_scope="read_only",
            persist="skip",
        ),
        makeRuntimeOperation(
            alias="list_active",
            handler=list_active_delegated_scopes,
            tx_scope="read_only",
            persist="skip",
        ),
    ),
)

__all__ = [
    "AttributePolicyRuntimeSpec",
    "AttributePolicyTable",
    "DelegatedAdminScopeRuntimeSpec",
    "DelegatedAdminScopeTable",
    "TenantMembershipRuntimeSpec",
    "TenantMembershipTable",
    "RoleRuntimeSpec",
    "RoleTable",
]
