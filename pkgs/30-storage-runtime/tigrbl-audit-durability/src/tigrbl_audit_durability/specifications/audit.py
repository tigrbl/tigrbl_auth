"""Audit-event alias and executable runtime specification."""

from tigrbl_identity_storage.tables import AuditEvent

from tigrbl import deriveTableSpec
from tigrbl import makeOp
from tigrbl_audit_durability.operations.audit import (
    append_audit_event_record,
    list_audit_event_records,
)


AuditEventTable = AuditEvent
AuditEventRuntimeSpec = deriveTableSpec(
    AuditEventTable,
    ops=(
        makeOp(
            extra={"owner_layer": "30-storage-runtime"},
            expose_routes=False,
            expose_rpc=False,
            expose_method=True,
            tx_scope="read_write",
            alias="append",
            handler=append_audit_event_record,
        ),
        makeOp(
            extra={"owner_layer": "30-storage-runtime"},
            expose_routes=False,
            expose_rpc=False,
            expose_method=True,
            alias="list_events",
            handler=list_audit_event_records,
            tx_scope="read_only",
        ),
    ),
)


__all__ = ["AuditEventRuntimeSpec", "AuditEventTable"]
