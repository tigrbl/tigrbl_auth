"""Identity-provider configuration contract objects."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True, slots=True)
class IdentityProvider:
    provider_id: str
    tenant_id: str
    kind: str
    issuer: str
    discovery_url: str
    audience: str
    logout_supported: bool
    display_name: str
    claim_mapping: Mapping[str, str]
    scopes: tuple[str, ...]
    key_set_version: int = 1
    enabled: bool = True


__all__ = ["IdentityProvider"]
