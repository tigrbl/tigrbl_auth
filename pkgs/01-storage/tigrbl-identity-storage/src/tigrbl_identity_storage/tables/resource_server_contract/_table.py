"""Durable resource-server contract and attestation registry."""

from __future__ import annotations


from tigrbl_identity_storage.framework import RestOltpTable, GUIDPk, JSON, Mapped, S, String, Timestamped, acol



class ResourceServerContract(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "resource_server_contracts"
    __table_args__ = ({"schema": "authn"},)

    contract_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    resource_server_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    contract_kind: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    status: Mapped[str] = acol(storage=S(String(64), nullable=False, default="active", index=True))
    contract_payload: Mapped[dict] = acol(storage=S(JSON, nullable=False, default=dict))


__all__ = ["ResourceServerContract"]
