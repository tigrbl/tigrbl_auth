"""Composition root for DID, VC-JOSE-COSE, and experimental CWT-SVID."""

from dataclasses import dataclass

from tigrbl_auth_protocol_cwt import CwtProfile, CwtProtocol
from tigrbl_credential_profile_vc_jose_cose import VcJoseCoseProtocol
from tigrbl_identity_protocol_did_core import DidCoreProtocol
from tigrbl_protected_envelope_capability import ProtectedEnvelopeCapability
from tigrbl_security_protocol_cose import COSEProfile, CoseProtocol
from tigrbl_security_protocol_jws import JWSProfile, JwsProtocol
from tigrbl_workload_credential_profile_cwt_svid_extension import (
    CwtSvidExtensionVerifier,
)


@dataclass(frozen=True, slots=True)
class IdentityArtifactComposition:
    vc_jose_cose: VcJoseCoseProtocol
    did_core: DidCoreProtocol
    cwt_svid_extension: CwtSvidExtensionVerifier | None


def build_identity_artifact_composition(
    *,
    jws_issuer,
    jws_verifier,
    cose_issuer,
    cose_verifier,
    did_resolver=None,
    proof_verifier=None,
    enable_cwt_svid_extension: bool = False,
    jose_algorithms: frozenset[str] = frozenset({"EdDSA", "ES256", "RS256"}),
    cose_algorithms: frozenset[object] = frozenset({-8, -7}),
) -> IdentityArtifactComposition:
    jws_capability = ProtectedEnvelopeCapability(jws_issuer, jws_verifier)
    cose_capability = ProtectedEnvelopeCapability(cose_issuer, cose_verifier)
    jws = JwsProtocol(
        jws_capability,
        JWSProfile(
            "vc+jwt",
            jose_algorithms,
            frozenset({"alg", "kid", "typ"}),
        ),
    )
    vc_cose = CoseProtocol(
        cose_capability,
        COSEProfile(
            "vc+cose",
            cose_algorithms,
            frozenset({1, 4}),
        ),
    )
    vc = VcJoseCoseProtocol(jws_protocol=jws, cose_protocol=vc_cose)
    did = DidCoreProtocol(did_resolver)

    cwt_svid = None
    if enable_cwt_svid_extension:
        if proof_verifier is None:
            raise ValueError(
                "experimental CWT-SVID requires an explicit proof verifier"
            )
        cwt_cose = CoseProtocol(
            cose_capability,
            COSEProfile(
                "cwt-svid-extension",
                cose_algorithms,
                frozenset({1, 4}),
            ),
        )
        cwt = CwtProtocol(
            cwt_cose,
            CwtProfile(
                "cwt-svid-extension",
                frozenset({1, 2, 4, 6, 8}),
                frozenset({"Sign1"}),
            ),
        )
        cwt_svid = CwtSvidExtensionVerifier(cwt, proof_verifier)

    return IdentityArtifactComposition(vc, did, cwt_svid)


__all__ = [
    "IdentityArtifactComposition",
    "build_identity_artifact_composition",
]
