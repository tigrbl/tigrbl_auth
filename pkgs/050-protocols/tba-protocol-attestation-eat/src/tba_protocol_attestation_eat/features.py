FEATURES_BY_VERSION = {
    "draft-ietf-rats-eat-30": frozenset(
        {"jwt", "cwt", "eat-profile", "nonce", "submodules"}
    ),
    "RFC9711": frozenset(
        {
            "jwt",
            "cwt",
            "eat-profile",
            "nonce",
            "submodules",
            "detached-bundles",
            "nested-tokens",
        }
    ),
}


def supports(feature: str, version: str = "RFC9711") -> bool:
    try:
        return feature in FEATURES_BY_VERSION[version]
    except KeyError as exc:
        raise ValueError(f"unsupported EAT version: {version}") from exc


__all__ = ["FEATURES_BY_VERSION", "supports"]
