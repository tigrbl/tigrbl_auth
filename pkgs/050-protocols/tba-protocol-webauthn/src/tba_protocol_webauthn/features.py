from .versions import WebAuthnVersion


class WebAuthnFeature:
    """Feature-name constants used by versioned protocol configuration."""

    REGISTRATION = "registration"
    AUTHENTICATION = "authentication"
    DISCOVERABLE_CREDENTIALS = "discoverable-credentials"
    USER_VERIFICATION = "user-verification"
    ATTESTATION = "attestation"
    BACKUP_STATE = "backup-state"
    JSON_SERIALIZATION = "json-serialization"
    CONDITIONAL_MEDIATION = "conditional-mediation"
    RELATED_ORIGINS = "related-origins"


BASE_FEATURES = frozenset(
    {
        WebAuthnFeature.REGISTRATION,
        WebAuthnFeature.AUTHENTICATION,
        WebAuthnFeature.DISCOVERABLE_CREDENTIALS,
        WebAuthnFeature.USER_VERIFICATION,
        WebAuthnFeature.ATTESTATION,
        WebAuthnFeature.BACKUP_STATE,
    }
)
LEVEL_3_FEATURES = BASE_FEATURES | {
    WebAuthnFeature.JSON_SERIALIZATION,
    WebAuthnFeature.CONDITIONAL_MEDIATION,
    WebAuthnFeature.RELATED_ORIGINS,
}


def features_for(version: str) -> frozenset[str]:
    if version not in {WebAuthnVersion.LEVEL_2, WebAuthnVersion.LEVEL_3}:
        raise ValueError(f"unsupported WebAuthn version: {version}")
    return LEVEL_3_FEATURES if version == WebAuthnVersion.LEVEL_3 else BASE_FEATURES


__all__ = ["BASE_FEATURES", "LEVEL_3_FEATURES", "WebAuthnFeature", "features_for"]
