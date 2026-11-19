from dataclasses import replace

import pytest
from cryptography.hazmat.primitives.asymmetric.x448 import X448PrivateKey
from tba_concrete_jose import JweCipherPolicy
from tba_contracts_protected_envelope import (
    EnvelopeProtectionRequest,
    EnvelopeVerificationRequest,
)
from tba_primitives_identity import ProtectedEnvelopeKind
from tba_provider_jose_cryptography import JweCryptographyProvider
from tba_provider_jose_cryptography._x448 import (
    _concat_kdf,
    load_public_jwk,
    public_jwk,
)

HEADERS = {"alg": "ECDH-ES", "enc": "A256GCM"}


def test_rfc7518_appendix_c_concat_kdf() -> None:
    secret = bytes.fromhex(
        "9e56d91d817135d372834283bf84269cfb316ea3da806a48f6daa7798cfe90c4"
    )
    assert _concat_kdf(secret, "A128GCM", 16, b"Alice", b"Bob") == bytes.fromhex(
        "56aa8deaf8236d205c2228cd71a7101a"
    )


def test_rfc8037_appendix_a7_x448() -> None:
    sender = X448PrivateKey.from_private_bytes(
        bytes.fromhex(
            "9a8f4925d1519f5775cf46b04b5800d4ee9ee8bae8bc5565d498c28d"
            "d9c9baf574a9419744897391006382a6f127ab1d9ac2d8c0a598726b"
        )
    )
    recipient = load_public_jwk(
        {
            "kty": "OKP",
            "crv": "X448",
            "x": "PreoKbDNIPW8_AtZm2_sz22kYnEHvbDU80W0MCfYuXL8PjT7QjKhPKcG3LV67D2uB73BxnvzNgk",
        }
    )
    assert public_jwk(sender.public_key())["x"] == (
        "mwj3zDG34-Z9ItWuoSEHSic70rg94Jxj-qc9LCLF2bvINmRyQdlT1AxbEtqIEg1TF3-A5TLEH6A"
    )
    assert sender.exchange(recipient) == bytes.fromhex(
        "07fff4181ac6cc95ec1c16a94a0f74d12da232ce40a77552281d282b"
        "b60c0b56fd2464c335543936521c24403085d59a449a5037514a879d"
    )


def test_x448_protection_and_verification_require_cipher_policy() -> None:
    recipient = X448PrivateKey.generate()
    public = {"recipient": recipient.public_key()}
    private = {"recipient": recipient}
    request = EnvelopeProtectionRequest(
        ProtectedEnvelopeKind.JWE, b"payload", HEADERS, "recipient"
    )
    with pytest.raises(ValueError, match="explicit X448 cipher policy"):
        JweCryptographyProvider(x448_public_keys=public).protect(request)

    policy = JweCipherPolicy()
    assert not policy.lint()
    issuer = JweCryptographyProvider(cipher_policy=policy, x448_public_keys=public)
    envelope = issuer.protect(request)
    assert (
        envelope.protected_headers["epk"]
        != issuer.protect(request).protected_headers["epk"]
    )
    verification = EnvelopeVerificationRequest(envelope)
    verifier = JweCryptographyProvider(cipher_policy=policy, x448_private_keys=private)
    assert verifier.verify(verification).payload == b"payload"
    assert (
        not JweCryptographyProvider(x448_private_keys=private)
        .verify(verification)
        .valid
    )
    wrong_key = JweCryptographyProvider(
        cipher_policy=policy, x448_private_keys={"recipient": X448PrivateKey.generate()}
    )
    assert not wrong_key.verify(verification).valid
    segments = str(envelope.serialization).split(".")
    segments[1] = "AA"
    altered = replace(envelope, serialization=".".join(segments))
    assert not verifier.verify(EnvelopeVerificationRequest(altered)).valid

    class DenyRecipient(JweCipherPolicy):
        def normalize(self, **kwargs):
            raise ValueError("recipient forbidden by cipher policy")

    denied = JweCryptographyProvider(
        cipher_policy=DenyRecipient(),
        x448_public_keys=public,
        x448_private_keys=private,
    )
    with pytest.raises(ValueError, match="recipient forbidden"):
        denied.protect(request)
    assert "recipient forbidden" in denied.verify(verification).reason
