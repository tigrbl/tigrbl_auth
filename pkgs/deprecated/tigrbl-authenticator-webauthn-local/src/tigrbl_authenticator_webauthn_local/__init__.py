"""Deprecated compatibility import for the removed WebAuthn metadata shell."""

from __future__ import annotations

import warnings


class WebAuthnLocalAuthenticator:
    def __init__(self, *args, **kwargs) -> None:
        warnings.warn(
            "WebAuthnLocalAuthenticator was a metadata-only shell and has been removed; compose the WebAuthn protocol and public-key capabilities instead",
            DeprecationWarning,
            stacklevel=2,
        )
        raise NotImplementedError("use tigrbl_auth_protocol_webauthn and the public-key capability packages")


__all__ = ["WebAuthnLocalAuthenticator"]
