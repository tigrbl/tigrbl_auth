"""Durable workload references, credential entitlements, artifact locators, and proof replay."""
from __future__ import annotations
import datetime as dt
from tigrbl_identity_storage.framework import Boolean, GUIDPk, JSON, Mapped, RestOltpTable, S, String, TZDateTime, Timestamped, acol

class WorkloadReferenceBinding(RestOltpTable, GUIDPk, Timestamped):
    __tablename__="workload_reference_bindings"; __table_args__=({"schema":"authn"},)
    reference_id: Mapped[str]=acol(storage=S(String(255),nullable=False,unique=True,index=True))
    tenant_id: Mapped[str]=acol(storage=S(String(255),nullable=False,index=True))
    reference_kind: Mapped[str]=acol(storage=S(String(64),nullable=False,index=True))
    reference_digest: Mapped[str]=acol(storage=S(String(128),nullable=False,index=True))
    reference_scope: Mapped[str]=acol(storage=S(String(1000),nullable=False,index=True))
    canonical_locator: Mapped[str|None]=acol(storage=S(String(2000),nullable=True))
    resolved_workload_id: Mapped[str|None]=acol(storage=S(String(1000),nullable=True,index=True))
    lifecycle_version: Mapped[str|None]=acol(storage=S(String(255),nullable=True))
    active: Mapped[bool]=acol(storage=S(Boolean,nullable=False,default=True,index=True))
    valid_from: Mapped[dt.datetime|None]=acol(storage=S(TZDateTime,nullable=True,index=True))
    valid_until: Mapped[dt.datetime|None]=acol(storage=S(TZDateTime,nullable=True,index=True))
    last_resolved_at: Mapped[dt.datetime|None]=acol(storage=S(TZDateTime,nullable=True,index=True))

class WorkloadCredentialEntitlement(RestOltpTable, GUIDPk, Timestamped):
    __tablename__="workload_credential_entitlements"; __table_args__=({"schema":"authn"},)
    entitlement_id: Mapped[str]=acol(storage=S(String(255),nullable=False,unique=True,index=True))
    tenant_id: Mapped[str]=acol(storage=S(String(255),nullable=False,index=True))
    actor_principal_id: Mapped[str]=acol(storage=S(String(255),nullable=False,index=True))
    workload_reference_id: Mapped[str]=acol(storage=S(String(255),nullable=False,index=True))
    credential_format: Mapped[str]=acol(storage=S(String(64),nullable=False,index=True))
    identity_constraint: Mapped[str|None]=acol(storage=S(String(1000),nullable=True,index=True))
    audience_constraint: Mapped[dict|None]=acol(storage=S(JSON,nullable=True))
    trust_domain_constraint: Mapped[str|None]=acol(storage=S(String(255),nullable=True,index=True))
    policy_reference: Mapped[str|None]=acol(storage=S(String(1000),nullable=True))
    enabled: Mapped[bool]=acol(storage=S(Boolean,nullable=False,default=True,index=True))
    valid_from: Mapped[dt.datetime|None]=acol(storage=S(TZDateTime,nullable=True,index=True))
    valid_until: Mapped[dt.datetime|None]=acol(storage=S(TZDateTime,nullable=True,index=True))

class ProtectedArtifactReference(RestOltpTable, GUIDPk, Timestamped):
    __tablename__="protected_artifact_references"; __table_args__=({"schema":"authn"},)
    artifact_id: Mapped[str]=acol(storage=S(String(255),nullable=False,unique=True,index=True))
    artifact_kind: Mapped[str]=acol(storage=S(String(64),nullable=False,index=True))
    artifact_format: Mapped[str]=acol(storage=S(String(128),nullable=False,index=True))
    profile: Mapped[str|None]=acol(storage=S(String(255),nullable=True,index=True))
    immutable_locator: Mapped[str]=acol(storage=S(String(2000),nullable=False))
    artifact_digest: Mapped[str]=acol(storage=S(String(128),nullable=False,index=True))
    media_type: Mapped[str|None]=acol(storage=S(String(255),nullable=True))
    valid_until: Mapped[dt.datetime|None]=acol(storage=S(TZDateTime,nullable=True,index=True))

class PossessionProofReplay(RestOltpTable, GUIDPk, Timestamped):
    __tablename__="possession_proof_replays"; __table_args__=({"schema":"authn"},)
    replay_key: Mapped[str]=acol(storage=S(String(128),nullable=False,unique=True,index=True))
    profile: Mapped[str]=acol(storage=S(String(128),nullable=False,index=True))
    proof_id: Mapped[str]=acol(storage=S(String(255),nullable=False,index=True))
    credential_digest: Mapped[str|None]=acol(storage=S(String(128),nullable=True,index=True))
    audience_digest: Mapped[str|None]=acol(storage=S(String(128),nullable=True,index=True))
    first_seen_at: Mapped[dt.datetime]=acol(storage=S(TZDateTime,nullable=False,index=True))
    expires_at: Mapped[dt.datetime]=acol(storage=S(TZDateTime,nullable=False,index=True))

__all__=["PossessionProofReplay","ProtectedArtifactReference","WorkloadCredentialEntitlement","WorkloadReferenceBinding"]