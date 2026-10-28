from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DelegatedCapability:
    action: str
    resource: str
    audience: str | None = None


__all__ = ["DelegatedCapability"]
