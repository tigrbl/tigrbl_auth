import pytest
from tigrbl_auth_protocol_jwt import compose_jwt_claim_set
from tigrbl_audience_claim_concrete import AudienceClaim
from tigrbl_expiration_claim_concrete import ExpirationClaim
from tigrbl_issued_at_claim_concrete import IssuedAtClaim
from tigrbl_issuer_claim_concrete import IssuerClaim
from tigrbl_jwt_id_claim_concrete import JwtIdClaim
from tigrbl_not_before_claim_concrete import NotBeforeClaim
from tigrbl_subject_claim_concrete import SubjectClaim
from tigrbl_identity_contracts.claims import Claim, ClaimSet
from tigrbl_identity_claims_bases import ClaimBase
from tigrbl_identity_core import ClaimType, RegisteredClaim


def test_registered_claim_taxonomy_and_standalone_classes():
    claims = (
        IssuerClaim("https://issuer.example"),
        SubjectClaim("subject"),
        AudienceClaim(["api"]),
        ExpirationClaim(20),
        NotBeforeClaim(5),
        IssuedAtClaim(10),
        JwtIdClaim("jti-1"),
    )
    assert all(isinstance(item, (Claim, ClaimBase)) for item in claims)
    assert ClaimSet(claims, "jwt", "RFC 7519").as_mapping()["sub"] == "subject"
    assert compose_jwt_claim_set(*claims).version == "RFC 7519"
    assert (
        RegisteredClaim.SUBJECT == "sub" and claims[1].claim_type is ClaimType.IDENTITY
    )


def test_claim_classes_reject_invalid_values():
    with pytest.raises(ValueError):
        ExpirationClaim("tomorrow")
    with pytest.raises(ValueError):
        AudienceClaim([])
