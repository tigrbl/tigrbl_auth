FEATURES = frozenset(
    {
        "compact",
        "json-general",
        "json-flattened",
        "detached-payload",
        "unencoded-payload",
    }
)


def supports(feature: str) -> bool:
    return feature in FEATURES
