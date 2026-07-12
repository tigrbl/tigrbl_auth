from dataclasses import dataclass
from typing import Mapping

from tigrbl_identity_contracts.attestation import ReferenceIntegrityManifest

from .comid import ComidTag, parse_comid
from .coswid import CoswidTag, parse_coswid
from .cotl import ConciseTrustList, parse_cotl
from .cots import ConciseTrustStore, parse_cots

CORIM_REVISION = "draft-ietf-rats-corim-11"


@dataclass(frozen=True, slots=True)
class CorimTag:
    tag_identity: str | bytes
    tags: tuple[ComidTag | CoswidTag | ConciseTrustList | ConciseTrustStore, ...]
    signer: str | None = None


def _parse_tag(value: Mapping[str, object]):
    tag_type = value.get("tag-type")
    if tag_type == "comid" or "triples" in value:
        return parse_comid(value)
    if tag_type == "coswid" or "software-name" in value:
        return parse_coswid(value)
    if tag_type == "cotl" or "trust-list" in value:
        return parse_cotl(value)
    if tag_type == "cots" or "trust-store" in value:
        return parse_cots(value)
    raise ValueError("unknown CoRIM tag type")


def parse_corim_tag(value: Mapping[str, object]) -> CorimTag:
    identity, tags = value.get("tag-identity"), value.get("tags", value.get("comids"))
    if not isinstance(identity, (str, bytes)) or not identity:
        raise ValueError("CoRIM requires tag-identity")
    if (
        not isinstance(tags, list)
        or not tags
        or not all(isinstance(item, Mapping) for item in tags)
    ):
        raise ValueError("CoRIM requires a non-empty tags array")
    signer = value.get("signer")
    if signer is not None and not isinstance(signer, str):
        raise ValueError("CoRIM signer must be a string")
    return CorimTag(identity, tuple(_parse_tag(item) for item in tags), signer)


def parse_corim(value: Mapping[str, object]) -> ReferenceIntegrityManifest:
    parsed = parse_corim_tag(value)
    manifests = tuple(dict(item) for item in value.get("tags", value.get("comids", ())))
    return ReferenceIntegrityManifest(
        str(parsed.tag_identity), manifests, parsed.signer
    )


__all__ = ["CORIM_REVISION", "CorimTag", "parse_corim", "parse_corim_tag"]
