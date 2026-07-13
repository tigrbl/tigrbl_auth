"""Wire-level structural contracts for OID4VCI 1.0 and OID4VP 1.0."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence


@dataclass(frozen=True, slots=True)
class CredentialOffer:
    credential_issuer: str
    credential_configuration_ids: tuple[str, ...]
    grants: Mapping[str, Any]


def parse_credential_offer(value: Mapping[str, Any]) -> CredentialOffer:
    issuer = value.get("credential_issuer")
    ids = value.get("credential_configuration_ids")
    grants = value.get("grants", {})
    if not isinstance(issuer, str) or not issuer.startswith("https://"):
        raise ValueError("credential_issuer must be an HTTPS URL")
    if (
        not isinstance(ids, list)
        or not ids
        or not all(isinstance(i, str) and i for i in ids)
    ):
        raise ValueError(
            "credential_configuration_ids must be a non-empty string array"
        )
    if not isinstance(grants, Mapping):
        raise ValueError("grants must be an object")
    return CredentialOffer(issuer, tuple(ids), dict(grants))


@dataclass(frozen=True, slots=True)
class PresentationRequest:
    client_id: str
    nonce: str
    response_type: str
    response_mode: str | None
    dcql_query: Mapping[str, Any] | None


def parse_presentation_request(value: Mapping[str, Any]) -> PresentationRequest:
    client_id, nonce = value.get("client_id"), value.get("nonce")
    if (
        not isinstance(client_id, str)
        or not client_id
        or not isinstance(nonce, str)
        or not nonce
    ):
        raise ValueError("OID4VP request requires client_id and nonce")
    if value.get("response_type") != "vp_token":
        raise ValueError("OID4VP response_type must be vp_token")
    query = value.get("dcql_query")
    if query is not None and not isinstance(query, Mapping):
        raise ValueError("dcql_query must be an object")
    return PresentationRequest(
        client_id, nonce, "vp_token", value.get("response_mode"), query
    )


@dataclass(frozen=True, slots=True)
class HaipPolicy:
    credential_formats: Sequence[str] = ("dc+sd-jwt", "mso_mdoc")
    require_signed_request: bool = True
    require_encrypted_response: bool = True
    require_key_binding: bool = True

    def accepts_format(self, value: str) -> bool:
        return value in self.credential_formats


__all__ = [
    "CredentialOffer",
    "HaipPolicy",
    "PresentationRequest",
    "parse_credential_offer",
    "parse_presentation_request",
]
