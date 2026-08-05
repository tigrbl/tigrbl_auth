"""Owned mapped-table inventory."""

from .auth_code import AuthCode
from .auth_session import AuthSession
from .authorization_server import AuthorizationServer
from .client import Client
from .client_registration import ClientRegistration
from .device_code import DeviceCode
from .pushed_authorization_request import PushedAuthorizationRequest
from .revoked_token import RevokedToken

TABLE_MODELS = (
    Client,
    ClientRegistration,
    AuthorizationServer,
    AuthSession,
    AuthCode,
    DeviceCode,
    RevokedToken,
    PushedAuthorizationRequest,
)
TABLE_MODEL_BY_NAME = {model.__name__: model for model in TABLE_MODELS}
TABLE_MODEL_BY_TABLENAME = {model.__tablename__: model for model in TABLE_MODELS}
__all__ = [model.__name__ for model in TABLE_MODELS] + [
    "TABLE_MODELS", "TABLE_MODEL_BY_NAME", "TABLE_MODEL_BY_TABLENAME",
]
