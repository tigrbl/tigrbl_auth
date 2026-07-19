"""Standalone RFC 8747 CWT confirmation claim."""

from tigrbl_claim_bases import ClaimBase
from tigrbl_identity_core import ClaimNameKind, ClaimType, ClaimValueType


class CwtConfirmationClaim(ClaimBase):
    claim_name = 8
    default_name_kind = ClaimNameKind.INTEGER_LABEL
    default_registry = "IANA CWT Claims"
    default_claim_type = ClaimType.AUTHORIZATION
    default_value_type = ClaimValueType.JSON_OBJECT
    default_standards = ("RFC8747", "RFC9679")

    @classmethod
    def validate_value(cls, value):
        if not isinstance(value, dict) or len(value) != 1:
            raise ValueError("CWT cnf requires exactly one confirmation method")
        method, confirmation = next(iter(value.items()))
        if method == 1 and not isinstance(confirmation, dict):
            raise ValueError("CWT cnf COSE_Key method requires a CBOR map")
        if method == 2 and not isinstance(confirmation, (list, tuple)):
            raise ValueError("CWT cnf Encrypted_COSE_Key requires a COSE array")
        if method in {3, 5} and not isinstance(confirmation, bytes):
            raise ValueError("CWT cnf kid and ckt methods require byte strings")
        if method not in {1, 2, 3, 5}:
            raise ValueError("unsupported CWT confirmation method")
        if method in {3, 5} and not confirmation:
            raise ValueError("CWT confirmation byte strings must not be empty")


__all__ = ["CwtConfirmationClaim"]