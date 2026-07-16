from abc import ABC

from tigrbl_security_trust_contracts import (
    Artifact,
    CanonicalizeRequest,
    IArtifactCodec,
    IArtifactIssuer,
    IArtifactOpener,
    IArtifactVerifier,
    IRecipientSetEditor,
    IssueRequest,
    OpenRequest,
    OpenResult,
    ParsedArtifact,
    ParseRequest,
    RewrapRequest,
    VerificationResult,
    VerifyRequest,
)


class SecurityArtifactCodecBase(IArtifactCodec, ABC):
    async def parse(self, request: ParseRequest) -> ParsedArtifact:
        raise NotImplementedError

    async def canonicalize(self, request: CanonicalizeRequest) -> bytes:
        raise NotImplementedError


class SecurityArtifactIssuerBase(IArtifactIssuer, ABC):
    async def issue(self, request: IssueRequest) -> Artifact:
        raise NotImplementedError


class ProtectedArtifactVerifierBase(IArtifactVerifier, ABC):
    async def verify(self, request: VerifyRequest) -> VerificationResult:
        raise NotImplementedError


class ProtectedArtifactOpenerBase(IArtifactOpener, ABC):
    async def open(self, request: OpenRequest) -> OpenResult:
        raise NotImplementedError


class RecipientSetEditorBase(IRecipientSetEditor, ABC):
    async def rewrap(self, request: RewrapRequest) -> Artifact:
        raise NotImplementedError


__all__ = [
    "ProtectedArtifactOpenerBase",
    "ProtectedArtifactVerifierBase",
    "RecipientSetEditorBase",
    "SecurityArtifactCodecBase",
    "SecurityArtifactIssuerBase",
]
