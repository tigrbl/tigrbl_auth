from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from tigrbl_auth_protocol_cwt.profile import CwtProfile
from tigrbl_auth_protocol_cwt.protocol import CwtProtocol
from tigrbl_cose_cryptography_provider import CoseSign1CryptographyProvider
from tigrbl_cwt_concrete import CwtClaimsSet
from tigrbl_protected_envelope_capability import ProtectedEnvelopeCapability
from tigrbl_security_protocol_cose import COSEProfile, CoseProtocol


def test_cose_sign1_and_cwt_execute_end_to_end() -> None:
    private = ed25519.Ed25519PrivateKey.generate()
    pub = {
        1: 1,
        -1: 6,
        -2: private.public_key().public_bytes(
            serialization.Encoding.Raw, serialization.PublicFormat.Raw
        ),
    }
    issuer = CoseSign1CryptographyProvider({"k": private}, {})
    verifier = CoseSign1CryptographyProvider({}, {"k": pub})
    cap = ProtectedEnvelopeCapability(issuer, verifier)
    cose = CoseProtocol(cap, COSEProfile("cwt", frozenset({-8}), frozenset({1, 4})))
    cwt = CwtProtocol(
        cose, CwtProfile("workload", frozenset({1, 2, 4}), frozenset({"Sign1"}))
    )
    envelope = cwt.issue(
        CwtClaimsSet({1: "issuer", 2: "subject", 4: 20}),
        key_reference="k",
        headers={1: -8, 4: "k"},
    )
    claims, result = cwt.verify(envelope)
    assert result.cryptographic_valid and claims.get_registered("sub") == "subject"
