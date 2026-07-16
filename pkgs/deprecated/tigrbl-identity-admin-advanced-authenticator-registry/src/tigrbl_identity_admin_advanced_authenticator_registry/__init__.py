from __future__ import annotations

import warnings

from tigrbl_advanced_authentication_capability.authenticators import AdvancedAuthenticatorRegistry


warnings.warn(
    "tigrbl_identity_admin_advanced_authenticator_registry is deprecated; "
    "import AdvancedAuthenticatorRegistry from tigrbl_identity_admin instead.",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = ["AdvancedAuthenticatorRegistry"]
