from __future__ import annotations

import warnings

warnings.warn(
    "tigrbl_control_plane_contracts.governance is deprecated; "
    "use tigrbl_management_plane_contracts.governance",
    DeprecationWarning,
    stacklevel=2,
)

from tigrbl_management_plane_contracts.governance import *  # noqa: F401,F403
from tigrbl_management_plane_contracts.governance import __all__ as __all__
