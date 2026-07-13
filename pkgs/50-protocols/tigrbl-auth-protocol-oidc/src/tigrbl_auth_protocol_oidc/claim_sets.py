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


__all__ = ["OIDC_EXTENSION_CLAIMS", "compose_oidc_claim_set"]
