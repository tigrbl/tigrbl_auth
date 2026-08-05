# ruff: noqa: F401
"""Durable workload references, credential entitlements, artifact locators, and proof replay."""
from __future__ import annotations
import datetime as dt
from tigrbl_identity_core.orm import Boolean, GUIDPk, JSON, Mapped, RestOltpTable, S, String, TZDateTime, Timestamped, acol

class ProtectedArtifactReference(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = 'protected_artifact_references'
    __table_args__ = ({'schema': 'authn'},)
    artifact_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    artifact_kind: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    artifact_format: Mapped[str] = acol(storage=S(String(128), nullable=False, index=True))
    profile: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    immutable_locator: Mapped[str] = acol(storage=S(String(2000), nullable=False))
    artifact_digest: Mapped[str] = acol(storage=S(String(128), nullable=False, index=True))
    media_type: Mapped[str | None] = acol(storage=S(String(255), nullable=True))
    valid_until: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))

class PossessionProofReplay(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = 'possession_proof_replays'
    __table_args__ = ({'schema': 'authn'},)
    replay_key: Mapped[str] = acol(storage=S(String(128), nullable=False, unique=True, index=True))
    profile: Mapped[str] = acol(storage=S(String(128), nullable=False, index=True))
    proof_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    credential_digest: Mapped[str | None] = acol(storage=S(String(128), nullable=True, index=True))
    audience_digest: Mapped[str | None] = acol(storage=S(String(128), nullable=True, index=True))
    first_seen_at: Mapped[dt.datetime] = acol(storage=S(TZDateTime, nullable=False, index=True))
    expires_at: Mapped[dt.datetime] = acol(storage=S(TZDateTime, nullable=False, index=True))
