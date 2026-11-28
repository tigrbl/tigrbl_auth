from .versions import CURRENT_VERSION, IsoMdocVersion


FEATURES_BY_VERSION = {
    IsoMdocVersion.ISO_18013_5_2021.value: frozenset(
        {"issuer-signed", "device-signed", "session-transcript", "cbor", "cose"}
    )
}


def supports(feature: str, version: IsoMdocVersion = CURRENT_VERSION) -> bool:
    return feature in FEATURES_BY_VERSION[version.value]


__all__ = ["FEATURES_BY_VERSION", "supports"]
