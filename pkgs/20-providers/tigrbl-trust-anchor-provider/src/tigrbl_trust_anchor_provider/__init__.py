from tigrbl_security_trust_contracts import TrustAnchor, TrustAnchorProviderPort


class ProfiledTrustAnchorProvider(TrustAnchorProviderPort):
    def __init__(self):
        self._anchors: dict[str, TrustAnchor] = {}

    def publish(self, anchor: TrustAnchor) -> None:
        if anchor.identifier in self._anchors:
            raise ValueError(f"duplicate trust anchor: {anchor.identifier}")
        if not anchor.certificate_der or not anchor.profiles:
            raise ValueError("trust anchor requires certificate material and profiles")
        self._anchors[anchor.identifier] = anchor

    def remove(self, identifier: str) -> None:
        try:
            del self._anchors[identifier]
        except KeyError as exc:
            raise LookupError(identifier) from exc

    def anchors_for(self, profile: str, /) -> tuple[TrustAnchor, ...]:
        return tuple(
            anchor for anchor in self._anchors.values() if profile in anchor.profiles
        )


__all__ = ["ProfiledTrustAnchorProvider"]
