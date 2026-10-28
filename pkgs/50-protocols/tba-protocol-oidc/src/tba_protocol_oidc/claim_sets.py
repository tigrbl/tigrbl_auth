"""OIDC Core 1.0 claim-set composition."""

from tba_contracts_identity.claims import ClaimSet
from tba_concrete_claim_authentication_context import AuthenticationContextClaim
from tba_concrete_claim_authentication_methods import AuthenticationMethodsClaim
from tba_concrete_claim_authentication_time import AuthenticationTimeClaim
from tba_concrete_claim_address_country_code import AddressCountryCodeClaim
from tba_concrete_claim_also_known_as import AlsoKnownAsClaim
from tba_concrete_claim_authorized_party import AuthorizedPartyClaim
from tba_concrete_claim_birth_family_name import BirthFamilyNameClaim
from tba_concrete_claim_birth_given_name import BirthGivenNameClaim
from tba_concrete_claim_birth_middle_name import BirthMiddleNameClaim
from tba_concrete_claim_msisdn import MsisdnClaim
from tba_concrete_claim_nationalities import NationalitiesClaim
from tba_concrete_claim_nonce import NonceClaim
from tba_concrete_claim_place_of_birth import PlaceOfBirthClaim
from tba_concrete_claim_salutation import SalutationClaim
from tba_concrete_claim_title import TitleClaim
from tba_concrete_claim_transaction_id import TransactionIdClaim
from tba_concrete_claim_verified_claims import VerifiedClaimsClaim
from tba_concrete_claim_access_token_hash import AccessTokenHashClaim
from tba_concrete_claim_address import AddressClaim
from tba_concrete_claim_authorization_code_hash import AuthorizationCodeHashClaim
from tba_concrete_claim_birthdate import BirthdateClaim
from tba_concrete_claim_email import EmailClaim
from tba_concrete_claim_email_verified import EmailVerifiedClaim
from tba_concrete_claim_family_name import FamilyNameClaim
from tba_concrete_claim_gender import GenderClaim
from tba_concrete_claim_given_name import GivenNameClaim
from tba_concrete_claim_locale import LocaleClaim
from tba_concrete_claim_middle_name import MiddleNameClaim
from tba_concrete_claim_name import NameClaim
from tba_concrete_claim_nickname import NicknameClaim
from tba_concrete_claim_phone_number import PhoneNumberClaim
from tba_concrete_claim_phone_number_verified import PhoneNumberVerifiedClaim
from tba_concrete_claim_picture_uri import PictureUriClaim
from tba_concrete_claim_preferred_username import PreferredUsernameClaim
from tba_concrete_claim_profile_uri import ProfileUriClaim
from tba_concrete_claim_session_id import SessionIdClaim
from tba_concrete_claim_state_hash import StateHashClaim
from tba_concrete_claim_updated_at import UpdatedAtClaim
from tba_concrete_claim_website_uri import WebsiteUriClaim
from tba_concrete_claim_zoneinfo import ZoneinfoClaim

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
    AccessTokenHashClaim,
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
