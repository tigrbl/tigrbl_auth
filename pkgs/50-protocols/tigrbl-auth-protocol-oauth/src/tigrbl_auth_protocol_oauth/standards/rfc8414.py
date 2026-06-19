"""RFC 8414 compatibility exports.

The well-known route is owned by
``tigrbl_identity_storage.tables.realm._oauth_authorization_server_metadata``.
"""

from __future__ import annotations

from typing import Final

from tigrbl_auth_protocol_oauth.standards.rfc8414_metadata import *
from tigrbl_identity_storage.tables.realm._oauth_authorization_server_metadata import (
    include_rfc8414,
)

RFC8414_SPEC_URL: Final = "https://www.rfc-editor.org/rfc/rfc8414"

__all__ = [name for name in globals() if not name.startswith("_")]
