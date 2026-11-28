from collections.abc import Mapping, Sequence

RELATIONSHIPS = frozenset(
    {
        "authentication",
        "assertionMethod",
        "keyAgreement",
        "capabilityInvocation",
        "capabilityDelegation",
    }
)
_KEY_MATERIAL_MEMBERS = frozenset({"publicKeyJwk", "publicKeyMultibase"})


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
    if not isinstance(methods, Sequence) or isinstance(methods, (str, bytes)):
        raise ValueError("verificationMethod must be an array")
    known: set[str] = set()
    for method in methods:
        if not isinstance(method, Mapping):
            raise ValueError("verificationMethod entries must be objects")
        method_id = method.get("id")
        method_controller = method.get("controller")
        method_type = method.get("type")
        if not all(
            isinstance(value, str) and value
            for value in (method_id, method_controller, method_type)
        ):
            raise ValueError("verificationMethod requires id, controller, and type")
        validate_did(method_controller)
        key_members = _KEY_MATERIAL_MEMBERS.intersection(method)
        if len(key_members) != 1:
            raise ValueError(
                "verificationMethod requires exactly one public key representation"
            )
        known.add(method_id)

    for relationship in RELATIONSHIPS:
        entries = document.get(relationship, ())
        if not isinstance(entries, Sequence) or isinstance(entries, (str, bytes)):
            raise ValueError(f"{relationship} must be an array")
        for entry in entries:
            if isinstance(entry, str) and entry not in known:
                raise ValueError(f"unresolved verification relationship: {entry}")
            if not isinstance(entry, (str, Mapping)):
                raise ValueError(f"invalid {relationship} entry")
