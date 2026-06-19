from __future__ import annotations

from typing import Iterable

from tigrbl_control_plane_contracts.correctness import (
    ControlPlaneCorrectnessReport,
    CorrectnessProofSection,
)


def build_control_plane_correctness_report(
    *,
    report_id: str,
    sections: Iterable[CorrectnessProofSection],
    required_section_ids: Iterable[str] = (),
) -> ControlPlaneCorrectnessReport:
    rows = tuple(sorted(sections, key=lambda section: section.section_id))
    present_section_ids = {section.section_id for section in rows}
    missing_sections = tuple(sorted(set(required_section_ids) - present_section_ids))
    failures = tuple(
        [
            *(f"missing required proof section: {section_id}" for section_id in missing_sections),
            *(("report has no proof sections",) if not rows else ()),
            *(
                failure
                for section in rows
                for failure in (
                    (f"{section.section_id}: {item}" for item in section.failures)
                    if not section.passed
                    else ()
                )
            ),
        ]
    )
    return ControlPlaneCorrectnessReport(
        report_id=report_id,
        passed=not failures,
        sections=rows,
        failures=failures,
    )


__all__ = [
    "ControlPlaneCorrectnessReport",
    "CorrectnessProofSection",
    "build_control_plane_correctness_report",
]
