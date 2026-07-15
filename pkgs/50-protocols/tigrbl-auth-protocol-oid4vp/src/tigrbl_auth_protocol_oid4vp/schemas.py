"""Typed OID4VP wire-schema projections."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Oid4vpAuthorizationRequest:
    client_id: str
    nonce: str
    accepted_formats: tuple[str, ...]
    state: str | None = None


@dataclass(frozen=True, slots=True)
class Oid4vpDirectPostResponse:
    vp_token: str | bytes
    state: str | None = None


__all__ = ["Oid4vpAuthorizationRequest", "Oid4vpDirectPostResponse"]
