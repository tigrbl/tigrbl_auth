"""OIDC Core 1.0 claim-set composition."""

from tigrbl_identity_contracts.claims import ClaimSet
from tigrbl_claim_authentication_context_concrete import AuthenticationContextClaim
from tigrbl_claim_authentication_methods_concrete import AuthenticationMethodsClaim
from tigrbl_claim_authentication_time_concrete import AuthenticationTimeClaim
from tigrbl_claim_address_country_code_concrete import AddressCountryCodeClaim
from tigrbl_claim_also_known_as_concrete import AlsoKnownAsClaim
from tigrbl_claim_authorized_party_concrete import AuthorizedPartyClaim
from tigrbl_claim_birth_family_name_concrete import BirthFamilyNameClaim
from tigrbl_claim_birth_given_name_concrete import BirthGivenNameClaim
from tigrbl_claim_birth_middle_name_concrete import BirthMiddleNameClaim
from tigrbl_claim_msisdn_concrete import MsisdnClaim
from tigrbl_claim_nationalities_concrete import NationalitiesClaim
from tigrbl_claim_nonce_concrete import NonceClaim
from tigrbl_claim_place_of_birth_concrete import PlaceOfBirthClaim
from tigrbl_claim_salutation_concrete import SalutationClaim
from tigrbl_claim_title_concrete import TitleClaim
from tigrbl_claim_transaction_id_concrete import TransactionIdClaim
from tigrbl_claim_verified_claims_concrete import VerifiedClaimsClaim
from tigrbl_claim_access_token_hash_oidc_concrete import OidcAccessTokenHashClaim
from tigrbl_claim_address_concrete import AddressClaim
from tigrbl_claim_authorization_code_hash_concrete import AuthorizationCodeHashClaim
from tigrbl_claim_birthdate_concrete import BirthdateClaim
from tigrbl_claim_email_concrete import EmailClaim
from tigrbl_claim_email_verified_concrete import EmailVerifiedClaim
from tigrbl_claim_family_name_concrete import FamilyNameClaim
from tigrbl_claim_gender_concrete import GenderClaim
from tigrbl_claim_given_name_concrete import GivenNameClaim
from tigrbl_claim_locale_concrete import LocaleClaim
from tigrbl_claim_middle_name_concrete import MiddleNameClaim
from tigrbl_claim_name_concrete import NameClaim
from tigrbl_claim_nickname_concrete import NicknameClaim
from tigrbl_claim_phone_number_concrete import PhoneNumberClaim
from tigrbl_claim_phone_number_verified_concrete import PhoneNumberVerifiedClaim
from tigrbl_claim_picture_uri_concrete import PictureUriClaim
from tigrbl_claim_preferred_username_concrete import PreferredUsernameClaim
from tigrbl_claim_profile_uri_concrete import ProfileUriClaim
from tigrbl_claim_session_id_concrete import SessionIdClaim
from tigrbl_claim_state_hash_concrete import StateHashClaim
from tigrbl_claim_updated_at_concrete import UpdatedAtClaim
from tigrbl_claim_website_uri_concrete import WebsiteUriClaim
from tigrbl_claim_zoneinfo_concrete import ZoneinfoClaim

OIDC_USERINFO_CLAIMS = (
    NameClaim,
    GivenNameClaim,
    FamilyNameClaim,
    MiddleNameClaim,
    NicknameClaim,
    PreferredUsernameClaim,
    ProfileUriClaim,
    PictureUriClaim,
    WebsiteUriClaim,
    EmailClaim,
    EmailVerifiedClaim,
    GenderClaim,
    BirthdateClaim,
    ZoneinfoClaim,
    LocaleClaim,
    PhoneNumberClaim,
    PhoneNumberVerifiedClaim,
    AddressClaim,
    UpdatedAtClaim,
)

OIDC_ID_TOKEN_PROFILE_CLAIMS = (
    AuthenticationTimeClaim,
    NonceClaim,
    AuthenticationContextClaim,
    AuthenticationMethodsClaim,
    AuthorizedPartyClaim,
    OidcAccessTokenHashClaim,
    AuthorizationCodeHashClaim,
    StateHashClaim,
    SessionIdClaim,
)

OIDC_EXTENSION_CLAIMS = (
    AuthenticationTimeClaim,
    NonceClaim,
    AuthenticationContextClaim,
    AuthenticationMethodsClaim,
    AuthorizedPartyClaim,
    VerifiedClaimsClaim,
    TransactionIdClaim,
    PlaceOfBirthClaim,
    NationalitiesClaim,
    BirthFamilyNameClaim,
    BirthGivenNameClaim,
    BirthMiddleNameClaim,
    SalutationClaim,
    TitleClaim,
    MsisdnClaim,
    AlsoKnownAsClaim,
    AddressCountryCodeClaim,
)


def compose_oidc_claim_set(*claims) -> ClaimSet:
    return ClaimSet(tuple(claims), "oidc", "1.0-errata2")


def compose_oidc_userinfo_claim_set(*claims) -> ClaimSet:
    return ClaimSet(tuple(claims), "oidc-userinfo", "1.0-errata2")


def compose_oidc_id_token_claim_set(*claims) -> ClaimSet:
    return ClaimSet(tuple(claims), "oidc-id-token", "1.0-errata2")


__all__ = [
    "OIDC_EXTENSION_CLAIMS",
    "OIDC_ID_TOKEN_PROFILE_CLAIMS",
    "OIDC_USERINFO_CLAIMS",
    "compose_oidc_claim_set",
    "compose_oidc_id_token_claim_set",
    "compose_oidc_userinfo_claim_set",
]
