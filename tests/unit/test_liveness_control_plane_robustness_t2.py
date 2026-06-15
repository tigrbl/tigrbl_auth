from __future__ import annotations

import tests.unit.formal_auth_helpers  # noqa: F401

from tigrbl_authz_policy import (
    ConvergenceEvent,
    CorrectnessProofSection,
    build_control_plane_correctness_report,
    evaluate_liveness_convergence,
)


def test_liveness_convergence_t2_distinguishes_pending_late_duplicate_and_out_of_order_events() -> None:
    events = (
        ConvergenceEvent("evt:policy", "policy:publish", "policy:v2", "2026-06-07T00:00:00+00:00", "2026-06-07T00:00:20+00:00", 30),
        ConvergenceEvent("evt:revocation", "revocation", "grant:1", "2026-06-07T00:00:00+00:00"),
        ConvergenceEvent("evt:key", "key:rotation", "key:1", "2026-06-07T00:00:00+00:00", "2026-06-07T00:02:00+00:00", 30),
        ConvergenceEvent("evt:delegation", "delegation:revoke", "delegation:1", "2026-06-07T00:00:00+00:00", "2026-06-07T00:00:01+00:00", 30),
        ConvergenceEvent("evt:trust", "trust-edge:revoke", "trust:1", "2026-06-07T00:00:00+00:00", "2026-06-07T00:00:01+00:00", 30),
        ConvergenceEvent("evt:delegation", "delegation:revoke", "delegation:1", "2026-06-07T00:00:00+00:00", "2026-06-07T00:00:01+00:00", 30),
    )

    report_a = evaluate_liveness_convergence(events)
    report_b = evaluate_liveness_convergence(tuple(reversed(events)))

    assert tuple(event.event_id for event in report_a.converged) == ("evt:delegation", "evt:policy", "evt:trust")
    assert tuple(event.event_id for event in report_a.pending) == ("evt:revocation",)
    assert tuple(event.event_id for event in report_a.late) == ("evt:key",)
    assert report_a.failures == report_b.failures
    assert len(report_a.converged) + len(report_a.pending) + len(report_a.late) == 5


def test_control_plane_report_t2_fails_closed_for_empty_and_missing_required_proof_families() -> None:
    empty = build_control_plane_correctness_report(report_id="report:empty", sections=())
    missing = build_control_plane_correctness_report(
        report_id="report:missing",
        required_section_ids=("delegation", "determinism", "liveness"),
        sections=(CorrectnessProofSection("liveness", True, "liveness passed"),),
    )

    assert empty.passed is False
    assert empty.failures == ("report has no proof sections",)
    assert missing.passed is False
    assert missing.failures == (
        "missing required proof section: delegation",
        "missing required proof section: determinism",
    )


def test_control_plane_report_t2_preserves_source_failures_and_is_stable_across_section_order() -> None:
    sections = (
        CorrectnessProofSection("liveness", True, "mutations converged"),
        CorrectnessProofSection("delegation", False, "delegation failed", ("uncovered scope", "unknown provenance")),
        CorrectnessProofSection("determinism", True, "replay stable"),
    )

    report_a = build_control_plane_correctness_report(
        report_id="report:authz",
        required_section_ids=("delegation", "determinism", "liveness"),
        sections=sections,
    )
    report_b = build_control_plane_correctness_report(
        report_id="report:authz",
        required_section_ids=("delegation", "determinism", "liveness"),
        sections=tuple(reversed(sections)),
    )

    assert tuple(section.section_id for section in report_a.sections) == ("delegation", "determinism", "liveness")
    assert report_a.failures == ("delegation: uncovered scope", "delegation: unknown provenance")
    assert report_a == report_b
