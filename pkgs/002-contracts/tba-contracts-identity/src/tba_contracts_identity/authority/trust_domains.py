from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TenantTrustDomainAuthority:
    tenant_slug: str
    issuer: str
    jwks_uri: str
    jwks_path: str
    subject_namespace: str
    protected_resource_identifier: str
    signing_scope: str
    accepted_issuers: tuple[str, ...]
    verification_scope: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class RealmTrustDomainAuthority:
    realm_slug: str
    issuer: str
    jwks_uri: str
    jwks_path: str
    subject_namespace: str
    protected_resource_identifier: str
    signing_scope: str
    accepted_issuers: tuple[str, ...]
    verification_scope: tuple[str, ...]


__all__ = ["RealmTrustDomainAuthority", "TenantTrustDomainAuthority"]
