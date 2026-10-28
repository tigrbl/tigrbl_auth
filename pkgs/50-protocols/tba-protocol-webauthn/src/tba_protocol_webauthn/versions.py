from dataclasses import dataclass


class WebAuthnVersion:
    """String constants; version history remains owned by this protocol package."""

    LEVEL_2 = "level-2"
    LEVEL_3 = "level-3"


@dataclass(frozen=True, slots=True)
class WebAuthnRevision:
    version: str
    publication_date: str
    status: str
    specification_uri: str

    @property
    def identifier(self) -> str:
        return self.version


WEB_AUTHN_REVISIONS = {
    WebAuthnVersion.LEVEL_2: WebAuthnRevision(
        WebAuthnVersion.LEVEL_2,
        "2021-04-08",
        "W3C Recommendation",
        "https://www.w3.org/TR/webauthn-2/",
    ),
    WebAuthnVersion.LEVEL_3: WebAuthnRevision(
        WebAuthnVersion.LEVEL_3,
        "2026-05-26",
        "W3C Candidate Recommendation Snapshot",
        "https://www.w3.org/TR/webauthn-3/",
    ),
}

CURRENT_VERSION = WEB_AUTHN_REVISIONS[WebAuthnVersion.LEVEL_2]


def resolve_revision(value: str) -> WebAuthnRevision:
    try:
        return WEB_AUTHN_REVISIONS[value]
    except KeyError as exc:
        raise ValueError(f"unsupported WebAuthn version: {value}") from exc


__all__ = [
    "CURRENT_VERSION",
    "WEB_AUTHN_REVISIONS",
    "WebAuthnRevision",
    "WebAuthnVersion",
    "resolve_revision",
]
