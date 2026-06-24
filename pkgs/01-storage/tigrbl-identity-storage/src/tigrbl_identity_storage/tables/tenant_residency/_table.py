"""Durable tenant residency assignments."""

from __future__ import annotations


from tigrbl_identity_storage.framework import RestOltpTable, GUIDPk, JSON, Mapped, S, String, Timestamped, acol



class TenantResidency(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "tenant_residency"
    __table_args__ = ({"schema": "authn"},)

    tenant_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    residency_zone_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    allowed_processing_regions: Mapped[list] = acol(storage=S(JSON, nullable=False, default=list))
    restricted_transfer_regions: Mapped[list | None] = acol(storage=S(JSON, nullable=True))
    realm: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    residency_attributes: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="active", index=True))


__all__ = ["TenantResidency"]
