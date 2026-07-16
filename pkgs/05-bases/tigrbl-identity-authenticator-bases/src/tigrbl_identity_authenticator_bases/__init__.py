"""Compatibility facade for :mod:`tigrbl_authenticator_bases`."""

from tigrbl_authenticator_bases import *  # noqa: F401,F403
from tigrbl_authenticator_bases import __all__ as _canonical_all


class WebAuthnAssertionMixin:
    """Removed compatibility shell; use PublicKeyAssertionVerificationBase."""

    async def verify_webauthn_assertion(self, assertion, credential):
        raise NotImplementedError(
            "use tigrbl-public-key-authentication-bases"
        )


__all__ = [*_canonical_all, "WebAuthnAssertionMixin"]
