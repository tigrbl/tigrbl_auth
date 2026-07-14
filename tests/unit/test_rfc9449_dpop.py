"""Tests for OAuth 2.0 Demonstrating Proof of Possession (DPoP) - RFC 9449.

These tests verify DPoP proof creation and validation per RFC 9449 and ensure
that the helper functions respect the ``enable_rfc9449`` feature flag.
"""

import asyncio
import pytest
from swarmauri_core.crypto.types import ExportPolicy, KeyUse
from swarmauri_core.key_providers.types import KeyAlg, KeyClass, KeySpec
from swarmauri_keyprovider_local import LocalKeyProvider
from tigrbl_auth.rfc.rfc9449_dpop import (
    RFC9449_SPEC_URL,
    makeProof,
    verify_proof,
    verify_proof_async,
    jwk_from_public_key,
    jwk_thumbprint,
)


class _ReplayOps:
    def __init__(self) -> None:
        self.keys: set[tuple[str, str, str, str, str | None]] = set()

    def check(self, claims, *, ttl_s: int = 300) -> bool:
        key = (claims.jkt, claims.jti, claims.htm, claims.htu, claims.ath)
        replayed = key in self.keys
        self.keys.add(key)
        return replayed


class _NonceOps:
    def __init__(self) -> None:
        self.values: set[str] = set()

    def issue(self, *, ttl_s: int = 300) -> str:
        nonce = f"nonce-{len(self.values) + 1}"
        self.values.add(nonce)
        return nonce

    def consume(self, nonce: str, *, now=None) -> bool:
        if nonce not in self.values:
            return False
        self.values.remove(nonce)
        return True


@pytest.mark.unit
def test_dpop_proof_verification():
    """DPoP proof must match HTTP method and URL and bind to the access token."""
    kp = LocalKeyProvider()
    spec = KeySpec(
        klass=KeyClass.asymmetric,
        alg=KeyAlg.ED25519,
        uses=(KeyUse.SIGN,),
        export_policy=ExportPolicy.SECRET_WHEN_ALLOWED,
    )
    ref = asyncio.run(kp.create_key(spec))
    jwk = jwk_from_public_key(ref.public or b"")
    jkt = jwk_thumbprint(jwk)
    proof = makeProof(ref, "POST", "https://rs.example.com/resource")
    replay = _ReplayOps()
    assert (
        verify_proof(proof, "POST", "https://rs.example.com/resource", jkt=jkt, replay_checker=replay.check) == jkt
    )


@pytest.mark.unit
def test_mismatched_method_rejected():
    """Verification fails when HTTP method does not match proof."""
    kp = LocalKeyProvider()
    spec = KeySpec(
        klass=KeyClass.asymmetric,
        alg=KeyAlg.ED25519,
        uses=(KeyUse.SIGN,),
        export_policy=ExportPolicy.SECRET_WHEN_ALLOWED,
    )
    ref = asyncio.run(kp.create_key(spec))
    proof = makeProof(ref, "GET", "https://rs.example.com/data")
    with pytest.raises(ValueError):
        verify_proof(proof, "POST", "https://rs.example.com/data", replay_checker=_ReplayOps().check)


@pytest.mark.unit
def test_feature_toggle_disabled():
    """When disabled, proof verification returns empty string."""
    kp = LocalKeyProvider()
    spec = KeySpec(
        klass=KeyClass.asymmetric,
        alg=KeyAlg.ED25519,
        uses=(KeyUse.SIGN,),
        export_policy=ExportPolicy.SECRET_WHEN_ALLOWED,
    )
    ref = asyncio.run(kp.create_key(spec))
    proof = makeProof(ref, "GET", "https://rs.example.com/data", enabled=False)
    assert proof == ""
    assert verify_proof("", "GET", "https://rs.example.com/data", enabled=False) == ""


@pytest.mark.unit
def test_spec_url_constant():
    """Ensure the exported constant points to the RFC 9449 specification."""
    assert RFC9449_SPEC_URL.endswith("rfc9449")


@pytest.mark.unit
def test_async_dpop_verifier_accepts_table_style_nonce_and_replay_operations():
    class AsyncReplayOps:
        def __init__(self) -> None:
            self.claims = []

        async def check(self, claims, *, ttl_s: int = 300) -> bool:
            self.claims.append((claims, ttl_s))
            return len(self.claims) > 1

    class AsyncNonceOps:
        def __init__(self, expected: str) -> None:
            self.expected = expected
            self.consumed = []

        async def consume(self, nonce: str, *, now=None) -> bool:
            self.consumed.append((nonce, now))
            return nonce == self.expected

    kp = LocalKeyProvider()
    spec = KeySpec(
        klass=KeyClass.asymmetric,
        alg=KeyAlg.ED25519,
        uses=(KeyUse.SIGN,),
        export_policy=ExportPolicy.SECRET_WHEN_ALLOWED,
    )
    ref = asyncio.run(kp.create_key(spec))
    jwk = jwk_from_public_key(ref.public or b"")
    jkt = jwk_thumbprint(jwk)
    nonce = "nonce-1"
    proof = makeProof(ref, "POST", "https://rs.example.com/resource", nonce=nonce)
    replay = AsyncReplayOps()
    nonce_ops = AsyncNonceOps(nonce)

    assert (
        asyncio.run(
            verify_proof_async(
                proof,
                "POST",
                "https://rs.example.com/resource",
                jkt=jkt,
                expected_nonce=nonce,
                replay_checker=replay.check,
                nonce_consumer=nonce_ops.consume,
            )
        )
        == jkt
    )
    assert replay.claims[0][0].jkt == jkt
    assert nonce_ops.consumed == [(nonce, None)]

    with pytest.raises(ValueError, match="replayed DPoP proof"):
        asyncio.run(
            verify_proof_async(
                proof,
                "POST",
                "https://rs.example.com/resource",
                jkt=jkt,
                replay_checker=replay.check,
            )
        )


@pytest.mark.unit
def test_dpop_protocol_does_not_export_store_classes():
    import tigrbl_auth_protocol_oauth.standards.dpop as dpop

    assert not hasattr(dpop, "DPoPReplayStore")
    assert not hasattr(dpop, "DPoPNonceStore")
