from tigrbl_identity_contracts.did import DidDocument, DidUrl


def select_document_resource(document: DidDocument, did_url: DidUrl):
    if did_url.did != document.identifier:
        raise ValueError("DID URL does not identify this document")
    identifier = str(did_url.did) + (f"#{did_url.fragment}" if did_url.fragment else "")
    for resource in (*document.verification_methods, *document.services):
        candidate = resource.identifier
        if candidate.startswith("#"):
            candidate = f"{document.identifier}{candidate}"
        if candidate == identifier:
            return resource
    raise LookupError(identifier)


__all__ = ["select_document_resource"]
