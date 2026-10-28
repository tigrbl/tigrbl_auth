FEATURES_BY_VERSION = {
    "draft-ietf-rats-corim-10": frozenset({"corim", "comid", "coswid"}),
    "draft-ietf-rats-corim-11": frozenset(
        {"corim", "comid", "coswid", "cotl", "cots", "reference-values", "endorsements"}
    ),
}


def supports(version: str, feature: str) -> bool:
    try:
        return feature in FEATURES_BY_VERSION[version]
    except KeyError as exc:
        raise ValueError(f"unsupported CoRIM version: {version}") from exc


__all__ = ["FEATURES_BY_VERSION", "supports"]
