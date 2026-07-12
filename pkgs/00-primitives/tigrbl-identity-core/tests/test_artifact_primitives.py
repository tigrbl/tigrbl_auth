from __future__ import annotations

import pytest

from tigrbl_identity_core import (
    APPLICATION_DC_SD_JWT,
    CredentialFormat,
    MediaType,
    generate_nonce,
    nonce_equal,
    normalize_protocol_tag,
    normalize_protocol_tags,
    require_absolute_uri,
    sha256_digest,
)


def test_protocol_tags_are_canonicalized() -> None:
    assert normalize_protocol_tag("XCAML") == "xacml"
    assert normalize_protocol_tag("OIDC4VI") == "oid4vci"
    assert normalize_protocol_tag("isomdc") == "iso-mdoc"
    assert normalize_protocol_tags(["oauth", "OIDC", "oauth"]) == ("oauth", "oidc")


def test_unknown_protocol_tag_is_rejected() -> None:
    with pytest.raises(ValueError, match="unknown protocol tag"):
        normalize_protocol_tag("not-a-protocol")


def test_nonce_generation_and_comparison() -> None:
    nonce = generate_nonce()
    assert len(nonce) >= 22
    assert nonce_equal(nonce, nonce)
    assert not nonce_equal(nonce, generate_nonce())
    with pytest.raises(ValueError, match="at least"):
        generate_nonce(size=8)


def test_media_type_and_uri_validation() -> None:
    assert str(APPLICATION_DC_SD_JWT) == "application/dc+sd-jwt"
    assert MediaType("APPLICATION/VC").value == "application/vc"
    assert require_absolute_uri("https://issuer.example", https=True) == "https://issuer.example"
    with pytest.raises(ValueError, match="HTTPS"):
        require_absolute_uri("http://issuer.example", https=True)


def test_artifact_enums_and_raw_digest() -> None:
    assert CredentialFormat.ISO_MDOC.value == "iso-mdoc"
    assert len(sha256_digest(b"artifact")) == 32
