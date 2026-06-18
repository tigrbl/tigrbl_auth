from __future__ import annotations

from typing import Any, Literal, Optional

from tigrbl_identity_server.framework import BaseModel, EmailStr, Field, constr

from tigrbl_identity_core.typing import StrUUID

_password = constr(min_length=8, max_length=256)
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


class CredsIn(BaseModel):
    identifier: constr(strip_whitespace=True, min_length=3, max_length=120)
    password: _password


class TokenPair(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = Field(default="bearer")
    id_token: Optional[str] = None


class RefreshIn(BaseModel):
    refresh_token: str


class LogoutIn(BaseModel):
    id_token_hint: str | None = None
    post_logout_redirect_uri: str | None = None
    state: str | None = None
    sid: str | None = None
    client_id: str | None = None


class LogoutOut(BaseModel):
    status: str
    session_id: str | None = None
    logout_id: str | None = None
    post_logout_redirect_uri: str | None = None
    state: str | None = None
    cookie_cleared: bool = True
    cookie_policy: dict[str, Any] | None = None
    frontchannel_logout: dict[str, Any] | None = None
    backchannel_logout: dict[str, Any] | None = None
    replay_protected: bool = True


class RevocationIn(BaseModel):
    token: str
    token_type_hint: str | None = None


class RevocationOut(BaseModel):
    revoked: bool = True


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


class IntrospectOut(BaseModel):
    active: bool
    sub: Optional[StrUUID] = None
    tid: Optional[StrUUID] = None
    kind: Optional[str] = None


class PasswordGrantForm(BaseModel):
    grant_type: Literal["password"]
    username: str
    password: str


class AuthorizationCodeGrantForm(BaseModel):
    grant_type: Literal["authorization_code"]
    code: str
    redirect_uri: str
    client_id: str
    code_verifier: Optional[str] = None


class AdminPasswordResetRequestIn(BaseModel):
    identifier: constr(strip_whitespace=True, min_length=3, max_length=120)


class AdminPasswordResetCompleteIn(BaseModel):
    token: constr(strip_whitespace=True, min_length=16, max_length=256)
    password: _password


class AdminPasswordChangeIn(BaseModel):
    current_password: _password
    new_password: _password


class AdminSessionOut(BaseModel):
    authenticated: bool
    session_id: str | None = None
    user_id: str | None = None
    tenant_id: str | None = None
    username: str | None = None
    email: str | None = None
    is_admin: bool = False
    is_superuser: bool = False
    must_change_password: bool = False
    roles: list[str] = Field(default_factory=list)
    debug_reset_token: str | None = None
