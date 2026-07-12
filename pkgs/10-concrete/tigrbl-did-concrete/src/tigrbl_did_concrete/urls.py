from urllib.parse import parse_qsl

from tigrbl_identity_contracts.did import DidUrl

from .identifiers import parse_did


def parse_did_url(value: str) -> DidUrl:
    fragment = value.partition("#")[2] if "#" in value else ""
    without_fragment = value.partition("#")[0]
    query = without_fragment.partition("?")[2] if "?" in without_fragment else ""
    without_query = without_fragment.partition("?")[0]
    did_text, separator, path = without_query.partition("/")
    did = parse_did(did_text)
    if query:
        parse_qsl(query, strict_parsing=True)
    return DidUrl(did, f"/{path}" if separator else "", query, fragment)


__all__ = ["parse_did_url"]
