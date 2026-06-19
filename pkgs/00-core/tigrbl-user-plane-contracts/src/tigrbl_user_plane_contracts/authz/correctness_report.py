from __future__ import annotations

import warnings

from tigrbl_control_plane_contracts.correctness import (
    ControlPlaneCorrectnessReport,
    CorrectnessProofSection,
)

warnings.warn(
    "tigrbl_user_plane_contracts.authz.correctness_report is deprecated; "
    "import control-plane correctness DTOs from "
    "tigrbl_control_plane_contracts.correctness and executable report builders "
    "from tigrbl_authz_policy.correctness_report.",
    DeprecationWarning,
    stacklevel=2,
)


__all__ = [
    "ControlPlaneCorrectnessReport",
    "CorrectnessProofSection",
]
