"""Owned mapped-table inventory."""

from .attribute_policy import AttributePolicy
from .authorization_invariant import AuthorizationInvariant
from .delegated_admin_scope import DelegatedAdminScope
from .invariant_evaluation import InvariantEvaluation
from .invariant_violation import InvariantViolation
from .policy import Policy
from .policy_condition import PolicyCondition
from .policy_set import PolicySet
from .policy_set_member import PolicySetMember
from .policy_target import PolicyTarget
from .policy_version import PolicyVersion
from .role import Role
from .tenant_membership import TenantMembership

TABLE_MODELS = (
    TenantMembership,
    Role,
    AttributePolicy,
    PolicyCondition,
    Policy,
    PolicyVersion,
    PolicySet,
    PolicySetMember,
    PolicyTarget,
    DelegatedAdminScope,
    AuthorizationInvariant,
    InvariantEvaluation,
    InvariantViolation,
)
TABLE_MODEL_BY_NAME = {model.__name__: model for model in TABLE_MODELS}
TABLE_MODEL_BY_TABLENAME = {model.__tablename__: model for model in TABLE_MODELS}
__all__ = [model.__name__ for model in TABLE_MODELS] + [
    "TABLE_MODELS", "TABLE_MODEL_BY_NAME", "TABLE_MODEL_BY_TABLENAME",
]
