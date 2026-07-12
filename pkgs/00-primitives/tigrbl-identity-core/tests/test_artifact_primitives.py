from __future__ import annotations

import pytest

from tigrbl_identity_core import (
    APPLICATION_DC_SD_JWT,
    ArtifactRef,
    CredentialId,
    CredentialRef,
    CredentialFormat,
    IdentityId,
    IdentityRef,
    MediaType,
    StandardOwner,
    bytes_equal,
    describe_owner,
    digest_bytes,
    digest_text,
    generate_nonce,
    nonce_equal,
    normalize_protocol_tag,
    normalize_protocol_tags,
    require_absolute_uri,
    sha256_digest,
    text_equal,
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
    assert (
        require_absolute_uri("https://issuer.example", https=True)
        == "https://issuer.example"
    )
    with pytest.raises(ValueError, match="HTTPS"):
        require_absolute_uri("http://issuer.example", https=True)


def test_artifact_enums_and_raw_digest() -> None:
    assert CredentialFormat.ISO_MDOC.value == "iso-mdoc"
    assert len(sha256_digest(b"artifact")) == 32


def test_references_digests_and_standard_lifecycle_metadata() -> None:
    identity = IdentityRef(IdentityId("identity-1"))
    credential = CredentialRef(CredentialId("credential-1"), identity.id)
    artifact = ArtifactRef("artifact-1", "credential", digest_text("payload"))
    assert credential.identity_id == identity.id
    assert artifact.digest == digest_bytes(b"payload").hex()
    assert bytes_equal(b"same", b"same") and text_equal("same", "same")
    owner = StandardOwner(
        "OID4VP 1.0",
        "OpenID for Verifiable Presentations 1.0",
        "implemented",
        ("/authorize",),
        "versioned owner",
        organization="OpenID Foundation",
        version="1.0",
        status="final",
        specification_uri="https://openid.net/specs/openid-4-verifiable-presentations-1_0-final.html",
        protocol_tags=("oid4vp",),
        claimable=False,
    )
    assert describe_owner(owner)["version"] == "1.0"
