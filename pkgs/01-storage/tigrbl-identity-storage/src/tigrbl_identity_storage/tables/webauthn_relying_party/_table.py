"""Tenant-scoped WebAuthn relying-party configuration."""

from tigrbl_identity_storage.framework import Boolean, GUIDPk, JSON, Mapped, RestOltpTable, S, String, Timestamped, acol


class WebAuthnRelyingParty(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "webauthn_relying_parties"
    __table_args__ = {"extend_existing": True, "schema": "authn"}

    rp_config_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    tenant_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    rp_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    display_name: Mapped[str] = acol(storage=S(String(255), nullable=False))
    allowed_origins: Mapped[list] = acol(storage=S(JSON, nullable=False, default=list))
    allowed_algorithms: Mapped[list] = acol(storage=S(JSON, nullable=False, default=list))
    user_verification_policy: Mapped[str] = acol(storage=S(String(32), nullable=False, default="preferred"))
    resident_key_policy: Mapped[str] = acol(storage=S(String(32), nullable=False, default="preferred"))
    attestation_policy: Mapped[str] = acol(storage=S(String(32), nullable=False, default="none"))
    allowed_attestation_formats: Mapped[list | None] = acol(storage=S(JSON, nullable=True))
    related_origins: Mapped[list | None] = acol(storage=S(JSON, nullable=True))
    enabled: Mapped[bool] = acol(storage=S(Boolean, nullable=False, default=True, index=True))


__all__ = ["WebAuthnRelyingParty"]
