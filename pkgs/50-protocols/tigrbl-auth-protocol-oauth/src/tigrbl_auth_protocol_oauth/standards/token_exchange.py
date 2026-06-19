"""OAuth token exchange compatibility exports.

The ``/token/exchange`` route is owned by
``tigrbl_identity_storage.tables.token_record._token_exchange``.
"""

from __future__ import annotations

from tigrbl_auth_protocol_oauth.standards._rfc8693.runtime import *
from tigrbl_identity_storage.tables.token_record._token_exchange import (
    include_rfc8693,
    include_token_exchange_endpoint,
)

__all__ = [name for name in globals() if not name.startswith("_")]
