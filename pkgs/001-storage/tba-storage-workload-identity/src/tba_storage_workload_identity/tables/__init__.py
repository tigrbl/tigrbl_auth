"""Owned mapped-table inventory."""

from .spiffe_state import SvidRecord, SpiffeTrustBundle, TrustDomainFederation
from .workload_credential_state import WorkloadReferenceBinding, WorkloadCredentialEntitlement
from .workload_identity import WorkloadIdentity

TABLE_MODELS = (
    WorkloadIdentity,
    SvidRecord,
    SpiffeTrustBundle,
    TrustDomainFederation,
    WorkloadReferenceBinding,
    WorkloadCredentialEntitlement,
)
TABLE_MODEL_BY_NAME = {model.__name__: model for model in TABLE_MODELS}
TABLE_MODEL_BY_TABLENAME = {model.__tablename__: model for model in TABLE_MODELS}
__all__ = [model.__name__ for model in TABLE_MODELS] + [
    "TABLE_MODELS", "TABLE_MODEL_BY_NAME", "TABLE_MODEL_BY_TABLENAME",
]
