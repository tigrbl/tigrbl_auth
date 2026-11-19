"""RFC 8392 feature ownership."""

from .versions import CURRENT_VERSION

FEATURES_BY_VERSION = {
    CURRENT_VERSION.value: frozenset(
        {"registered-claims", "cbor-map", "cose-protection", "application-cwt"}
    )
}


def supports(feature: str, version: str = CURRENT_VERSION.value) -> bool:
    try:
        return feature in FEATURES_BY_VERSION[version]
    except KeyError as exc:
        raise ValueError(f"unsupported CWT version: {version}") from exc


__all__ = ["FEATURES_BY_VERSION", "supports"]
