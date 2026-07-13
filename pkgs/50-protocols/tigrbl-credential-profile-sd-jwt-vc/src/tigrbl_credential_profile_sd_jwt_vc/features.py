FEATURES_BY_VERSION = {
    "draft-10": frozenset({"vct", "status", "key-binding"}),
    "draft-13": frozenset({"vct", "status", "key-binding", "type-metadata"}),
    "draft-17": frozenset(
        {
            "vct",
            "status",
            "key-binding",
            "type-metadata",
            "vct-integrity",
            "dc-media-type",
        }
    ),
}


def supports(feature: str, version: str = "draft-17") -> bool:
    try:
        return feature in FEATURES_BY_VERSION[version]
    except KeyError as exc:
        raise ValueError(f"unsupported SD-JWT VC version: {version}") from exc


__all__ = ["FEATURES_BY_VERSION", "supports"]
