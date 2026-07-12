"""Minimal structural validation for W3C Verifiable Credentials Data Model 2.0."""

from __future__ import annotations

from typing import Any, Mapping

VC_CONTEXT_V2 = "https://www.w3.org/ns/credentials/v2"


def validate_verifiable_credential(value: Mapping[str, Any]) -> None:
    contexts = value.get("@context")
    types = value.get("type")
    if not isinstance(contexts, list) or not contexts or contexts[0] != VC_CONTEXT_V2:
        raise ValueError("VCDM 2.0 credential must use the v2 base context first")
    if not isinstance(types, list) or "VerifiableCredential" not in types:
        raise ValueError("credential type must include VerifiableCredential")
    if "issuer" not in value or not isinstance(value.get("credentialSubject"), (dict, list)):
        raise ValueError("credential requires issuer and credentialSubject")


def validate_verifiable_presentation(value: Mapping[str, Any]) -> None:
    contexts = value.get("@context")
    types = value.get("type")
    if not isinstance(contexts, list) or not contexts or contexts[0] != VC_CONTEXT_V2:
        raise ValueError("VCDM 2.0 presentation must use the v2 base context first")
    if not isinstance(types, list) or "VerifiablePresentation" not in types:
        raise ValueError("presentation type must include VerifiablePresentation")


__all__ = ["VC_CONTEXT_V2", "validate_verifiable_credential", "validate_verifiable_presentation"]
