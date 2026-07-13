import pytest
from tigrbl_claim_address_country_code_concrete import AddressCountryCodeClaim
from tigrbl_claim_also_known_as_concrete import AlsoKnownAsClaim
from tigrbl_attestation_protocol_eat import compose_eat_claim_set
from tigrbl_auth_protocol_oauth import compose_oauth_claim_set
from tigrbl_auth_protocol_oidc import compose_oidc_claim_set
from tigrbl_auth_protocol_jwt import compose_jwt_claim_set
from tigrbl_claim_authentication_context_concrete import AuthenticationContextClaim
from tigrbl_claim_authentication_methods_concrete import AuthenticationMethodsClaim
from tigrbl_claim_authentication_time_concrete import AuthenticationTimeClaim
from tigrbl_claim_audience_concrete import AudienceClaim
from tigrbl_claim_authorized_party_concrete import AuthorizedPartyClaim
from tigrbl_claim_birth_family_name_concrete import BirthFamilyNameClaim
from tigrbl_claim_birth_given_name_concrete import BirthGivenNameClaim
from tigrbl_claim_birth_middle_name_concrete import BirthMiddleNameClaim
from tigrbl_claim_client_id_concrete import ClientIdClaim
from tigrbl_claim_confirmation_concrete import ConfirmationClaim
from tigrbl_credential_profile_sd_jwt_vc import compose_sd_jwt_vc_claim_set
from tigrbl_claim_credential_status_concrete import CredentialStatusClaim
from tigrbl_claim_credential_type_concrete import CredentialTypeClaim
from tigrbl_claim_eat_profile_concrete import EatProfileClaim
from tigrbl_claim_expiration_concrete import ExpirationClaim
from tigrbl_claim_issued_at_concrete import IssuedAtClaim
from tigrbl_claim_issuer_concrete import IssuerClaim
from tigrbl_claim_jwt_id_concrete import JwtIdClaim
from tigrbl_claim_msisdn_concrete import MsisdnClaim
from tigrbl_claim_nationalities_concrete import NationalitiesClaim
from tigrbl_claim_not_before_concrete import NotBeforeClaim
from tigrbl_claim_place_of_birth_concrete import PlaceOfBirthClaim
from tigrbl_claim_salutation_concrete import SalutationClaim
from tigrbl_claim_nonce_concrete import NonceClaim
from tigrbl_claim_scope_concrete import ScopeClaim
from tigrbl_security_event_protocol_set import compose_set_claim_set
from tigrbl_claim_security_events_concrete import SecurityEventsClaim
from tigrbl_claim_subject_concrete import SubjectClaim
from tigrbl_claim_transaction_id_concrete import TransactionIdClaim
from tigrbl_claim_title_concrete import TitleClaim
from tigrbl_claim_verified_claims_concrete import VerifiedClaimsClaim
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
    assert compose_jwt_claim_set(*claims).version == "RFC7519"
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
    assert eat.version == "RFC9711"
    assert sd_jwt_vc.protocol == "sd-jwt-vc"
    assert security_event.version == "RFC8417"


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


def test_identity_assurance_claims_each_have_standalone_concrete_classes():
    claims = (
        PlaceOfBirthClaim({"country": "US"}),
        NationalitiesClaim(["US"]),
        BirthFamilyNameClaim("Example"),
        BirthGivenNameClaim("Alice"),
        BirthMiddleNameClaim("B"),
        SalutationClaim("Dr"),
        TitleClaim("Engineer"),
        MsisdnClaim("+12025550123"),
        AlsoKnownAsClaim("A. Example"),
        AddressCountryCodeClaim("US"),
    )
    composed = compose_oidc_claim_set(*claims)
    assert {claim.name for claim in composed.claims} == {
        "place_of_birth",
        "nationalities",
        "birth_family_name",
        "birth_given_name",
        "birth_middle_name",
        "salutation",
        "title",
        "msisdn",
        "also_known_as",
        "address.country_code",
    }
    with pytest.raises(ValueError):
        BirthGivenNameClaim(42)
    with pytest.raises(ValueError):
        AddressCountryCodeClaim("usa")
