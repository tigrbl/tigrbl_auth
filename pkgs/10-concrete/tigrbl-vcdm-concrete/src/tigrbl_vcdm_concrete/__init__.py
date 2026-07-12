from typing import Any, Mapping

VC_CONTEXT_V2 = "https://www.w3.org/ns/credentials/v2"


def _validate(value: Mapping[str, Any], expected: str) -> None:
    contexts = value.get("@context")
    types = value.get("type")
    if not isinstance(contexts, list) or not contexts or contexts[0] != VC_CONTEXT_V2:
        raise ValueError("VCDM 2.0 object must use the v2 base context first")
    if not isinstance(types, list) or expected not in types:
        raise ValueError(f"type must include {expected}")


def validate_verifiable_credential(value: Mapping[str, Any]) -> None:
    _validate(value, "VerifiableCredential")
    if "issuer" not in value or not isinstance(
        value.get("credentialSubject"), (dict, list)
    ):
        raise ValueError("credential requires issuer and credentialSubject")


def validate_verifiable_presentation(value: Mapping[str, Any]) -> None:
    _validate(value, "VerifiablePresentation")


__all__ = [
    "VC_CONTEXT_V2",
    "validate_verifiable_credential",
    "validate_verifiable_presentation",
]
