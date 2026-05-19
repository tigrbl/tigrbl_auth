"""Audit lookup and export RPC methods."""

from __future__ import annotations

from tigrbl_auth.api.rpc.registry import RpcMethodDefinition
from tigrbl_auth.api.rpc.schemas.audit import (
    AuditExportParams,
    AuditExportResult,
    AuditListParams,
    AuditListResult,
)
from tigrbl_auth.api.rpc.methods._shared import export_records, list_rows, row_to_dict


async def handle_audit_list(params: AuditListParams, _context):
    from tigrbl_auth.tables import AuditEvent

    rows = await list_rows(
        AuditEvent,
        filters={"event_type": params.event_type, "outcome": params.outcome},
        limit=params.limit,
        offset=params.offset,
        order_by="occurred_at",
    )
    items = [row_to_dict(row) for row in rows]
    return AuditListResult(count=len(items), items=items)


async def handle_audit_export(params: AuditExportParams, _context):
    from tigrbl_auth.tables import AuditEvent

    rows = await list_rows(
        AuditEvent,
        filters={"event_type": params.event_type, "outcome": params.outcome},
        limit=params.limit,
        offset=params.offset,
        order_by="occurred_at",
    )
    items = [row_to_dict(row) for row in rows]
    return AuditExportResult(
        export_format=params.export_format,
        count=len(items),
        content=export_records(items, params.export_format),
        items=items,
    )


METHODS = (
    RpcMethodDefinition(
        name="audit.list",
        summary="List durable audit events.",
        description="Returns persisted audit events for operator search and review.",
        params_model=AuditListParams,
        result_model=AuditListResult,
        handler=handle_audit_list,
        owner_module="tigrbl_auth/api/rpc/methods/audit.py",
        tags=("audit", "operator"),
    ),
    RpcMethodDefinition(
        name="audit.export",
        summary="Export durable audit events.",
        description="Exports the filtered audit result set as JSON, NDJSON, or CSV content.",
        params_model=AuditExportParams,
        result_model=AuditExportResult,
        handler=handle_audit_export,
        owner_module="tigrbl_auth/api/rpc/methods/audit.py",
        tags=("audit", "operator"),
    ),
)
