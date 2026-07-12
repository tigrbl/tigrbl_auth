from tigrbl_identity_contracts.did import DidDocument


def validate_did_document(document: DidDocument) -> None:
    method_ids = [method.identifier for method in document.verification_methods]
    if len(method_ids) != len(set(method_ids)):
        raise ValueError("DID verification method identifiers must be unique")
    prefix = f"{document.identifier}#"
    if any(not identifier.startswith(prefix) for identifier in method_ids):
        raise ValueError(
            "embedded verification methods must be controlled by document-local identifiers"
        )
    references = {
        reference
        for values in (document.relationships or {}).values()
        for reference in values
    }
    missing = references - set(method_ids)
    if missing:
        raise ValueError(
            f"verification relationships reference unknown methods: {sorted(missing)}"
        )
    service_ids = [service.identifier for service in document.services]
    if len(service_ids) != len(set(service_ids)):
        raise ValueError("DID service identifiers must be unique")


__all__ = ["validate_did_document"]
