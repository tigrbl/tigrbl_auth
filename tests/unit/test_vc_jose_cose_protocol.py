from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519

from tigrbl_cose_cryptography_provider import CoseSign1CryptographyProvider
from tigrbl_jose_cryptography_provider import JwsCryptographyProvider
from tigrbl_protected_envelope_capability import ProtectedEnvelopeCapability
from tigrbl_security_protocol_cose import COSEProfile, CoseProtocol
from tigrbl_security_protocol_jws import JWSProfile, JwsProtocol
from tigrbl_credential_profile_vc_jose_cose import VcJoseCoseProtocol


VC = {
    "@context": ["https://www.w3.org/ns/credentials/v2"],
    "type": ["VerifiableCredential"],
    "issuer": "https://issuer.example",
    "credentialSubject": {"id": "did:example:holder"},
}


def _protocol() -> VcJoseCoseProtocol:
    private = ed25519.Ed25519PrivateKey.generate()
    private_pem = private.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    )
    public_pem = private.public_key().public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    jws = JwsProtocol(
        ProtectedEnvelopeCapability(
            JwsCryptographyProvider({"jose": private_pem}),
            JwsCryptographyProvider({"jose": public_pem}),
        ),
        JWSProfile("vc+jwt", frozenset({"EdDSA"}), frozenset({"alg", "kid", "typ"})),
    )
    cose_key = {1: 1, -1: 6, -2: private.public_key().public_bytes_raw()}
    cose = CoseProtocol(
        ProtectedEnvelopeCapability(
            CoseSign1CryptographyProvider({"cose": private}),
            CoseSign1CryptographyProvider({}, {"cose": cose_key}),
        ),
        COSEProfile("vc+cose", frozenset({-8}), frozenset({1, 4})),
    )
    return VcJoseCoseProtocol(jws_protocol=jws, cose_protocol=cose)


def test_vc_jose_issuance_and_verification_reconstructs_verified_claims() -> None:
    protocol = _protocol()
    credential = protocol.issue(
        VC,
        media_type="application/vc+jwt",
        key_reference="jose",
        headers={"alg": "EdDSA", "kid": "jose", "typ": "vc+jwt"},
    )
    result = protocol.verify(credential)
    assert result.valid
    assert result.credential.credential_claims["issuer"] == VC["issuer"]


def test_vc_cose_issuance_and_verification_executes_crypto() -> None:
    protocol = _protocol()
    credential = protocol.issue(
        VC,
        media_type="application/vc+cose",
        key_reference="cose",
        headers={1: -8, 4: b"cose"},
    )
    result = protocol.verify(credential)
    assert result.valid
    assert result.envelope_result.cryptographic_valid
