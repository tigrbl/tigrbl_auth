"""Durable external subject aliases."""

from __future__ import annotations


from tigrbl_identity_storage.framework import RestOltpTable, GUIDPk, Mapped, S, String, Timestamped, acol



class SubjectAlias(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "subject_aliases"
    __table_args__ = ({"schema": "authn"},)

    principal_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    issuer: Mapped[str] = acol(storage=S(String(1000), nullable=False, index=True))
    subject: Mapped[str] = acol(storage=S(String(1000), nullable=False, index=True))
    tenant_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    verified: Mapped[str] = acol(storage=S(String(8), nullable=False, default="false", index=True))


__all__ = ["SubjectAlias"]
