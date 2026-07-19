from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from tigrbl_identity_core import ProtectedEnvelopeKind
from tigrbl_protected_envelope_contracts import EnvelopeProtectionRequest, EnvelopeVerificationRequest
from tigrbl_jose_cryptography_provider import JweCryptographyProvider, JwsCryptographyProvider
from tigrbl_cose_concrete import sig_structure
from tigrbl_cose_cryptography_provider import sign_detached_signature, verify_detached_signature

def test_jws_and_jwe_providers_execute_crypto() -> None:
    private=ed25519.Ed25519PrivateKey.generate(); pem=private.private_bytes(serialization.Encoding.PEM,serialization.PrivateFormat.PKCS8,serialization.NoEncryption()); pub=private.public_key().public_bytes(serialization.Encoding.PEM,serialization.PublicFormat.SubjectPublicKeyInfo)
    issuer=JwsCryptographyProvider({"k":pem}); envelope=issuer.protect(EnvelopeProtectionRequest(ProtectedEnvelopeKind.JWS,b"payload",{"alg":"EdDSA","kid":"k"},"k"))
    assert JwsCryptographyProvider({"k":pub}).verify(EnvelopeVerificationRequest(envelope)).cryptographic_valid
    jwe=JweCryptographyProvider({"e":b"0"*32}); encrypted=jwe.protect(EnvelopeProtectionRequest(ProtectedEnvelopeKind.JWE,b"secret",{"alg":"dir","enc":"A256GCM"},"e")); assert jwe.verify(EnvelopeVerificationRequest(encrypted)).payload==b"secret"
def test_cose_ed25519_sign_and_verify() -> None:
    private=ed25519.Ed25519PrivateKey.generate(); data=sig_structure("Signature1",b"",b"",b"p"); sig=sign_detached_signature(algorithm=-8,private_key=private,signing_input=data)
    assert verify_detached_signature(algorithm=-8,public_key={1:1,-1:6,-2:private.public_key().public_bytes(serialization.Encoding.Raw,serialization.PublicFormat.Raw)},signing_input=data,signature=sig)