from .versions import CURRENT_VERSION

FEATURES_BY_VERSION = {
    CURRENT_VERSION.identifier: frozenset(
        {
            "bearer-token",
            "jwt-access-token",
            "opaque-token-introspection",
            "issuer-audience-time-validation",
            "scope-enforcement",
            "policy-evaluation",
            "dpop-sender-constraint",
            "mtls-sender-constraint",
            "protected-resource-metadata",
            "fail-closed",
        }
    )
}


def supports(feature: str, version: str = CURRENT_VERSION.identifier) -> bool:
    try:
        return feature in FEATURES_BY_VERSION[version]
    except KeyError as exc:
        raise ValueError(f"unsupported protected-resource profile: {version}") from exc


__all__ = ["FEATURES_BY_VERSION", "supports"]
