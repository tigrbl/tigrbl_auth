"""Cross-repository compact JWE interoperability against Swarmauri source."""

import os
from pathlib import Path

import pytest
from cryptography.hazmat.primitives.asymmetric.x448 import X448PrivateKey
from tba_capability_protected_envelope import ProtectedEnvelopeCapability
from tba_concrete_jose import JweCipherPolicy
from tba_concrete_jwe import parse_jwe_compact
from tba_contracts_protected_envelope import ProtectedEnvelope
from tba_primitives_identity import ProtectedEnvelopeKind
from tba_primitives_identity.base64url import base64url_encode
from tba_protocol_security_jwe import JWEProfile, JweProtocol
from tba_provider_jose_cryptography import JweCryptographyProvider


@pytest.fixture
def swarmauri_jwe(monkeypatch):
    checkout = os.environ.get("SWARMAURI_SDK_ROOT")
    if not checkout:
        pytest.skip("Set SWARMAURI_SDK_ROOT to the Swarmauri SDK checkout")
    packages = Path(checkout).resolve(strict=True) / "pkgs"
    monkeypatch.syspath_prepend(str(packages / "core"))
    monkeypatch.syspath_prepend(str(packages / "standards" / "swarmauri_crypto_jwe"))
    from swarmauri_core.crypto.types import JWAAlg
    from swarmauri_crypto_jwe import JweCrypto
    import swarmauri_crypto_jwe

    assert Path(swarmauri_crypto_jwe.__file__).is_relative_to(packages)
    return JweCrypto(enable_x448=True), JWAAlg


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("payload", "party_headers"),
    [(b"", {}), (b"cross-repository X448", {"apu": "QWxpY2U", "apv": "Qm9i"})],
)
async def test_compact_x448_interop_in_both_directions(
    swarmauri_jwe, payload, party_headers
) -> None:
    sdk, algorithms = swarmauri_jwe
    key = X448PrivateKey.generate()
    public = key.public_key()
    jwk = {
        "kty": "OKP",
        "crv": "X448",
        "x": base64url_encode(public.public_bytes_raw()),
    }
    policy = JweCipherPolicy()
    issuer = JweCryptographyProvider(
        cipher_policy=policy, x448_public_keys={"r": public}
    )
    verifier = JweCryptographyProvider(
        cipher_policy=policy, x448_private_keys={"r": key}
    )
    protocol = JweProtocol(
        ProtectedEnvelopeCapability(issuer, verifier),
        JWEProfile("x448", frozenset({"ECDH-ES"}), frozenset({"alg", "enc", "kid"})),
    )

    sdk_token = await sdk.encrypt_compact(
        payload=payload,
        alg=algorithms.ECDH_ES,
        enc=algorithms.A256GCM,
        key=jwk,
        kid="r",
        header_extra=party_headers,
    )
    sdk_headers = parse_jwe_compact(sdk_token).protected_headers
    envelope = ProtectedEnvelope(ProtectedEnvelopeKind.JWE, sdk_token, sdk_headers)
    assert protocol.decrypt(envelope).payload == payload

    tba_envelope = protocol.encrypt(
        payload,
        key_reference="r",
        headers={"alg": "ECDH-ES", "enc": "A256GCM", "kid": "r", **party_headers},
    )
    assert (
        await sdk.decrypt_compact(tba_envelope.serialization, ecdh_private_key=key)
    ).plaintext == payload
