from dataclasses import dataclass

from .versions import WebAuthnVersion
from .features import features_for


@dataclass(frozen=True, slots=True)
class WebAuthnConfiguration:
    version: str = WebAuthnVersion.LEVEL_2
    allowed_algorithms: tuple[int, ...] = (-7, -257)
    user_verification: str = "preferred"
    resident_key: str = "preferred"
    attestation: str = "none"
    timeout_ms: int = 300_000
    enabled_features: frozenset[str] = frozenset()
    related_origins: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.allowed_algorithms:
            raise ValueError("at least one WebAuthn COSE algorithm is required")
        if self.timeout_ms <= 0:
            raise ValueError("WebAuthn timeout must be positive")
        unsupported = self.enabled_features.difference(features_for(self.version))
        if unsupported:
            raise ValueError(
                f"features are unavailable in {self.version}: {sorted(unsupported)}"
            )

    def feature_enabled(self, feature: str) -> bool:
        return feature in self.enabled_features


__all__ = ["WebAuthnConfiguration"]
