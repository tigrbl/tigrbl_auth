import pytest
from tba_runtime_identity_administration._advanced_identity_plane.authenticators import (
    AdvancedAuthenticatorRegistry as CanonicalAdvancedAuthenticatorRegistry,
)
from tba_provider_authentication_anomaly_detector import (
    AuthAnomalyDetector as CanonicalAuthAnomalyDetector,
)
from tba_storage_core.tables import (
    AuthenticationChallenge as CanonicalAuthenticationChallenge,
)
from tba_storage_core.tables import CredentialMfaFactor, CredentialWebAuthnPasskey
from tba_auth.services.advanced_identity_plane import (
    AdaptiveContext,
    AdvancedAuthenticatorRegistry,
    AuthAnomalyDetector,
)


def test_advanced_authenticator_registry_supports_passwordless_webauthn_mfa_and_replay_safety():
    assert AdvancedAuthenticatorRegistry is CanonicalAdvancedAuthenticatorRegistry

    registry = AdvancedAuthenticatorRegistry()
    assert registry.challenge_table is CanonicalAuthenticationChallenge
    assert registry.mfa_factor_table is CredentialMfaFactor
    assert registry.webauthn_passkey_table is CredentialWebAuthnPasskey
    passwordless = registry.enroll_passwordless_credential(
        subject_id="alice",
        tenant_id="tenant-a",
        recovery_codes=("backup-1", "backup-2"),
    )
    webauthn = registry.register_webauthn_credential(
        subject_id="alice",
        tenant_id="tenant-a",
        rp_id="auth.example.com",
        algorithm="ES256",
        transports=("internal", "hybrid"),
    )
    factor = registry.enroll_mfa_factor(
        subject_id="alice",
        tenant_id="tenant-a",
        method="otp",
        bound_credential_id=webauthn.credential_id,
    )

    challenge, decision = registry.begin_passwordless_assertion(
        subject_id="alice",
        tenant_id="tenant-a",
        context=AdaptiveContext(
            tenant_id="tenant-a",
            trusted_network=False,
            trusted_device=False,
            ip_country="DE",
            local_hour=23,
            known_countries=("US", "DE"),
        ),
    )

    assert passwordless.recovery_codes == ("backup-1", "backup-2")
    assert decision.allowed
    assert decision.step_up_required
    assert decision.risk_level == "medium"
    assert set(challenge.allowed_methods) == {"otp", "passwordless", "webauthn"}

    completed = registry.complete_passwordless_assertion(
        challenge_id=challenge.challenge_id,
        credential_id=webauthn.credential_id,
        nonce=challenge.expected_nonce,
    )
    mfa_challenge = registry.begin_mfa_challenge(
        subject_id="alice", tenant_id="tenant-a"
    )
    registry.complete_mfa_challenge(
        challenge_id=mfa_challenge.challenge_id,
        factor_id=factor.factor_id,
        method="otp",
        nonce=mfa_challenge.expected_nonce,
    )

    assert completed.bound_credential_id == webauthn.credential_id
    assert registry.webauthn_credentials[webauthn.credential_id].sign_count == 1

    with pytest.raises(PermissionError, match="already consumed"):
        registry.complete_passwordless_assertion(
            challenge_id=challenge.challenge_id,
            credential_id=webauthn.credential_id,
            nonce=challenge.expected_nonce,
        )


def test_auth_anomaly_detector_normalizes_redacts_and_explains_detection_outputs():
    assert AuthAnomalyDetector is CanonicalAuthAnomalyDetector

    detector = AuthAnomalyDetector()
    detector.record_event(
        tenant_id="tenant-a",
        subject_id="alice",
        event_type="login",
        correlation_id="corr-1",
        ip_country="US",
        trusted_device=True,
        outcome="failure",
        details={"access_token": "abc.def.ghi", "ip": "198.51.100.10"},
    )
    detector.record_event(
        tenant_id="tenant-a",
        subject_id="alice",
        event_type="login",
        correlation_id="corr-2",
        ip_country="US",
        trusted_device=False,
        outcome="failure",
        details={"password": "never-log-this", "ip": "198.51.100.11"},
    )
    event, signal = detector.record_event(
        tenant_id="tenant-a",
        subject_id="alice",
        event_type="login",
        correlation_id="corr-3",
        ip_country="DE",
        trusted_device=False,
        outcome="failure",
        details={"refresh_token": "secret", "ip": "203.0.113.44"},
    )

    assert signal is not None
    assert signal.severity == "high"
    assert signal.recommended_action == "manual-review"
    assert "repeated authentication failures" in signal.reasons
    assert "untrusted device telemetry" in signal.reasons
    assert event.details["refresh_token"] == "[REDACTED]"
    assert signal.redacted_details["refresh_token"] == "[REDACTED]"
