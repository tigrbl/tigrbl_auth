"""Deprecated compatibility facade for tigrbl-auth-router-admin-gate."""

import warnings

from tigrbl_auth_router_admin_gate import *
from tigrbl_auth_router_admin_gate import __all__

warnings.warn(
    "tigrbl-authz-policy-admin-gate moved to tigrbl-auth-router-admin-gate",
    DeprecationWarning,
    stacklevel=2,
)
