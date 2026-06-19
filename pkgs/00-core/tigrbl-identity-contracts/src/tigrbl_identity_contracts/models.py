from __future__ import annotations

"""First-class public wire contract models for identity consumers."""

from typing import Any, Literal

from pydantic import AnyUrl, BaseModel, ConfigDict, Field


class ContractModel(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class OAuthTokenRequest(ContractModel):
    grant_type: str
    client_id: str | None = None
    client_secret: str | None = None
    code: str | None = None
    code_verifier: str | None = None
    redirect_uri: str | None = None
    refresh_token: str | None = None
    scope: str | None = None
    resource: list[str] = Field(default_factory=list)
    audience: str | None = None


class OAuthTokenResponse(ContractModel):
    access_token: str
    token_type: Literal["Bearer", "bearer"] = "Bearer"
    expires_in: int | None = None
    refresh_token: str | None = None
    id_token: str | None = None
    scope: str | None = None


class OAuthIntrospectionResponse(ContractModel):
    active: bool
    sub: str | None = None
    client_id: str | None = None
    scope: str | None = None
    iss: str | None = None
    aud: str | list[str] | None = None
    exp: int | None = None
    iat: int | None = None


class OidcDiscoveryDocument(ContractModel):
    issuer: AnyUrl
    authorization_endpoint: AnyUrl | None = None
    token_endpoint: AnyUrl | None = None
    jwks_uri: AnyUrl
    userinfo_endpoint: AnyUrl | None = None
    end_session_endpoint: AnyUrl | None = None
    response_types_supported: list[str] = Field(default_factory=lambda: ["code"])
    subject_types_supported: list[str] = Field(default_factory=lambda: ["public"])
    id_token_signing_alg_values_supported: list[str] = Field(default_factory=list)
    scopes_supported: list[str] = Field(default_factory=list)
    claims_supported: list[str] = Field(default_factory=list)


class OidcIdTokenClaims(ContractModel):
    iss: str
    sub: str
    aud: str | list[str]
    exp: int
    iat: int
    auth_time: int | None = None
    nonce: str | None = None
    azp: str | None = None
    sid: str | None = None


class ResourceServerMetadata(ContractModel):
    resource: str
    issuer: str
    jwks_uri: str | None = None
    introspection_endpoint: str | None = None
    scopes_supported: list[str] = Field(default_factory=list)
    bearer_methods_supported: list[str] = Field(default_factory=lambda: ["header"])


class AccessTokenClaims(ContractModel):
    iss: str
    sub: str
    aud: str | list[str]
    exp: int
    iat: int | None = None
    scope: str | None = None
    client_id: str | None = None
    cnf: dict[str, Any] | None = None


class RpConfiguration(ContractModel):
    issuer: str
    client_id: str
    redirect_uri: str
    scopes: list[str] = Field(default_factory=lambda: ["openid"])
    client_secret: str | None = None
    post_logout_redirect_uri: str | None = None


class RpLoginRequest(ContractModel):
    state: str
    nonce: str
    code_challenge: str
    code_challenge_method: Literal["S256"] = "S256"
    redirect_uri: str
    scope: str = "openid"


class ContractProjection(ContractModel):
    kind: Literal["openapi"]
    profile: str
    version: str
    document: dict[str, Any]


__all__ = [
    "AccessTokenClaims",
    "ContractModel",
    "ContractProjection",
    "OAuthIntrospectionResponse",
    "OAuthTokenRequest",
    "OAuthTokenResponse",
    "OidcDiscoveryDocument",
    "OidcIdTokenClaims",
    "ResourceServerMetadata",
    "RpConfiguration",
    "RpLoginRequest",
]
