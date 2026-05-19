"""Schemas for key and JWKS operator methods."""

from __future__ import annotations

from typing import Any

from .common import EmptyParams
from pydantic import Field
from tigrbl_auth.api.rpc.registry import RpcSchema


class KeyRecord(RpcSchema):
    id: str
    kind: str
    kid: str | None = None
    label: str | None = None
    service_id: str | None = None
    digest: str | None = None
    created_at: str | None = None
    valid_from: str | None = None
    valid_to: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class KeysListParams(EmptyParams):
    tenant: str | None = None
    tenant_id: str | None = None


class KeysListResult(RpcSchema):
    key_count: int
    rotation_event_count: int
    keys: list[KeyRecord] = Field(default_factory=list)
    rotation_events: list[dict[str, Any]] = Field(default_factory=list)


class JwksShowParams(EmptyParams):
    pass


class JwksShowResult(RpcSchema):
    jwks: dict[str, Any] = Field(default_factory=dict)


class KeysRotateParams(RpcSchema):
    reason: str = "operator_rotation"


class KeysRotateResult(RpcSchema):
    status: str = "rotated"
    new_kid: str
    rotation_event: dict[str, Any] | None = None


class TenantKeySeedParams(RpcSchema):
    tenant: str
    tenant_id: str | None = None
    kid: str | None = None
    force: bool = False
    label: str | None = None
    status: str = "active"
    alg: str = "EdDSA"
    kty: str = "OKP"
    use: str = "sig"
    crv: str = "Ed25519"
    x: str | None = None


class TenantKeyCreateParams(RpcSchema):
    tenant: str
    tenant_id: str | None = None
    kid: str
    label: str | None = None
    status: str = "active"
    alg: str = "EdDSA"
    kty: str = "OKP"
    use: str = "sig"
    crv: str = "Ed25519"
    x: str | None = None
    n: str | None = None
    e: str | None = None
    publish: bool = True


class TenantKeyUpdateParams(RpcSchema):
    tenant: str
    tenant_id: str | None = None
    kid: str
    label: str | None = None
    status: str | None = None
    alg: str | None = None
    kty: str | None = None
    use: str | None = None
    crv: str | None = None
    x: str | None = None
    n: str | None = None
    e: str | None = None
    publish: bool | None = None


class TenantKeyDeleteParams(RpcSchema):
    tenant: str
    tenant_id: str | None = None
    kid: str


class TenantKeyMutationResult(RpcSchema):
    status: str
    key: KeyRecord | None = None
    jwks: dict[str, Any] = Field(default_factory=dict)


__all__ = [
    "JwksShowParams",
    "JwksShowResult",
    "KeyRecord",
    "TenantKeyCreateParams",
    "TenantKeyDeleteParams",
    "TenantKeyMutationResult",
    "TenantKeySeedParams",
    "TenantKeyUpdateParams",
    "KeysListParams",
    "KeysListResult",
    "KeysRotateParams",
    "KeysRotateResult",
]
