"""Provider registry for storage-backed crypto key execution."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any


class CryptoProviderRegistry:
    """Small runtime registry from durable provider names to provider instances."""

    def __init__(self, providers: Mapping[str, Any] | None = None) -> None:
        self._providers: dict[str, Any] = dict(providers or {})

    def register(self, name: str, provider: Any) -> None:
        cleaned = str(name).strip()
        if not cleaned:
            raise ValueError("provider name is required")
        self._providers[cleaned] = provider

    def get(self, name: str | None) -> Any:
        if name is None:
            if len(self._providers) == 1:
                return next(iter(self._providers.values()))
            raise LookupError("provider name is required")
        try:
            return self._providers[str(name)]
        except KeyError as exc:
            raise LookupError(f"crypto provider not registered: {name}") from exc


def resolve_provider(
    name: str | None,
    *,
    registry: CryptoProviderRegistry | Mapping[str, Any] | None = None,
    ctx: Mapping[str, Any] | None = None,
) -> Any:
    if isinstance(registry, CryptoProviderRegistry):
        return registry.get(name)
    if registry is not None:
        return CryptoProviderRegistry(registry).get(name)
    if ctx is not None:
        providers = ctx.get("crypto_providers")
        if isinstance(providers, Mapping):
            return CryptoProviderRegistry(providers).get(name)
        provider = ctx.get("crypto_provider")
        if provider is not None and (name is None or str(ctx.get("crypto_provider_name") or name) == str(name)):
            return provider
    raise LookupError("crypto provider registry not available")


__all__ = ["CryptoProviderRegistry", "resolve_provider"]
