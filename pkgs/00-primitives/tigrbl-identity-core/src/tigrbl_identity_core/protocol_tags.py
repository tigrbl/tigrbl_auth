"""Canonical protocol-family tags used across package metadata."""

from typing import Final

PROTOCOL_TAGS: Final[frozenset[str]] = frozenset(
    {
        "authzen",
        "cbor",
        "comid",
        "corim",
        "cose",
        "coswid",
        "cotl",
        "cots",
        "cwt",
        "dc-api",
        "did-core",
        "dpop",
        "eat",
        "fido",
        "fido-mds",
        "fido2",
        "gnap",
        "haip",
        "identity-assurance",
        "iso-mdoc",
        "jose",
        "jwe",
        "jws",
        "jwt",
        "kb-jwt",
        "mtls",
        "oauth",
        "oid4vci",
        "oid4vp",
        "oidc",
        "openid-federation",
        "pkce",
        "passkey",
        "rar",
        "rats",
        "sd-jwt",
        "sd-jwt-vc",
        "set",
        "shared-signals",
        "spiffe",
        "svid",
        "token-exchange",
        "ctap",
        "ctap2",
        "w3c-vcdm",
        "w3c-vp",
        "webauthn",
        "x509",
        "xacml",
        "zta",
    }
)

PROTOCOL_TAG_ALIASES: Final[dict[str, str]] = {
    "xcaml": "xacml",
    "oidc4vi": "oid4vci",
    "oidc4vci": "oid4vci",
    "openid4vci": "oid4vci",
    "openid4vp": "oid4vp",
    "isomdc": "iso-mdoc",
    "mdoc": "iso-mdoc",
    "x.509": "x509",
}


def normalize_protocol_tag(value: str) -> str:
    tag = str(value).strip().lower().replace("_", "-")
    tag = PROTOCOL_TAG_ALIASES.get(tag, tag)
    if tag not in PROTOCOL_TAGS:
        raise ValueError(f"unknown protocol tag: {value}")
    return tag


def normalize_protocol_tags(
    values: list[str] | tuple[str, ...] | set[str],
) -> tuple[str, ...]:
    return tuple(sorted({normalize_protocol_tag(value) for value in values}))


__all__ = [
    "PROTOCOL_TAG_ALIASES",
    "PROTOCOL_TAGS",
    "normalize_protocol_tag",
    "normalize_protocol_tags",
]
