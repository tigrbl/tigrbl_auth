_OAUTH_21_FEATURES = frozenset(
    {
        "authorization-code",
        "client-credentials",
        "refresh-token",
        "pkce-required",
        "exact-redirect-uri",
        "no-implicit",
        "no-password-grant",
    }
)

FEATURES_BY_VERSION = {
    "RFC6749": frozenset(
        {
            "authorization-code",
            "implicit",
            "password",
            "client-credentials",
            "refresh-token",
        }
    ),
    "draft-ietf-oauth-v2-1-13": _OAUTH_21_FEATURES,
    "draft-ietf-oauth-v2-1-14": _OAUTH_21_FEATURES,
    "draft-ietf-oauth-v2-1-15": _OAUTH_21_FEATURES,
}


def supports(feature: str, version: str = "draft-ietf-oauth-v2-1-15") -> bool:
    try:
        return feature in FEATURES_BY_VERSION[version]
    except KeyError as exc:
        raise ValueError(f"unsupported OAuth version/profile: {version}") from exc


__all__ = ["FEATURES_BY_VERSION", "supports"]
