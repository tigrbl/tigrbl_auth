from typing import Mapping, Sequence

RELATIONSHIPS = frozenset({"authentication", "assertionMethod", "keyAgreement", "capabilityInvocation", "capabilityDelegation"})

def validate_did(value: str) -> None:
    if not value.startswith("did:") or value.count(":") < 2:
        raise ValueError("invalid DID syntax")
    method, method_specific_id = value[4:].split(":", 1)
    if not method or not method_specific_id or any(ch.isspace() for ch in value):
        raise ValueError("invalid DID syntax")

def validate_document(document: Mapping[str, object]) -> None:
    identifier = document.get("id")
    if not isinstance(identifier, str):
        raise ValueError("DID Document id is required")
    validate_did(identifier)
    controllers = document.get("controller", ())
    if isinstance(controllers, str):
        controllers = (controllers,)
    if not isinstance(controllers, Sequence):
        raise ValueError("controller must be a DID or sequence of DIDs")
    for controller in controllers:
        if not isinstance(controller, str):
            raise ValueError("controller must contain DIDs")
        validate_did(controller)
    methods = document.get("verificationMethod", ())
    known = {method.get("id") for method in methods if isinstance(method, Mapping)}
    for relationship in RELATIONSHIPS:
        for entry in document.get(relationship, ()):
            if isinstance(entry, str) and entry not in known:
                raise ValueError(f"unresolved verification relationship: {entry}")