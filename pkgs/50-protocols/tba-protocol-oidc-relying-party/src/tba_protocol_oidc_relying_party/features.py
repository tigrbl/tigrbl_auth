"""Features selected by each RP composite profile revision."""

from .versions import CURRENT_VERSION, VERSION_HISTORY

FEATURES_BY_VERSION = {
    VERSION_HISTORY[0].identifier: frozenset(
        {"authorization-code", "id-token", "userinfo", "discovery"}
    ),
    CURRENT_VERSION.identifier: frozenset(
        {
            "authorization-code",
            "id-token",
            "userinfo",
            "discovery",
            "pkce-s256",
            "rp-initiated-logout",
            "callback-issuer-validation",
            "browser-memory-only",
        }
    ),
}


def supports(feature: str, version: str = CURRENT_VERSION.identifier) -> bool:
    try:
        return feature in FEATURES_BY_VERSION[version]
    except KeyError as exc:
        raise ValueError(f"unsupported RP profile version: {version}") from exc


__all__ = ["FEATURES_BY_VERSION", "supports"]
