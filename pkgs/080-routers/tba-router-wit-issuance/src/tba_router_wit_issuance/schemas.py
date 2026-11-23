from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

JwkString = Annotated[str, StringConstraints(max_length=2048)]
JwkOperations = Annotated[list[JwkString], Field(max_length=16)]


class WitIssueRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    confirmation_jwk: dict[JwkString, JwkString | JwkOperations] = Field(
        min_length=1, max_length=16
    )


class WitIssueResponse(BaseModel):
    workload_identity_token: str
