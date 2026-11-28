import pytest
from tba_auth.services.advanced_identity_plane import (
    AdvancedAuthenticatorRegistry,
)


def test_deprecated_advanced_authenticator_registry_reexports_admin_surface():
    with pytest.warns(DeprecationWarning):
        from tba_runtime_identity_administration_advanced_authenticator_registry import (
            AdvancedAuthenticatorRegistry as DeprecatedAdvancedAuthenticatorRegistry,
        )

    assert DeprecatedAdvancedAuthenticatorRegistry is AdvancedAuthenticatorRegistry
