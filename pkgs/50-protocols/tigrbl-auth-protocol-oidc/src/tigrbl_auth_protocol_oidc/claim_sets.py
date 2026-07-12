"""OIDC Core 1.0 claim-set composition."""

from tigrbl_identity_contracts.claims import ClaimSet
from tigrbl_authentication_context_claim_concrete import AuthenticationContextClaim
from tigrbl_authentication_methods_claim_concrete import AuthenticationMethodsClaim
from tigrbl_authentication_time_claim_concrete import AuthenticationTimeClaim
from tigrbl_address_country_code_claim_concrete import AddressCountryCodeClaim
from tigrbl_also_known_as_claim_concrete import AlsoKnownAsClaim
from tigrbl_authorized_party_claim_concrete import AuthorizedPartyClaim
from tigrbl_birth_family_name_claim_concrete import BirthFamilyNameClaim
from tigrbl_birth_given_name_claim_concrete import BirthGivenNameClaim
from tigrbl_birth_middle_name_claim_concrete import BirthMiddleNameClaim
from tigrbl_msisdn_claim_concrete import MsisdnClaim
from tigrbl_nationalities_claim_concrete import NationalitiesClaim
from tigrbl_nonce_claim_concrete import NonceClaim
from tigrbl_place_of_birth_claim_concrete import PlaceOfBirthClaim
from tigrbl_salutation_claim_concrete import SalutationClaim
from tigrbl_title_claim_concrete import TitleClaim
from tigrbl_transaction_id_claim_concrete import TransactionIdClaim
from tigrbl_verified_claims_claim_concrete import VerifiedClaimsClaim

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
    return ClaimSet(tuple(claims), "oidc", "1.0")


__all__ = ["OIDC_EXTENSION_CLAIMS", "compose_oidc_claim_set"]
