import re

from tigrbl_identity_contracts.did import Did

_METHOD = re.compile(r"^[a-z0-9]+$")


def parse_did(value: str) -> Did:
    did = Did.parse(value)
    if not _METHOD.fullmatch(did.method):
        raise ValueError("DID method must contain lowercase letters and digits")
    if any(character.isspace() for character in did.method_specific_id):
        raise ValueError("DID method-specific identifier cannot contain whitespace")
    return did


__all__ = ["parse_did"]
