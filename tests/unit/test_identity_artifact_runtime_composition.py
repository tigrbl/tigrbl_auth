import pytest

from tigrbl_identity_runtime.composition.identity_artifacts import (
    build_identity_artifact_composition,
)


class _Provider:
    def protect(self, request):
        raise NotImplementedError

    def verify(self, request):
        raise NotImplementedError


class _ProofVerifier:
    def verify(self, request):
        raise NotImplementedError


def test_identity_artifact_runtime_composes_protocols_without_transport() -> None:
    provider = _Provider()
    composition = build_identity_artifact_composition(
        jws_issuer=provider,
        jws_verifier=provider,
        cose_issuer=provider,
        cose_verifier=provider,
    )
    assert composition.vc_jose_cose is not None
    assert composition.did_core is not None
    assert composition.cwt_svid_extension is None


def test_experimental_cwt_svid_fails_closed_without_proof_verifier() -> None:
    provider = _Provider()
    with pytest.raises(ValueError, match="proof verifier"):
        build_identity_artifact_composition(
            jws_issuer=provider,
            jws_verifier=provider,
            cose_issuer=provider,
            cose_verifier=provider,
            enable_cwt_svid_extension=True,
        )
    composition = build_identity_artifact_composition(
        jws_issuer=provider,
        jws_verifier=provider,
        cose_issuer=provider,
        cose_verifier=provider,
        proof_verifier=_ProofVerifier(),
        enable_cwt_svid_extension=True,
    )
    assert composition.cwt_svid_extension is not None
