import pytest
from tba_concrete_claim_address_country_code import AddressCountryCodeClaim
from tba_concrete_claim_also_known_as import AlsoKnownAsClaim
from tba_protocol_attestation_eat import compose_eat_claim_set
from tba_protocol_oauth import compose_oauth_claim_set
from tba_protocol_oidc import compose_oidc_claim_set
from tba_protocol_jwt import compose_jwt_claim_set
from tba_concrete_claim_authentication_context import AuthenticationContextClaim
from tba_concrete_claim_authentication_methods import AuthenticationMethodsClaim
from tba_concrete_claim_authentication_time import AuthenticationTimeClaim
from tba_concrete_claim_audience import AudienceClaim
from tba_concrete_claim_authorized_party import AuthorizedPartyClaim
from tba_concrete_claim_birth_family_name import BirthFamilyNameClaim
from tba_concrete_claim_birth_given_name import BirthGivenNameClaim
from tba_concrete_claim_birth_middle_name import BirthMiddleNameClaim
from tba_concrete_claim_client_id import ClientIdClaim
from tba_concrete_claim_confirmation import ConfirmationClaim
from tba_profile_credential_sd_jwt_vc import compose_sd_jwt_vc_claim_set
from tba_concrete_claim_credential_status import CredentialStatusClaim
from tba_concrete_claim_credential_type import CredentialTypeClaim
from tba_concrete_claim_eat_profile import EatProfileClaim
from tba_concrete_claim_expiration import ExpirationClaim
from tba_concrete_claim_issued_at import IssuedAtClaim
from tba_concrete_claim_issuer import IssuerClaim
from tba_concrete_claim_jwt_id import JwtIdClaim
from tba_concrete_claim_msisdn import MsisdnClaim
from tba_concrete_claim_nationalities import NationalitiesClaim
from tba_concrete_claim_not_before import NotBeforeClaim
from tba_concrete_claim_place_of_birth import PlaceOfBirthClaim
from tba_concrete_claim_salutation import SalutationClaim
from tba_concrete_claim_nonce import NonceClaim
from tba_concrete_claim_scope import ScopeClaim
from tba_protocol_security_event_set import compose_set_claim_set
from tba_concrete_claim_security_events import SecurityEventsClaim
from tba_concrete_claim_subject import SubjectClaim
from tba_concrete_claim_transaction_id import TransactionIdClaim
from tba_concrete_claim_title import TitleClaim
from tba_concrete_claim_verified_claims import VerifiedClaimsClaim
from tba_contracts_identity.claims import Claim, ClaimSet
from tba_bases_identity_claims import ClaimBase
from tba_primitives_identity import ClaimType, RegisteredClaim


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
