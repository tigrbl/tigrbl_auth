from __future__ import annotations

import tests.unit.formal_auth_helpers  # noqa: F401

from tigrbl_auth.services.formal_authorization import (
    build_control_plane_correctness_report as facade_build_report,
)
from tigrbl_identity_policy import (
    CorrectnessProofSection,
    build_control_plane_correctness_report,
)


def test_control_plane_correctness_report_t0_exports_facade_identity() -> None:
    assert facade_build_report is build_control_plane_correctness_report


def test_control_plane_correctness_report_t1_aggregates_failed_sections() -> None:
    report = build_control_plane_correctness_report(
        report_id="report:authz",
        sections=(
            CorrectnessProofSection("liveness", True, "mutations converged"),
            CorrectnessProofSection("determinism", True, "policy replay was stable"),
            CorrectnessProofSection("delegation", False, "delegation proof failed", ("uncovered scope",)),
        ),
    )

    assert report.passed is False
    assert tuple(section.section_id for section in report.sections) == ("delegation", "determinism", "liveness")
    assert report.failures == ("delegation: uncovered scope",)
