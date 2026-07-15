SERVER_FEATURES = frozenset(
    {
        "registration",
        "authentication",
        "discoverable-credentials",
        "user-verification",
        "backup-state",
        "attestation-policy",
        "metadata-status",
        "credential-management",
    }
)

__all__ = ["SERVER_FEATURES"]
