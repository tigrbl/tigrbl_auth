from __future__ import annotations

from dataclasses import replace
from typing import Any, Iterable, Mapping

from tigrbl_identity_contracts.federation import FederatedSession, IdentityProvider
from tigrbl_identity_core.clock import utc_now_iso


class FederationRegistry:
    def __init__(self) -> None:
        self._providers: dict[str, IdentityProvider] = {}
        self._sessions: dict[str, FederatedSession] = {}

    @property
    def providers(self) -> Mapping[str, IdentityProvider]:
        return dict(self._providers)

    def register_provider(
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
    ) -> IdentityProvider:
        if kind not in {"social", "sso", "federation"}:
            raise ValueError(f"unsupported provider kind {kind!r}")
        provider = IdentityProvider(
            provider_id=provider_id,
            tenant_id=tenant_id,
            kind=kind,
            issuer=issuer,
            discovery_url=discovery_url,
            audience=audience,
            logout_supported=logout_supported,
            display_name=display_name,
            claim_mapping=dict(claim_mapping or {"sub": "sub", "email": "email", "name": "name"}),
            scopes=tuple(sorted(set(scopes))),
        )
        self._providers[provider_id] = provider
        return provider

    def rotate_provider_keys(self, provider_id: str) -> IdentityProvider:
        provider = self._providers[provider_id]
        updated = replace(provider, key_set_version=provider.key_set_version + 1)
        self._providers[provider_id] = updated
        return updated

    def normalize_claims(self, provider_id: str, claims: Mapping[str, Any]) -> dict[str, Any]:
        provider = self._providers[provider_id]
        normalized: dict[str, Any] = {"iss": provider.issuer}
        for target, source in provider.claim_mapping.items():
            normalized[target] = claims.get(source)
        if normalized.get("name") in {None, ""}:
            normalized["name"] = normalized.get("email") or normalized.get("sub")
        return normalized

    def bind_session(
        self,
        *,
        provider_id: str,
        tenant_id: str,
        session_id: str,
        issuer: str,
        audience: str,
        claims: Mapping[str, Any],
    ) -> FederatedSession:
        provider = self._providers[provider_id]
        if not provider.enabled:
            raise PermissionError("identity provider is disabled")
        if provider.tenant_id != tenant_id:
            raise PermissionError("identity provider tenant mismatch")
        if provider.issuer != issuer:
            raise PermissionError("identity provider issuer mismatch")
        if provider.audience != audience:
            raise PermissionError("identity provider audience mismatch")
        session = FederatedSession(
            session_id=session_id,
            provider_id=provider_id,
            tenant_id=tenant_id,
            issuer=issuer,
            audience=audience,
            logout_supported=provider.logout_supported,
            normalized_claims=self.normalize_claims(provider_id, claims),
            bound_at=utc_now_iso(),
        )
        self._sessions[session_id] = session
        return session

    def summary(self) -> dict[str, Any]:
        return {
            "provider_count": len(self._providers),
            "active_provider_count": sum(provider.enabled for provider in self._providers.values()),
            "kinds": sorted({provider.kind for provider in self._providers.values()}),
            "session_count": len(self._sessions),
        }


__all__ = ["FederationRegistry"]
