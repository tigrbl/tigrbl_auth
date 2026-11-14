import pytest
import tba_runtime_identity_administration._advanced_identity_plane.authenticators as authenticators_module
from tba_runtime_identity.settings import settings
from tba_auth.services.advanced_identity_plane import (
    AdvancedAuthenticatorRegistry,
)


def test_advanced_authenticator_uses_canonical_webauthn_algorithm_registry(monkeypatch):
    assert "WEBAUTHN_ALGORITHMS" not in authenticators_module.__dict__
    assert (
        AdvancedAuthenticatorRegistry.__init__.__kwdefaults__[
            "webauthn_algorithm_validator"
        ]
        is authenticators_module.is_webauthn_algorithm
    )

    monkeypatch.setattr(settings, "enable_rfc8812", True)
    registry = AdvancedAuthenticatorRegistry()
    with pytest.raises(ValueError, match="unsupported WebAuthn algorithm"):
        registry.register_webauthn_credential(
            subject_id="alice",
            tenant_id="tenant-a",
            rp_id="auth.example.com",
            algorithm="HS256",
        )
