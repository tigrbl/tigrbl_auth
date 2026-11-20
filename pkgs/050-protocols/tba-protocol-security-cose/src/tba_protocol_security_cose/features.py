FEATURES = frozenset(
    {
        "sign",
        "sign1",
        "encrypt",
        "encrypt0",
        "mac",
        "mac0",
    }
)


def supports(feature: str) -> bool:
    return feature in FEATURES
