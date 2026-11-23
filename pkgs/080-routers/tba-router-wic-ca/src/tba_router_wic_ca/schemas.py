from pydantic import BaseModel, ConfigDict, Field


class WicIssueRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    csr_pem: str = Field(min_length=1, max_length=16384)


class WicIssueResponse(BaseModel):
    certificate_pem: str
