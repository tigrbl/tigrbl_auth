from enum import StrEnum


class TokenProfile(StrEnum):
    ACCESS_TOKEN = "access-token"
    ID_TOKEN = "id-token"
    REFRESH_TOKEN = "refresh-token"
    SECURITY_EVENT_TOKEN = "security-event-token"
    ENTITY_ATTESTATION_TOKEN = "entity-attestation-token"
    JWT_SVID = "jwt-svid"
    SD_JWT_KEY_BINDING = "kb-jwt"
    WALLET_ATTESTATION = "wallet-attestation"


class TokenEnvelopeFormat(StrEnum):
    JWT = "jwt"
    CWT = "cwt"


__all__ = ["TokenEnvelopeFormat", "TokenProfile"]
