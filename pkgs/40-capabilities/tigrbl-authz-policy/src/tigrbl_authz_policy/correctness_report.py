"""Compatibility re-export for assurance correctness reports."""

from __future__ import annotations

from .assurance import (
    ControlPlaneCorrectnessReport,
    CorrectnessProofSection,
    build_control_plane_correctness_report,
)

__all__ = [
    "ControlPlaneCorrectnessReport",
    "CorrectnessProofSection",
    "build_control_plane_correctness_report",
]
