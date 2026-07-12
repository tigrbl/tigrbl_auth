"""Structural EAT and CoRIM/CoMID models over already-decoded CBOR claims."""

from __future__ import annotations

from typing import Any, Mapping

from tigrbl_identity_contracts.attestation import AttestationEvidence, ReferenceIntegrityManifest

EAT_PROFILE_CLAIM = 265
EAT_NONCE_CLAIM = 10


def parse_eat(claims: Mapping[str | int, Any]) -> AttestationEvidence:
    profile = claims.get(EAT_PROFILE_CLAIM, claims.get("eat_profile"))
    if not isinstance(profile, (str, int)):
        raise ValueError("EAT requires an eat_profile claim")
    nonce = claims.get(EAT_NONCE_CLAIM, claims.get("nonce"))
    if nonce is not None and not isinstance(nonce, (bytes, str, list)):
        raise ValueError("EAT nonce has an invalid representation")
    return AttestationEvidence(str(profile), dict(claims))


def parse_corim(value: Mapping[str, Any]) -> ReferenceIntegrityManifest:
    tag_identity = value.get("tag-identity")
    manifests = value.get("comids")
    if not isinstance(tag_identity, (str, bytes)):
        raise ValueError("CoRIM requires tag-identity")
    if not isinstance(manifests, list) or not all(isinstance(item, Mapping) for item in manifests):
        raise ValueError("CoRIM requires a comids array")
    return ReferenceIntegrityManifest(str(tag_identity), tuple(dict(item) for item in manifests), value.get("signer"))


__all__ = ["EAT_NONCE_CLAIM", "EAT_PROFILE_CLAIM", "parse_corim", "parse_eat"]
