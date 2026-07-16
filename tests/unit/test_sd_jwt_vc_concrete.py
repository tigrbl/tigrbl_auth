import base64
import json

import pytest
from tigrbl_sd_jwt_concrete import Disclosure, disclosure_digest, encode_disclosure
from tigrbl_credential_profile_sd_jwt_vc import (
    DRAFT_REVISION,
    MEDIA_TYPE,
    parse_sd_jwt_vc,
    parse_status_reference,
    parse_type_metadata,
    validate_sd_jwt_vc,
)


def _segment(value: object) -> str:
    return base64.urlsafe_b64encode(json.dumps(value).encode()).rstrip(b"=").decode()


def _credential(
    claims: dict, disclosure: str | None = None, typ: str = "dc+sd-jwt"
) -> str:
    issuer_jwt = (
        f"{_segment({'alg': 'ES256', 'typ': typ})}.{_segment(claims)}.signature"
    )
    return issuer_jwt + (f"~{disclosure}~" if disclosure else "~")


def test_sd_jwt_vc_revision_media_type_and_required_vct_are_pinned():
    credential = parse_sd_jwt_vc(
        _credential({"vct": "https://example.org/types/employee"})
    )
    validate_sd_jwt_vc(credential)
    assert DRAFT_REVISION == "draft-ietf-oauth-sd-jwt-vc-17"
    assert MEDIA_TYPE == "application/dc+sd-jwt"


def test_sd_jwt_vc_disclosure_must_be_referenced():
    disclosure = encode_disclosure(Disclosure("salt", "given_name", "Alice"))
    credential = parse_sd_jwt_vc(
        _credential(
            {
                "vct": "urn:example:employee",
                "_sd_alg": "sha-256",
                "_sd": [disclosure_digest(disclosure)],
            },
            disclosure,
        )
    )
    validate_sd_jwt_vc(credential)
    with pytest.raises(ValueError, match="unreferenced"):
        validate_sd_jwt_vc(
            parse_sd_jwt_vc(_credential({"vct": "urn:example"}, disclosure))
        )


def test_legacy_typ_requires_explicit_compatibility_selection():
    credential = parse_sd_jwt_vc(_credential({"vct": "urn:example"}, typ="vc+sd-jwt"))
    with pytest.raises(ValueError, match="typ"):
        validate_sd_jwt_vc(credential)
    validate_sd_jwt_vc(credential, accept_legacy_typ=True)


def test_type_metadata_and_status_are_structurally_validated():
    metadata = parse_type_metadata(
        {
            "vct": "urn:example:employee",
            "name": "Employee",
            "claims": [{"path": ["name"]}],
        }
    )
    status = parse_status_reference(
        {"status_list": {"idx": 4, "uri": "https://example/status"}}
    )
    assert metadata.name == "Employee" and status.index == 4
    with pytest.raises(ValueError):
        parse_status_reference({"one": {}, "two": {}})


def test_sd_jwt_vc_does_not_make_issuer_trust_decisions():
    credential = parse_sd_jwt_vc(
        _credential({"vct": "urn:example", "iss": "https://issuer"})
    )
    validate_sd_jwt_vc(credential)
    assert not hasattr(credential, "trusted")
