FEATURES_BY_VERSION = {
    "draft-20": frozenset({"presentation-definition", "direct-post", "request-uri"}),
    "draft-25": frozenset(
        {"dcql", "direct-post", "direct-post-jwt", "request-uri", "transaction-data"}
    ),
    "1.0": frozenset(
        {
            "dcql",
            "direct-post",
            "direct-post-jwt",
            "request-uri",
            "transaction-data",
            "digital-credentials-api",
            "same-device",
            "cross-device",
        }
    ),
}


def supports(feature: str, version: str = "1.0") -> bool:
    try:
        return feature in FEATURES_BY_VERSION[version]
    except KeyError as exc:
        raise ValueError(f"unsupported OID4VP version: {version}") from exc


__all__ = ["FEATURES_BY_VERSION", "supports"]
