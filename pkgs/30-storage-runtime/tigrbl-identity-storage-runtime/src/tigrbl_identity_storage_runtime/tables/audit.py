"""Audit-event alias and executable runtime specification."""

from tigrbl_identity_storage.tables import AuditEvent

from ..derive import deriveRuntimeTableSpec
from ..make import makeRuntimeOperation
from ..ops.audit import append_audit_event_record, list_audit_event_records


AuditEventTable = AuditEvent
AuditEventRuntimeSpec = deriveRuntimeTableSpec(
    AuditEventTable,
    operations=(
        makeRuntimeOperation(alias="append", handler=append_audit_event_record),
        makeRuntimeOperation(
            alias="list_events",
            handler=list_audit_event_records,
            tx_scope="read_only",
        ),
    ),
)


__all__ = ["AuditEventRuntimeSpec", "AuditEventTable"]
