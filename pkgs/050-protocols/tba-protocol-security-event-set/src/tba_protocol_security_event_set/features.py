FEATURES_BY_VERSION = {
    "draft-ietf-secevent-token-13": frozenset({"events", "subject", "transaction-id"}),
    "RFC8417": frozenset(
        {
            "events",
            "subject",
            "transaction-id",
            "explicit-typing",
            "multiple-audiences",
            "non-token-use",
        }
    ),
}


def supports(feature: str, version: str = "RFC8417") -> bool:
    try:
        return feature in FEATURES_BY_VERSION[version]
    except KeyError as exc:
        raise ValueError(f"unsupported SET version: {version}") from exc


__all__ = ["FEATURES_BY_VERSION", "supports"]
