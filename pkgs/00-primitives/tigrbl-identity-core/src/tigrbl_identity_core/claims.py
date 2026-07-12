"""Primitive claim taxonomy shared across token and credential families."""

from enum import StrEnum


class ClaimType(StrEnum):
    IDENTITY = "identity"
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    ASSURANCE = "assurance"
    CREDENTIAL = "credential"
    ATTESTATION = "attestation"
    SECURITY_EVENT = "security-event"
    WORKLOAD = "workload"
    TRANSACTION = "transaction"
    PROTOCOL = "protocol"


class ClaimValueType(StrEnum):
    STRING = "string"
    STRING_LIST = "string-list"
    NUMBER = "number"
    BOOLEAN = "boolean"
    URI = "uri"
    TIMESTAMP = "timestamp"
    JSON_OBJECT = "json-object"
    JSON_VALUE = "json-value"


class RegisteredClaim(StrEnum):
    ISSUER = "iss"
    SUBJECT = "sub"
    AUDIENCE = "aud"
    EXPIRATION = "exp"
    NOT_BEFORE = "nbf"
    ISSUED_AT = "iat"
    JWT_ID = "jti"
    AUTH_TIME = "auth_time"
    NONCE = "nonce"
    AUTH_CONTEXT = "acr"
    AUTH_METHODS = "amr"
    AUTHORIZED_PARTY = "azp"
    CONFIRMATION = "cnf"
    SCOPE = "scope"
    CLIENT_ID = "client_id"
    VERIFIED_CLAIMS = "verified_claims"
    PLACE_OF_BIRTH = "place_of_birth"
    NATIONALITIES = "nationalities"
    BIRTH_FAMILY_NAME = "birth_family_name"
    BIRTH_GIVEN_NAME = "birth_given_name"
    BIRTH_MIDDLE_NAME = "birth_middle_name"
    SALUTATION = "salutation"
    TITLE = "title"
    MSISDN = "msisdn"
    ALSO_KNOWN_AS = "also_known_as"
    ADDRESS_COUNTRY_CODE = "address.country_code"
    CREDENTIAL_TYPE = "vct"
    CREDENTIAL_STATUS = "status"
    SECURITY_EVENTS = "events"
    TRANSACTION_ID = "txn"
    EAT_PROFILE = "eat_profile"


__all__ = ["ClaimType", "ClaimValueType", "RegisteredClaim"]
