"""Storage-runtime federation repository composition."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

from tigrbl_identity_contracts.federation import (
    FederatedSession as FederatedSessionContract,
    IdentityProvider as IdentityProviderContract,
)
from tigrbl_identity_core.clock import utc_now_iso
from tigrbl_identity_storage.tables import FederatedSession, IdentityProvider


def _items(result: Any) -> tuple[Any, ...]:
    if isinstance(result, Mapping) and isinstance(result.get("items"), list):
        result = result["items"]
    elif hasattr(result, "items") and isinstance(getattr(result, "items"), list):
        result = result.items
    if isinstance(result, tuple):
        return result
    if isinstance(result, list):
        return tuple(result)
    if result is None:
        return ()
    return (result,)


def _row_value(row: Any, key: str, default: Any = None) -> Any:
    if isinstance(row, Mapping):
        return row.get(key, default)
    return getattr(row, key, default)


def _list_payload(values: Iterable[str]) -> dict[str, list[str]]:
    return {"items": sorted({str(value).strip() for value in values if str(value).strip()})}


def _list_from_payload(value: Any) -> tuple[str, ...]:
    if isinstance(value, Mapping):
        value = value.get("items", ())
    return tuple(str(item) for item in (value or ()))


def _provider_contract(row: Any) -> IdentityProviderContract:
    return IdentityProviderContract(
        provider_id=str(_row_value(row, "provider_id")),
        tenant_id=str(_row_value(row, "tenant_id")),
        kind=str(_row_value(row, "kind")),
        issuer=str(_row_value(row, "issuer")),
        discovery_url=str(_row_value(row, "discovery_url")),
        audience=str(_row_value(row, "audience")),
        logout_supported=bool(_row_value(row, "logout_supported", False)),
        display_name=str(_row_value(row, "display_name")),
        claim_mapping=dict(_row_value(row, "claim_mapping", {}) or {}),
        scopes=_list_from_payload(_row_value(row, "scopes", {})),
        key_set_version=int(_row_value(row, "key_set_version", 1) or 1),
        enabled=bool(_row_value(row, "enabled", True)),
    )


def _session_contract(row: Any) -> FederatedSessionContract:
    return FederatedSessionContract(
        session_id=str(_row_value(row, "session_id")),
        provider_id=str(_row_value(row, "provider_id")),
        tenant_id=str(_row_value(row, "tenant_id")),
        issuer=str(_row_value(row, "issuer")),
        audience=str(_row_value(row, "audience")),
        logout_supported=bool(_row_value(row, "logout_supported", False)),
        normalized_claims=dict(_row_value(row, "normalized_claims", {}) or {}),
        bound_at=str(_row_value(row, "bound_at")),
    )


class StorageFederationRepository:
    """Federation registry behavior backed by identity storage table handlers."""

    def __init__(self, db: Any) -> None:
        self.db = db

    async def providers(self) -> Mapping[str, IdentityProviderContract]:
        rows = _items(await IdentityProvider.handlers.list.core({"payload": {}, "db": self.db}))
        return {provider.provider_id: provider for provider in (_provider_contract(row) for row in rows)}

    async def register_provider(
        self,
        *,
        provider_id: str,
        tenant_id: str,
        kind: str,
        issuer: str,
        discovery_url: str,
        audience: str,
        display_name: str,
        logout_supported: bool = False,
        claim_mapping: Mapping[str, str] | None = None,
        scopes: Iterable[str] = (),
    ) -> IdentityProviderContract:
        if kind not in {"social", "sso", "federation"}:
            raise ValueError(f"unsupported provider kind {kind!r}")
        row = await IdentityProvider.handlers.create.core(
            {
                "payload": {
                    "provider_id": provider_id,
                    "tenant_id": tenant_id,
                    "kind": kind,
                    "issuer": issuer,
                    "discovery_url": discovery_url,
                    "audience": audience,
                    "logout_supported": logout_supported,
                    "display_name": display_name,
                    "claim_mapping": dict(claim_mapping or {"sub": "sub", "email": "email", "name": "name"}),
                    "scopes": _list_payload(scopes),
                    "key_set_version": 1,
                    "enabled": True,
                },
                "db": self.db,
            }
        )
        return _provider_contract(row)

    async def rotate_provider_keys(self, provider_id: str) -> IdentityProviderContract:
        provider = (await self.providers())[provider_id]
        rows = _items(
            await IdentityProvider.handlers.list.core(
                {"payload": {"filters": {"provider_id": provider_id}}, "db": self.db}
            )
        )
        row = rows[0]
        updated = await IdentityProvider.handlers.update.core(
            {
                "path_params": {"id": _row_value(row, "id")},
                "payload": {"key_set_version": provider.key_set_version + 1},
                "db": self.db,
            }
        )
        return _provider_contract(updated)

    async def normalize_claims(self, provider_id: str, claims: Mapping[str, Any]) -> dict[str, Any]:
        provider = (await self.providers())[provider_id]
        normalized: dict[str, Any] = {"iss": provider.issuer}
        for target, source in provider.claim_mapping.items():
            normalized[target] = claims.get(source)
        if normalized.get("name") in {None, ""}:
            normalized["name"] = normalized.get("email") or normalized.get("sub")
        return normalized

    async def bind_session(
        self,
        *,
        provider_id: str,
        tenant_id: str,
        session_id: str,
        issuer: str,
        audience: str,
        claims: Mapping[str, Any],
    ) -> FederatedSessionContract:
        provider = (await self.providers())[provider_id]
        if not provider.enabled:
            raise PermissionError("identity provider is disabled")
        if provider.tenant_id != tenant_id:
            raise PermissionError("identity provider tenant mismatch")
        if provider.issuer != issuer:
            raise PermissionError("identity provider issuer mismatch")
        if provider.audience != audience:
            raise PermissionError("identity provider audience mismatch")
        row = await FederatedSession.handlers.create.core(
            {
                "payload": {
                    "session_id": session_id,
                    "provider_id": provider_id,
                    "tenant_id": tenant_id,
                    "issuer": issuer,
                    "audience": audience,
                    "logout_supported": provider.logout_supported,
                    "normalized_claims": await self.normalize_claims(provider_id, claims),
                    "bound_at": utc_now_iso(),
                },
                "db": self.db,
            }
        )
        return _session_contract(row)


def create_storage_federation_repository(db: Any) -> StorageFederationRepository:
    return StorageFederationRepository(db)


__all__ = ["StorageFederationRepository", "create_storage_federation_repository"]
