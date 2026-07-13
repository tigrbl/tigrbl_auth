"""OAuth durable-state aliases and executable runtime specifications."""

from tigrbl_identity_storage.tables import AuthCode, ClientRegistration, RevokedToken

from ..derive import deriveRuntimeTableSpec
from ..make import makeRuntimeOperation
from ..ops.oauth_state import (
    is_token_hash_revoked,
    persist_authorization_code,
    record_revoked_token_hash,
    upsert_client_registration,
)

AuthCodeTable = AuthCode
AuthCodeRuntimeSpec = deriveRuntimeTableSpec(
    AuthCodeTable,
    operations=(
        makeRuntimeOperation(
            alias="authorize",
            handler=persist_authorization_code,
            response_model=AuthCode.schemas.create.out,
        ),
    ),
)

ClientRegistrationTable = ClientRegistration
ClientRegistrationRuntimeSpec = deriveRuntimeTableSpec(
    ClientRegistrationTable,
    operations=(
        makeRuntimeOperation(alias="upsert", handler=upsert_client_registration),
    ),
)

RevokedTokenTable = RevokedToken
RevokedTokenRuntimeSpec = deriveRuntimeTableSpec(
    RevokedTokenTable,
    operations=(
        makeRuntimeOperation(alias="record_hash", handler=record_revoked_token_hash),
        makeRuntimeOperation(alias="is_hash_revoked", handler=is_token_hash_revoked),
    ),
)

__all__ = [
    "AuthCodeRuntimeSpec",
    "AuthCodeTable",
    "ClientRegistrationRuntimeSpec",
    "ClientRegistrationTable",
    "RevokedTokenRuntimeSpec",
    "RevokedTokenTable",
]
