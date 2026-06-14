from __future__ import annotations

from typing import Any, Literal, Optional

from tigrbl_identity_server.framework import BaseModel, EmailStr, Field, constr

from tigrbl_identity_core.typing import StrUUID

_username = constr(strip_whitespace=True, min_length=3, max_length=80)
_password = constr(min_length=8, max_length=256)
_tenant_slug = constr(strip_whitespace=True, min_length=3, max_length=120)
_realm_slug = constr(strip_whitespace=True, min_length=3, max_length=120)


class RegisterIn(BaseModel):
    tenant_slug: _tenant_slug
    username: _username
    email: EmailStr
    password: _password


class DynamicClientRegistrationIn(BaseModel):
    tenant_slug: _tenant_slug = Field(default="public")
    redirect_uris: list[str]
    grant_types: list[str] = Field(default_factory=lambda: ["authorization_code"])
    response_types: list[str] = Field(default_factory=lambda: ["code"])
    token_endpoint_auth_method: str = Field(default="client_secret_basic")
    token_endpoint_auth_signing_alg: str | None = None
    tls_client_certificate_thumbprint: str | None = None
    self_signed_tls_client_certificate_thumbprint: str | None = None
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


class AdminIdentityOut(BaseModel):
    id: str
    tenant_id: str
    username: str
    email: str
    is_active: bool = True
    is_admin: bool = False
    is_superuser: bool = False
    must_change_password: bool = False
    roles: list[str] = Field(default_factory=list)
    created_at: str | None = None
    updated_at: str | None = None


class AdminIdentityProvisionIn(BaseModel):
    tenant_id: str
    username: _username
    email: constr(strip_whitespace=True, min_length=3, max_length=120)
    password: _password
    is_admin: bool = False
    is_superuser: bool = False
    must_change_password: bool = True


class AdminIdentityUpdateIn(BaseModel):
    username: _username | None = None
    email: constr(strip_whitespace=True, min_length=3, max_length=120) | None = None
    password: _password | None = None
    is_active: bool | None = None
    is_admin: bool | None = None
    is_superuser: bool | None = None
    must_change_password: bool | None = None


class AdminTenantOut(BaseModel):
    id: str
    realm_id: str | None = None
    slug: _tenant_slug
    name: constr(strip_whitespace=True, min_length=1, max_length=120)
    email: constr(strip_whitespace=True, min_length=3, max_length=120)
    created_at: str | None = None
    updated_at: str | None = None


class AdminTenantProvisionIn(BaseModel):
    realm_id: str | None = None
    slug: _tenant_slug
    name: constr(strip_whitespace=True, min_length=1, max_length=120)
    email: constr(strip_whitespace=True, min_length=3, max_length=120)


class AdminTenantUpdateIn(BaseModel):
    realm_id: str | None = None
    slug: _tenant_slug | None = None
    name: constr(strip_whitespace=True, min_length=1, max_length=120) | None = None
    email: constr(strip_whitespace=True, min_length=3, max_length=120) | None = None
    is_active: bool | None = None


class AdminRealmOut(BaseModel):
    id: str
    slug: _realm_slug
    name: constr(strip_whitespace=True, min_length=1, max_length=120)
    issuer_path: str = ""
    description: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


class AdminRealmProvisionIn(BaseModel):
    slug: _realm_slug
    name: constr(strip_whitespace=True, min_length=1, max_length=120)
    issuer_path: str | None = None
    description: constr(strip_whitespace=True, max_length=255) | None = None


class AdminRealmUpdateIn(BaseModel):
    slug: _realm_slug | None = None
    name: constr(strip_whitespace=True, min_length=1, max_length=120) | None = None
    issuer_path: str | None = None
    description: constr(strip_whitespace=True, max_length=255) | None = None


class MyAccountProfileOut(BaseModel):
    id: str
    tenant_id: str
    username: str
    email: str
    is_active: bool = True
    must_change_password: bool = False
    roles: list[str] = Field(default_factory=list)
    created_at: str | None = None
    updated_at: str | None = None


class MyAccountProfileUpdateIn(BaseModel):
    username: _username | None = None
    email: constr(strip_whitespace=True, min_length=3, max_length=120) | None = None


class MyAccountSessionOut(BaseModel):
    id: str
    tenant_id: str
    user_id: str
    username: str
    client_id: str | None = None
    state: str = "active"
    auth_time: str | None = None
    last_seen_at: str | None = None
    expires_at: str | None = None
    ended_at: str | None = None


class MyAccountConsentOut(BaseModel):
    id: str
    tenant_id: str
    user_id: str
    client_id: str
    scope: str
    claims: dict[str, Any] | None = None
    state: str = "active"
    granted_at: str | None = None
    expires_at: str | None = None
    revoked_at: str | None = None


class MyAccountAuthorizedAppOut(BaseModel):
    client_id: str
    tenant_id: str
    scope: str
    consent_state: str = "active"
    granted_at: str | None = None
    revoked_at: str | None = None


class MyAccountPasswordChangeIn(BaseModel):
    current_password: _password
    new_password: _password


class MyAccountMutationOut(BaseModel):
    status: str
    id: str | None = None
