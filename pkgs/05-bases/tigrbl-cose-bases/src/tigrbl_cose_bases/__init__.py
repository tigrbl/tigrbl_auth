"""Protocol-neutral extension bases for CBOR, COSE, and CWT envelopes."""

from abc import ABC
from typing import Mapping

from tigrbl_identity_contracts.tokens import ProtectedTokenEnvelope, VerifiedTokenEnvelope
from tigrbl_token_bases import EatTokenEnvelopeVerifierBase


class CborCodecBase(ABC):
    def encode(self, value: object, /) -> bytes:
        raise NotImplementedError

    def decode(self, value: bytes, /) -> object:
        raise NotImplementedError


class CoseVerifierBase(ABC):
    def verify_cose(self, value: bytes, /) -> Mapping[str | int, object]:
        raise NotImplementedError


class CwtCoderBase(ABC):
    def encode_claims(self, claims: Mapping[str | int, object], /) -> bytes:
        raise NotImplementedError

    def decode_claims(self, token: bytes, /) -> Mapping[str | int, object]:
        raise NotImplementedError


class EatCwtVerifierBase(EatTokenEnvelopeVerifierBase):
    """Verify an RFC 9711 EAT carried in a CWT/COSE envelope."""

    def verify_envelope(self, envelope: ProtectedTokenEnvelope, /) -> VerifiedTokenEnvelope:
        raise NotImplementedError


__all__ = ["CborCodecBase", "CoseVerifierBase", "CwtCoderBase", "EatCwtVerifierBase"]
