from __future__ import annotations

from pathlib import Path
from typing import Any

from .disclosure import build_disclosure_rules
from .provenance import build_release_provenance_requirements
from .transport import build_transport_postures


def build_phase6_delivery_summary(*, repo_root: Path | None = None) -> dict[str, Any]:
    transport = build_transport_postures()
    disclosure = build_disclosure_rules()
    provenance = build_release_provenance_requirements(repo_root=repo_root)
    return {
        "transport": {
            "implemented_protocols": sorted(
                protocol
                for protocol, posture in transport.items()
                if posture.backend_runtime_support == "implemented"
            ),
            "claimable_protocols": sorted(
                protocol
                for protocol, posture in transport.items()
                if posture.certification_claimable
            ),
            "upgrade_protocols": sorted(
                protocol
                for protocol, posture in transport.items()
                if posture.enablement_flags
            ),
            "missing_protocols": sorted(
                protocol
                for protocol, posture in transport.items()
                if posture.backend_runtime_support != "implemented"
            ),
        },
        "uix_disclosure": {
            "artifact_kinds": sorted(disclosure),
            "admin_renderings": sorted(rule.admin_rendering for rule in disclosure.values()),
            "public_renderings": sorted(rule.public_rendering for rule in disclosure.values()),
            "redacted_field_count": sum(len(rule.redacted_fields) for rule in disclosure.values()),
        },
        "release_provenance": {
            "standards": sorted(provenance),
            "satisfied_standards": sorted(
                standard
                for standard, requirement in provenance.items()
                if requirement.satisfied
            ),
            "release_gate_obligations": sorted(
                {
                    gate
                    for requirement in provenance.values()
                    for gate in requirement.release_gate_obligations
                }
            ),
            "missing_path_count": sum(len(requirement.missing_paths) for requirement in provenance.values()),
        },
    }
