"""Owned mapped-table inventory."""

from .operator_activity import OperatorActivity
from .operator_audit_event import OperatorAuditEvent
from .operator_metadata import OperatorMetadata
from .operator_record import OperatorRecord
from .operator_transaction import OperatorTransaction

TABLE_MODELS = (
    OperatorMetadata,
    OperatorRecord,
    OperatorTransaction,
    OperatorAuditEvent,
    OperatorActivity,
)
TABLE_MODEL_BY_NAME = {model.__name__: model for model in TABLE_MODELS}
TABLE_MODEL_BY_TABLENAME = {model.__tablename__: model for model in TABLE_MODELS}
__all__ = [model.__name__ for model in TABLE_MODELS] + [
    "TABLE_MODELS", "TABLE_MODEL_BY_NAME", "TABLE_MODEL_BY_TABLENAME",
]
