from __future__ import annotations

import pytest

from tigrbl_security_proof_pkce import (
    PKCE_CHALLENGE_METHOD,
    PkceProofProvider,
    make_pkce_verifier,
    pkce_s256_challenge,
    validate_pkce_verifier,
    verify_pkce_s256_challenge,
)
from tigrbl_security_trust_contracts import Artifact, IssueRequest, VerifyRequest


@pytest.mark.unit
def test_pkce_provider_t0_helpers_generate_validate_and_verify_s256() -> None:
    verifier = make_pkce_verifier(64)
    challenge = pkce_s256_challenge(verifier)

    assert validate_pkce_verifier(verifier) == verifier
    assert verify_pkce_s256_challenge(verifier, challenge)
    assert not verify_pkce_s256_challenge(verifier, "wrong")
    assert not verify_pkce_s256_challenge("short", "bad")
    assert verify_pkce_s256_challenge("short", "bad", enabled=False)


@pytest.mark.unit
async def test_pkce_provider_t1_reuses_artifact_verifier_request_shape() -> None:
    provider = PkceProofProvider()
    issued = await provider.issue(IssueRequest(op="issue", opts={"length": 64}))

    assert issued.kind == "pkce"
    assert issued.structured is not None
    assert issued.structured["code_challenge_method"] == PKCE_CHALLENGE_METHOD

    result = await provider.verify(
        VerifyRequest(
            artifact=Artifact(
                kind="pkce",
                format="oauth-parameters",
                structured={"code_challenge": issued.structured["code_challenge"]},
            ),
            context={"code_verifier": issued.structured["code_verifier"]},
        )
    )
    mismatch = await provider.verify(
        VerifyRequest(
            artifact=Artifact(
                kind="pkce",
                format="oauth-parameters",
                structured={"code_challenge": "wrong"},
            ),
            context={"code_verifier": issued.structured["code_verifier"]},
        )
    )

    assert result.valid
    assert not mismatch.valid
