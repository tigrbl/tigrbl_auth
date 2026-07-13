FEATURES_BY_VERSION = {
    "draft-ietf-oauth-json-web-token-32": frozenset(
        {"registered-claims", "public-claims", "private-claims"}
    ),
    "RFC7519": frozenset(
        {
            "registered-claims",
            "public-claims",
            "private-claims",
            "nested-jwt",
            "string-or-array-audience",
        }
    ),
}


def supports(feature: str, version: str = "RFC7519") -> bool:
    try:
        return feature in FEATURES_BY_VERSION[version]
    except KeyError as exc:
        raise ValueError(f"unsupported JWT version: {version}") from exc


__all__ = ["FEATURES_BY_VERSION", "supports"]
