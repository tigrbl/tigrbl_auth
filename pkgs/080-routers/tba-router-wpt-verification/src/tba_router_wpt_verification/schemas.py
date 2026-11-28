"""Bounded request values for an authenticated verification delegation."""

from pydantic import BaseModel, ConfigDict, Field


class TokenHeader(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    name: str = Field(min_length=1, max_length=128, pattern=r"^[A-Za-z][A-Za-z0-9-]*$")
    value: str = Field(min_length=1, max_length=16384, pattern=r"^[\x21-\x7e]+$")


class WptVerificationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    workload_identity_token: str = Field(min_length=1, max_length=16384)
    workload_proof_token: str = Field(min_length=1, max_length=16384)
    token_headers: list[TokenHeader] = Field(default_factory=list, max_length=32)


class WptVerificationResponse(BaseModel):
    valid: bool
    subject: str
    audience: str
    proof_id: str
    expires_at: float
