"""Table-owned operator transaction log."""

from __future__ import annotations

from tigrbl_identity_storage.framework import RestOltpTable, Mapped, S, String, acol


class OperatorTransaction(RestOltpTable):
    __tablename__ = "operator_transactions"

    transaction_id: Mapped[str] = acol(
        storage=S(String(255), primary_key=True, nullable=False)
    )
    ts: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    command: Mapped[str] = acol(storage=S(String(255), nullable=False))
    resource: Mapped[str] = acol(storage=S(String(128), nullable=False, index=True))
    status: Mapped[str] = acol(storage=S(String(64), nullable=False))
    record_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True))
    changed_ids_json: Mapped[str] = acol(
        storage=S(String(8000), nullable=False, default="[]")
    )
    summary_json: Mapped[str] = acol(
        storage=S(String(20000), nullable=False, default="{}")
    )
    actor: Mapped[str | None] = acol(storage=S(String(255), nullable=True))
    profile: Mapped[str | None] = acol(storage=S(String(255), nullable=True))
    tenant: Mapped[str | None] = acol(storage=S(String(255), nullable=True))
    issuer: Mapped[str | None] = acol(storage=S(String(512), nullable=True))
    before_checksum: Mapped[str | None] = acol(storage=S(String(128), nullable=True))
    after_checksum: Mapped[str | None] = acol(storage=S(String(128), nullable=True))


__all__ = ["OperatorTransaction"]
