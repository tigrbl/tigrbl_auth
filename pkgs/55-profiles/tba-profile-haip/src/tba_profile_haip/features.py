FEATURES_BY_VERSION = {
    "draft-03": frozenset(
        {
            "oid4vci",
            "oid4vp",
            "sd-jwt-vc",
            "iso-mdoc",
            "wallet-attestation",
            "key-attestation",
        }
    ),
    "1.0": frozenset(
        {
            "oid4vci-1.0",
            "oid4vp-1.0",
            "sd-jwt-vc",
            "iso-mdoc",
            "dcql",
            "wallet-attestation",
            "key-attestation",
            "holder-binding",
            "verifier-attestation",
            "encrypted-responses",
        }
    ),
}


def supports(feature: str, version: str = "1.0") -> bool:
    try:
        return feature in FEATURES_BY_VERSION[version]
    except KeyError as exc:
        raise ValueError(f"unsupported HAIP version: {version}") from exc


__all__ = ["FEATURES_BY_VERSION", "supports"]
