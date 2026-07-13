from collections.abc import Callable, Mapping

from tigrbl_identity_contracts.attestation import AttestationEvidence

PlatformEvidenceAdapter = Callable[[bytes | str, str], Mapping[str | int, object]]


class PlatformAttestationProvider:
    def __init__(self):
        self._adapters: dict[str, PlatformEvidenceAdapter] = {}

    def register(self, platform: str, adapter: PlatformEvidenceAdapter) -> None:
        if not platform or platform in self._adapters:
            raise ValueError("platform adapter must be non-empty and unique")
        self._adapters[platform] = adapter

    def collect(
        self, platform: str, artifact: bytes | str, profile: str
    ) -> AttestationEvidence:
        adapter = self._adapters.get(platform)
        if adapter is None:
            raise LookupError(platform)
        claims = adapter(artifact, profile)
        if not isinstance(claims, Mapping) or not claims:
            raise ValueError("platform adapter returned no evidence claims")
        reported_profile = claims.get("eat_profile", claims.get(265))
        if str(reported_profile) != profile:
            raise ValueError("platform evidence profile mismatch")
        normalized = dict(claims)
        normalized["platform"] = platform
        return AttestationEvidence(profile, normalized, artifact)


__all__ = ["PlatformAttestationProvider", "PlatformEvidenceAdapter"]
