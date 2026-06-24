"""Table-owned operator audit log."""

from __future__ import annotations

from tigrbl_identity_storage.framework import RestOltpTable, Mapped, S, String, acol


class OperatorAuditEvent(RestOltpTable):
    __tablename__ = "operator_audit_events"

    id: Mapped[str] = acol(storage=S(String(255), primary_key=True, nullable=False))
    tenant_id: Mapped[str | None] = acol(
        storage=S(String(255), nullable=True, index=True)
    )
    actor_user_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True))
    actor_client_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True))
    session_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True))
    event_type: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    target_type: Mapped[str] = acol(storage=S(String(128), nullable=False))
    target_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True))
    outcome: Mapped[str] = acol(storage=S(String(64), nullable=False))
    request_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True))
    occurred_at: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    details_json: Mapped[str] = acol(
        storage=S(String(20000), nullable=False, default="{}")
    )


__all__ = ["OperatorAuditEvent"]
