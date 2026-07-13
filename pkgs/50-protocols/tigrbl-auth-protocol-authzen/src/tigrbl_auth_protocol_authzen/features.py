FEATURES_BY_VERSION = {
    "draft-00": frozenset({"access-evaluation"}),
    "implementers-draft-1": frozenset({"access-evaluation"}),
    "1.0": frozenset(
        {
            "access-evaluation",
            "access-evaluations",
            "search-subject",
            "search-resource",
            "search-action",
            "configuration",
            "capabilities",
        }
    ),
}


def supports(feature: str, version: str = "1.0") -> bool:
    try:
        return feature in FEATURES_BY_VERSION[version]
    except KeyError as exc:
        raise ValueError(f"unsupported AuthZEN version: {version}") from exc


__all__ = ["FEATURES_BY_VERSION", "supports"]
