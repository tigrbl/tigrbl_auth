from collections.abc import Mapping

from tigrbl_identity_contracts.did import (
    DidDocument,
    DidService,
    DidVerificationMethod,
    VerificationRelationship,
)

from .identifiers import parse_did


def parse_did_document(value: Mapping[str, object]) -> DidDocument:
    identifier = value.get("id")
    if not isinstance(identifier, str):
        raise ValueError("DID document requires id")
    did = parse_did(identifier)
    methods = []
    for item in value.get("verificationMethod", ()):
        if not isinstance(item, Mapping) or not all(
            isinstance(item.get(name), str) for name in ("id", "type", "controller")
        ):
            raise ValueError("invalid DID verification method")
        key_members = [
            name for name in ("publicKeyJwk", "publicKeyMultibase") if name in item
        ]
        if len(key_members) != 1:
            raise ValueError(
                "verification method requires exactly one public key representation"
            )
        key_value = item[key_members[0]]
        key = (
            dict(key_value)
            if isinstance(key_value, Mapping)
            else {"publicKeyMultibase": key_value}
        )
        methods.append(
            DidVerificationMethod(
                item["id"], parse_did(item["controller"]), item["type"], key
            )
        )
    services = []
    for item in value.get("service", ()):
        if (
            not isinstance(item, Mapping)
            or not isinstance(item.get("id"), str)
            or "serviceEndpoint" not in item
        ):
            raise ValueError("invalid DID service")
        types = item.get("type")
        types = (types,) if isinstance(types, str) else tuple(types or ())
        services.append(DidService(item["id"], types, item["serviceEndpoint"]))
    relationships = {}
    for relationship in VerificationRelationship:
        if relationship.value in value:
            members = value[relationship.value]
            if not isinstance(members, list) or not all(
                isinstance(member, str) for member in members
            ):
                raise ValueError(
                    f"{relationship.value} must be an array of method references"
                )
            relationships[relationship] = tuple(members)
    return DidDocument(did, tuple(methods), relationships, tuple(services))


__all__ = ["parse_did_document"]
