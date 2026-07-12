from typing import Any, Mapping
from tigrbl_identity_contracts.attestation import ReferenceIntegrityManifest

CORIM_REVISION = "draft-ietf-rats-corim-08"


def parse_corim(value: Mapping[str, Any]) -> ReferenceIntegrityManifest:
    tag_identity = value.get("tag-identity")
    manifests = value.get("comids")
    if not isinstance(tag_identity, (str, bytes)):
        raise ValueError("CoRIM requires tag-identity")
    if not isinstance(manifests, list) or not all(
        isinstance(item, Mapping) for item in manifests
    ):
        raise ValueError("CoRIM requires a comids array")
    return ReferenceIntegrityManifest(
        str(tag_identity), tuple(dict(item) for item in manifests), value.get("signer")
    )


__all__ = ["CORIM_REVISION", "parse_corim"]
