from .versions import CURRENT_VERSION, VcdmVersion


FEATURES_BY_VERSION = {
    VcdmVersion.V1_1.value: frozenset({"credential", "presentation", "issuance-date"}),
    VcdmVersion.V2_0.value: frozenset(
        {
            "credential",
            "presentation",
            "valid-from",
            "valid-until",
            "credential-status",
            "credential-schema",
        }
    ),
}


def supports(feature: str, version: VcdmVersion = CURRENT_VERSION) -> bool:
    return feature in FEATURES_BY_VERSION[version.value]


__all__ = ["FEATURES_BY_VERSION", "supports"]
