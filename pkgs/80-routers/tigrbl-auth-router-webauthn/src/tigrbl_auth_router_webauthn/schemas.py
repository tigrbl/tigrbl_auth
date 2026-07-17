"""WebAuthn application/JSON carrier envelopes."""

from pydantic import BaseModel, ConfigDict, Field


class RegistrationOptionsIn(BaseModel):
    user_name: str = Field(min_length=1, max_length=320)
    display_name: str = Field(min_length=1, max_length=320)


class AuthenticationOptionsIn(BaseModel):
    user_name: str | None = Field(default=None, max_length=320)
    conditional: bool = False


class CredentialResponseIn(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    client_data_json: str = Field(alias="clientDataJSON")
    attestation_object: str | None = Field(default=None, alias="attestationObject")
    authenticator_data: str | None = Field(default=None, alias="authenticatorData")
    signature: str | None = None
    user_handle: str | None = Field(default=None, alias="userHandle")
    transports: tuple[str, ...] = ()


class PublicKeyCredentialIn(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str
    raw_id: str = Field(alias="rawId")
    type: str = "public-key"
    response: CredentialResponseIn
    authenticator_attachment: str | None = Field(
        default=None, alias="authenticatorAttachment"
    )
    client_extension_results: dict[str, object] = Field(
        default_factory=dict, alias="clientExtensionResults"
    )


class RenameCredentialIn(BaseModel):
    display_name: str = Field(min_length=1, max_length=120)


__all__ = [
    "AuthenticationOptionsIn",
    "CredentialResponseIn",
    "PublicKeyCredentialIn",
    "RegistrationOptionsIn",
    "RenameCredentialIn",
]
