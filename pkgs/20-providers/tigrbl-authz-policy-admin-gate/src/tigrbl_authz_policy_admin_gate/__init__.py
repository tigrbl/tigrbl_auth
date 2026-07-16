"""Deprecated compatibility facade for tigrbl-auth-api-admin-gate."""

import warnings

from tigrbl_auth_api_admin_gate import *
from tigrbl_auth_api_admin_gate import __all__

warnings.warn(
    "tigrbl-authz-policy-admin-gate moved to tigrbl-auth-api-admin-gate",
    DeprecationWarning,
    stacklevel=2,
)
