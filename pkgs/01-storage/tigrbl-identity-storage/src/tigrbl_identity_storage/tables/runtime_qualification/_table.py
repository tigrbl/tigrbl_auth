"""Durable runtime qualification evidence."""

from __future__ import annotations


from tigrbl_identity_storage.framework import RestOltpTable, GUIDPk, JSON, Mapped, S, String, Timestamped, acol



class RuntimeQualificationRecord(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "runtime_qualifications"
    __table_args__ = ({"schema": "authn"},)

    qualification_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    release_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    runtime_name: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    status: Mapped[str] = acol(storage=S(String(64), nullable=False, default="qualified", index=True))
    qualification_payload: Mapped[dict] = acol(storage=S(JSON, nullable=False, default=dict))


__all__ = ["RuntimeQualificationRecord"]
