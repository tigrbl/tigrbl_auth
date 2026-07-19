FEATURES = frozenset({
    "compact",
    "json-general",
    "json-flattened",
    "authenticated-encryption",
    "nested-jwt",
})

def supports(feature: str) -> bool:
    return feature in FEATURES
