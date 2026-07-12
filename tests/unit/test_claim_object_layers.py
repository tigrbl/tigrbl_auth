import pytest
from tigrbl_attestation_protocol_eat import compose_eat_claim_set
from tigrbl_auth_protocol_oauth import compose_oauth_claim_set
from tigrbl_auth_protocol_oidc import compose_oidc_claim_set
from tigrbl_auth_protocol_jwt import compose_jwt_claim_set
from tigrbl_authentication_context_claim_concrete import AuthenticationContextClaim
from tigrbl_authentication_methods_claim_concrete import AuthenticationMethodsClaim
from tigrbl_authentication_time_claim_concrete import AuthenticationTimeClaim
from tigrbl_audience_claim_concrete import AudienceClaim
from tigrbl_authorized_party_claim_concrete import AuthorizedPartyClaim
from tigrbl_client_id_claim_concrete import ClientIdClaim
from tigrbl_confirmation_claim_concrete import ConfirmationClaim
from tigrbl_credential_profile_sd_jwt_vc import compose_sd_jwt_vc_claim_set
from tigrbl_credential_status_claim_concrete import CredentialStatusClaim
from tigrbl_credential_type_claim_concrete import CredentialTypeClaim
from tigrbl_eat_profile_claim_concrete import EatProfileClaim
from tigrbl_expiration_claim_concrete import ExpirationClaim
from tigrbl_issued_at_claim_concrete import IssuedAtClaim
from tigrbl_issuer_claim_concrete import IssuerClaim
from tigrbl_jwt_id_claim_concrete import JwtIdClaim
from tigrbl_not_before_claim_concrete import NotBeforeClaim
from tigrbl_nonce_claim_concrete import NonceClaim
from tigrbl_scope_claim_concrete import ScopeClaim
from tigrbl_security_event_protocol_set import compose_set_claim_set
from tigrbl_security_events_claim_concrete import SecurityEventsClaim
from tigrbl_subject_claim_concrete import SubjectClaim
from tigrbl_transaction_id_claim_concrete import TransactionIdClaim
from tigrbl_verified_claims_claim_concrete import VerifiedClaimsClaim
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


def test_protocols_compose_independently_owned_claim_classes():
    oidc = compose_oidc_claim_set(
        AuthenticationTimeClaim(10),
        NonceClaim("nonce"),
        AuthenticationContextClaim("phr"),
        AuthenticationMethodsClaim(["pwd", "otp"]),
        AuthorizedPartyClaim("client"),
        VerifiedClaimsClaim({"verification": {}, "claims": {}}),
        TransactionIdClaim("txn-1"),
    )
    oauth = compose_oauth_claim_set(
        ClientIdClaim("client"),
        ScopeClaim("openid profile"),
        ConfirmationClaim({"jkt": "thumbprint"}),
    )
    eat = compose_eat_claim_set(EatProfileClaim("urn:example:eat"), NonceClaim("n"))
    sd_jwt_vc = compose_sd_jwt_vc_claim_set(
        CredentialTypeClaim("urn:example:credential"),
        CredentialStatusClaim({"status_list": {"idx": 1}}),
    )
    security_event = compose_set_claim_set(
        IssuerClaim("https://issuer.example"),
        AudienceClaim("receiver"),
        IssuedAtClaim(10),
        JwtIdClaim("event-1"),
        SecurityEventsClaim({"https://schemas.example/event": {}}),
    )

    assert oidc.protocol == "oidc"
    assert oauth.version == "RFC 9068"
    assert eat.version == "RFC 9711"
    assert sd_jwt_vc.protocol == "sd-jwt-vc"
    assert security_event.version == "RFC 8417"


@pytest.mark.parametrize(
    ("claim_type", "invalid_value"),
    [
        (AuthenticationTimeClaim, "now"),
        (AuthenticationMethodsClaim, []),
        (ConfirmationClaim, []),
        (CredentialStatusClaim, "active"),
        (SecurityEventsClaim, {"not-a-uri": {}}),
        (VerifiedClaimsClaim, []),
    ],
)
def test_extension_claims_reject_wrong_shapes(claim_type, invalid_value):
    with pytest.raises(ValueError):
        claim_type(invalid_value)


def test_protocol_composers_enforce_mandatory_claims():
    with pytest.raises(ValueError, match="requires vct"):
        compose_sd_jwt_vc_claim_set(CredentialStatusClaim({"status_list": {}}))
    with pytest.raises(ValueError, match="missing SET claims"):
        compose_set_claim_set(
            SecurityEventsClaim({"https://schemas.example/event": {}})
        )
