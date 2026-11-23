FEATURES = frozenset(
    {
        "did-syntax",
        "did-url",
        "verification-method",
        "verification-relationships",
        "services",
        "resolution-metadata",
        "document-metadata",
    }
)


def supports(feature: str) -> bool:
    return feature in FEATURES
