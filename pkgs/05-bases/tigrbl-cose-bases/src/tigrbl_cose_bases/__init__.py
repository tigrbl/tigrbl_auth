"""Protocol-neutral extension bases for CBOR, COSE, and CWT envelopes."""

from abc import ABC
from typing import Mapping

from tigrbl_protected_envelope_bases import (
    ProtectedEnvelopeIssuerBase,
    ProtectedEnvelopeVerifierBase,
)
from tigrbl_token_bases import (
    EatTokenEnvelopeVerifierBase,
    ProfiledTokenIssuerBase,
    ProfiledTokenVerifierBase,
)
from tigrbl_token_contracts import ProtectedTokenEnvelope, VerifiedTokenEnvelope


class CborCodecBase(ABC):
    def encode(self, value: object, /) -> bytes:
        raise NotImplementedError

    def decode(self, value: bytes, /) -> object:
        raise NotImplementedError


class CoseEnvelopeIssuerBase(ProtectedEnvelopeIssuerBase):
    """Issue a protected envelope constrained to a COSE structure kind."""


class CoseEnvelopeVerifierBase(ProtectedEnvelopeVerifierBase):
    """Verify a protected envelope constrained to a COSE structure kind."""


class CoseVerifierBase(ABC):
    """Compatibility base for existing raw COSE verifiers."""

    def verify_cose(self, value: bytes, /) -> Mapping[str | int, object]:
        raise NotImplementedError


class CwtCoderBase(ABC):
    def encode_claims(self, claims: Mapping[str | int, object], /) -> bytes:
        raise NotImplementedError

    def decode_claims(self, token: bytes, /) -> Mapping[str | int, object]:
        raise NotImplementedError


class CwtTokenIssuerBase(ProfiledTokenIssuerBase):
    """Issue tokens constrained to a CWT profile and COSE protection."""


class CwtTokenVerifierBase(ProfiledTokenVerifierBase):
    """Verify tokens constrained to a CWT profile and COSE protection."""


class EatCwtVerifierBase(EatTokenEnvelopeVerifierBase):
    """Verify an RFC 9711 EAT carried in a CWT/COSE envelope."""

    def verify_envelope(
        self,
        envelope: ProtectedTokenEnvelope,
        /,
    ) -> VerifiedTokenEnvelope:
        raise NotImplementedError


__all__ = [
    "CborCodecBase",
    "CoseEnvelopeIssuerBase",
    "CoseEnvelopeVerifierBase",
    "CoseVerifierBase",
    "CwtCoderBase",
    "CwtTokenIssuerBase",
    "CwtTokenVerifierBase",
    "EatCwtVerifierBase",
]