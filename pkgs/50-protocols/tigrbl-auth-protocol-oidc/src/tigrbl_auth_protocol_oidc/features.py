FEATURES_BY_VERSION = {
    "1.0": frozenset(
        {"id-token", "userinfo", "discovery", "standard-claims", "pairwise-subject"}
    ),
    "1.0-errata2": frozenset(
        {
            "id-token",
            "userinfo",
            "discovery",
            "standard-claims",
            "pairwise-subject",
            "errata-set-1",
            "errata-set-2",
        }
    ),
}


def supports(feature: str, version: str = "1.0-errata2") -> bool:
    try:
        return feature in FEATURES_BY_VERSION[version]
    except KeyError as exc:
        raise ValueError(f"unsupported OIDC version: {version}") from exc


__all__ = ["FEATURES_BY_VERSION", "supports"]
