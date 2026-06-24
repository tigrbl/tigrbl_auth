"""OAuth token exchange compatibility exports.

The ``/token/exchange`` route is owned by
``tigrbl_identity_storage_runtime.token_exchange``.
"""

from __future__ import annotations
# ruff: noqa: F403,F405

from tigrbl_auth_protocol_oauth.standards._rfc8693.runtime import *
from tigrbl_identity_storage_runtime.token_exchange import *

__all__ = [name for name in globals() if not name.startswith("_")]
