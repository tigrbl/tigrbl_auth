"""Durable control-plane correctness report artifacts."""

from __future__ import annotations


from tigrbl_identity_core.orm import RestOltpTable, Boolean, GUIDPk, JSON, Mapped, S, String, Timestamped, acol



class ControlCorrectnessReport(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "control_correctness_reports"
    __table_args__ = ({"schema": "authn"},)

    report_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    release_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    passed: Mapped[bool] = acol(storage=S(Boolean, nullable=False, default=False, index=True))
    report_payload: Mapped[dict] = acol(storage=S(JSON, nullable=False, default=dict))


__all__ = ["ControlCorrectnessReport"]
