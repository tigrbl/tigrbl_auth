from time import time

from tigrbl_key_attestation_verifier import ProfiledKeyAttestationVerifier
from tigrbl_platform_attestation_provider import PlatformAttestationProvider
from tigrbl_security_event_replay_store import InMemorySecurityEventReplayStore
from tigrbl_wallet_attestation_verifier import ProfiledWalletAttestationVerifier


def _wallet_claims(**overrides):
    claims = {
        "iss": "https://wallet-provider.example",
        "aud": "https://issuer.example",
        "iat": int(time()),
        "exp": int(time()) + 60,
        "jti": "attestation-1",
        "wallet_instance_id": "wallet-1",
        "key_protection": "hardware",
    }
    claims.update(overrides)
    return claims


def test_wallet_attestation_requires_profile_typ_claim_policy_and_replay_once():
    replay = InMemorySecurityEventReplayStore()
    verifier = ProfiledWalletAttestationVerifier(
        lambda token, profile: ({"typ": "wallet-attestation+jwt"}, _wallet_claims()),
        "https://wallet-provider.example",
        "https://issuer.example",
        replay.consume_once,
    )
    assert verifier.verify_wallet_attestation("a.b.c")
    assert not verifier.verify_wallet_attestation("a.b.c")


def test_wallet_attestation_rejects_software_key_or_wrong_token_profile_typ():
    verifier = ProfiledWalletAttestationVerifier(
        lambda token, profile: (
            {"typ": "JWT"},
            _wallet_claims(key_protection="software"),
        ),
        "https://wallet-provider.example",
        "https://issuer.example",
        lambda issuer, token_id: True,
    )
    assert not verifier.verify_wallet_attestation("a.b.c")


def test_key_attestation_binds_profile_key_challenge_and_protection():
    def backend(artifact, profile):
        return {
            "profile": profile,
            "key_id": "key-1",
            "challenge": "challenge-1",
            "key_protection": "secure-element",
            "verified_boot": True,
        }
    verifier = ProfiledKeyAttestationVerifier(
        backend,
        "android-key",
        "key-1",
        "challenge-1",
    )
    assert verifier.verify_key_attestation(b"attestation")
    wrong_challenge = ProfiledKeyAttestationVerifier(
        backend,
        "android-key",
        "key-1",
        "different",
    )
    assert not wrong_challenge.verify_key_attestation(b"attestation")


def test_platform_provider_normalizes_vendor_evidence_and_checks_profile():
    provider = PlatformAttestationProvider()
    provider.register(
        "tpm",
        lambda artifact, profile: {
            "eat_profile": profile,
            "measurement": "approved",
            "raw_format": "tpm-quote",
        },
    )
    evidence = provider.collect("tpm", b"quote", "urn:example:eat-profile")
    assert evidence.claims["platform"] == "tpm"
    assert evidence.profile == "urn:example:eat-profile"
