FEATURES_BY_VERSION = {
    "draft-13": frozenset(
        {"access-token-request", "client-instance", "interaction", "continuation"}
    ),
    "draft-ietf-gnap-core-protocol-20": frozenset(
        {
            "access-token-request",
            "client-instance",
            "interaction",
            "continuation",
            "subject-information",
            "token-rotation",
        }
    ),
    "RFC9635": frozenset(
        {
            "access-token-request",
            "client-instance",
            "interaction",
            "continuation",
            "subject-information",
            "token-rotation",
            "key-proofing",
            "multiple-access-tokens",
        }
    ),
}


def supports(feature: str, version: str = "RFC9635") -> bool:
    try:
        return feature in FEATURES_BY_VERSION[version]
    except KeyError as exc:
        raise ValueError(f"unsupported GNAP version: {version}") from exc


__all__ = ["FEATURES_BY_VERSION", "supports"]
