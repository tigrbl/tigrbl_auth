"""Negative vectors that keep neighboring identity artifact profiles distinct."""

import json

import pytest

from tigrbl_auth_protocol_cwt.profile import CwtProfile
from tigrbl_auth_protocol_oidc.id_token_profile import validate_id_token_profile
from tigrbl_credential_profile_vc_jose_cose import select_format, validate_jose_vc
from tigrbl_identity_protocol_did_core import DidCoreProtocol
from tigrbl_proof_of_possession_contracts import PossessionProofVerificationResult
from tigrbl_workload_credential_profile_cwt_svid_extension import (
    validate_cwt_svid_extension,
)


ID_TOKEN_CLAIMS = {
    "iss": "https://issuer.example",
    "sub": "subject",
    "aud": "client",
    "exp": 200,
    "iat": 100,
}


def test_vc_profile_rejects_legacy_nested_vc_claim() -> None:
    with pytest.raises(ValueError, match="legacy vc and vp"):
        validate_jose_vc(
            {"alg": "EdDSA", "typ": "vc+jwt"},
            {"vc": {"type": ["VerifiableCredential"]}},
        )


def test_vc_profile_does_not_advertise_unimplemented_presentations() -> None:
    with pytest.raises(ValueError, match="unsupported VC-JOSE-COSE media type"):
        select_format("application/vp+jwt")


def test_did_document_rejects_unresolved_verification_relationship() -> None:
    document = {
        "id": "did:example:123",
        "verificationMethod": [],
        "authentication": ["did:example:123#missing"],
    }
    with pytest.raises(ValueError, match="unresolved verification relationship"):
        DidCoreProtocol().parse(json.dumps(document))


def test_id_token_profile_rejects_oauth_access_token_type() -> None:
    with pytest.raises(ValueError, match="unexpected ID Token type"):
        validate_id_token_profile(
            {"alg": "RS256", "typ": "at+jwt"},
            ID_TOKEN_CLAIMS,
            expected_issuer="https://issuer.example",
            client_id="client",
            now=150,
        )


def test_cwt_profile_rejects_unselected_cose_carrier() -> None:
    profile = CwtProfile("signed-cwt", frozenset({1, 2, 4}), frozenset({"Sign1"}))
    with pytest.raises(ValueError, match="COSE message type not allowed"):
        profile.validate({1: "issuer", 2: "subject", 4: 200}, "Mac0")


def test_cwt_svid_rejects_unverified_or_replayed_proof() -> None:
    claims = {
        1: "issuer",
        2: "spiffe://example.org/workload",
        4: 200,
        6: 100,
        8: {1: b"key"},
    }
    rejected = PossessionProofVerificationResult(False, replay_accepted=False)
    with pytest.raises(ValueError, match="proof of possession"):
        validate_cwt_svid_extension(
            {1: -7, 4: b"kid"},
            claims,
            proof_result=rejected,
        )
