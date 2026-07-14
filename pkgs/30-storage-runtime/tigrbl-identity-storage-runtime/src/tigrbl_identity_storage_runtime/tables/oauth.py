"""OAuth durable-state aliases and executable runtime specifications."""

from tigrbl_identity_storage.tables import (
    AuthCode,
    ClientRegistration,
    DeviceCode,
    PushedAuthorizationRequest,
    RevokedToken,
)

from ..derive import deriveRuntimeTableSpec
from ..make import makeRuntimeOperation
from ..ops.oauth_state import (
    create_client_registration,
    disable_client_registration,
    is_token_hash_revoked,
    persist_authorization_code,
    persist_pushed_authorization_request,
    read_client_registration,
    record_revoked_token_hash,
    update_client_registration,
    upsert_client_registration,
)
from ..ops.device_codes import approve_device_code, deny_device_code

AuthCodeTable = AuthCode
AuthCodeRuntimeSpec = deriveRuntimeTableSpec(
    AuthCodeTable,
    operations=(
        makeRuntimeOperation(
            alias="authorize",
            handler=persist_authorization_code,
        ),
    ),
)

ClientRegistrationTable = ClientRegistration
ClientRegistrationRuntimeSpec = deriveRuntimeTableSpec(
    ClientRegistrationTable,
    operations=(
        makeRuntimeOperation(alias="register", handler=create_client_registration),
        makeRuntimeOperation(
            alias="get_registration",
            handler=read_client_registration,
            tx_scope="read_only",
            persist="skip",
        ),
        makeRuntimeOperation(
            alias="update_registration",
            handler=update_client_registration,
        ),
        makeRuntimeOperation(
            alias="disable_registration",
            handler=disable_client_registration,
        ),
        makeRuntimeOperation(alias="upsert", handler=upsert_client_registration),
    ),
)

DeviceCodeTable = DeviceCode
DeviceCodeRuntimeSpec = deriveRuntimeTableSpec(
    DeviceCodeTable,
    operations=(
        makeRuntimeOperation(alias="approve", handler=approve_device_code),
        makeRuntimeOperation(alias="deny", handler=deny_device_code),
    ),
)

PushedAuthorizationRequestTable = PushedAuthorizationRequest
PushedAuthorizationRequestRuntimeSpec = deriveRuntimeTableSpec(
    PushedAuthorizationRequestTable,
    operations=(
        makeRuntimeOperation(
            alias="push_authorization_request",
            handler=persist_pushed_authorization_request,
        ),
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
    "DeviceCodeRuntimeSpec",
    "DeviceCodeTable",
    "PushedAuthorizationRequestRuntimeSpec",
    "PushedAuthorizationRequestTable",
    "RevokedTokenRuntimeSpec",
    "RevokedTokenTable",
]
