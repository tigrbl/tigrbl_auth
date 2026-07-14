"""OAuth wire schemas owned by the versioned protocol package."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, EmailStr, Field, constr

from tigrbl_identity_core.typing import StrUUID


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = Field(default="bearer")
    id_token: str | None = None


class RefreshIn(BaseModel):
    refresh_token: str


class IntrospectOut(BaseModel):
    active: bool
    sub: StrUUID | None = None
    tid: StrUUID | None = None
    kind: str | None = None


class PasswordGrantForm(BaseModel):
    grant_type: Literal["password"]
    username: str
    password: str


class AuthorizationCodeGrantForm(BaseModel):
    grant_type: Literal["authorization_code"]
    code: str
    redirect_uri: str
    client_id: str
    code_verifier: str | None = None


_tenant_slug = constr(strip_whitespace=True, min_length=3, max_length=120)


class DynamicClientRegistrationIn(BaseModel):
    tenant_slug: _tenant_slug = Field(default="public")
    redirect_uris: list[str]
    grant_types: list[str] = Field(default_factory=lambda: ["authorization_code"])
    response_types: list[str] = Field(default_factory=lambda: ["code"])
    token_endpoint_auth_method: str = Field(default="client_secret_basic")
    token_endpoint_auth_signing_alg: str | None = None
    tls_client_certificate_thumbprint: str | None = None
    self_signed_tls_client_certificate_thumbprint: str | None = None
    tls_client_auth_subject_dn: str | None = None
    tls_client_auth_san_dns: str | None = None
    tls_client_auth_san_uri: str | None = None
    tls_client_auth_san_ip: str | None = None
    tls_client_auth_san_email: str | None = None
    application_type: str | None = None
    scope: str | None = None
    client_name: str | None = None
    client_uri: str | None = None
    jwks_uri: str | None = None
    contacts: list[EmailStr] | None = None
    software_id: str | None = None
    software_version: str | None = None
    post_logout_redirect_uris: list[str] | None = None
    frontchannel_logout_uri: str | None = None
    frontchannel_logout_session_required: bool = True
    backchannel_logout_uri: str | None = None
    backchannel_logout_session_required: bool = True


class DynamicClientRegistrationOut(BaseModel):
    client_id: str
    client_secret: str | None = None
    client_id_issued_at: int
    client_secret_expires_at: int = 0
    redirect_uris: list[str]
    grant_types: list[str]
    response_types: list[str]
    token_endpoint_auth_method: str
    token_endpoint_auth_signing_alg: str | None = None
    tls_client_certificate_thumbprint: str | None = None
    self_signed_tls_client_certificate_thumbprint: str | None = None
    tls_client_auth_subject_dn: str | None = None
    tls_client_auth_san_dns: str | None = None
    tls_client_auth_san_uri: str | None = None
    tls_client_auth_san_ip: str | None = None
    tls_client_auth_san_email: str | None = None
    application_type: str | None = None
    scope: str | None = None
    client_name: str | None = None
    client_uri: str | None = None
    jwks_uri: str | None = None
    contacts: list[EmailStr] | None = None
    software_id: str | None = None
    software_version: str | None = None
    post_logout_redirect_uris: list[str] | None = None
    frontchannel_logout_uri: str | None = None
    frontchannel_logout_session_required: bool = True
    backchannel_logout_uri: str | None = None
    backchannel_logout_session_required: bool = True
    registration_access_token: str | None = None
    registration_client_uri: str | None = None


class DynamicClientRegistrationManagementIn(BaseModel):
    tenant_slug: _tenant_slug | None = None
    redirect_uris: list[str] | None = None
    grant_types: list[str] | None = None
    response_types: list[str] | None = None
    token_endpoint_auth_method: str | None = None
    token_endpoint_auth_signing_alg: str | None = None
    tls_client_certificate_thumbprint: str | None = None
    self_signed_tls_client_certificate_thumbprint: str | None = None
    tls_client_auth_subject_dn: str | None = None
    tls_client_auth_san_dns: str | None = None
    tls_client_auth_san_uri: str | None = None
    tls_client_auth_san_ip: str | None = None
    tls_client_auth_san_email: str | None = None
    application_type: str | None = None
    scope: str | None = None
    client_name: str | None = None
    client_uri: str | None = None
    jwks_uri: str | None = None
    contacts: list[EmailStr] | None = None
    software_id: str | None = None
    software_version: str | None = None
    post_logout_redirect_uris: list[str] | None = None
    frontchannel_logout_uri: str | None = None
    frontchannel_logout_session_required: bool | None = None
    backchannel_logout_uri: str | None = None
    backchannel_logout_session_required: bool | None = None


class DeviceAuthorizationIn(BaseModel):
    client_id: str
    scope: str | None = None
    audience: str | None = None
    resource: list[str] | None = None


class DeviceAuthorizationOut(BaseModel):
    device_code: str
    user_code: str
    verification_uri: str
    verification_uri_complete: str
    expires_in: int
    interval: int


class PushedAuthorizationRequestIn(BaseModel):
    client_id: str
    request: str | None = None
    response_type: str | None = None
    redirect_uri: str | None = None
    scope: str | None = None
    state: str | None = None
    nonce: str | None = None
    code_challenge: str | None = None
    code_challenge_method: str | None = None
    resource: list[str] | None = None
    authorization_details: list[dict[str, Any]] | None = None


class PushedAuthorizationResponse(BaseModel):
    request_uri: str
    expires_in: int


class RevocationIn(BaseModel):
    token: str
    token_type_hint: str | None = None


class RevocationOut(BaseModel):
    revoked: bool = True


__all__ = [
    "AuthorizationCodeGrantForm",
    "DeviceAuthorizationIn",
    "DeviceAuthorizationOut",
    "DynamicClientRegistrationIn",
    "DynamicClientRegistrationManagementIn",
    "DynamicClientRegistrationOut",
    "IntrospectOut",
    "PasswordGrantForm",
    "PushedAuthorizationRequestIn",
    "PushedAuthorizationResponse",
    "RefreshIn",
    "RevocationIn",
    "RevocationOut",
    "TokenPair",
]
