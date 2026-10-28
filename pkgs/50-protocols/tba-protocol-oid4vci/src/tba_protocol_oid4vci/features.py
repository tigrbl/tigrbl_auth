FEATURES_BY_VERSION = {
    "draft-11": frozenset({"credential-offer", "pre-authorized-code", "deferred"}),
    "draft-15": frozenset(
        {"credential-offer", "pre-authorized-code", "deferred", "notification", "batch"}
    ),
    "1.0": frozenset(
        {
            "credential-offer",
            "pre-authorized-code",
            "authorization-code",
            "deferred",
            "notification",
            "batch",
            "credential-configuration-id",
            "proofs",
        }
    ),
}


def supports(feature: str, version: str = "1.0") -> bool:
    try:
        return feature in FEATURES_BY_VERSION[version]
    except KeyError as exc:
        raise ValueError(f"unsupported OID4VCI version: {version}") from exc


__all__ = ["FEATURES_BY_VERSION", "supports"]
