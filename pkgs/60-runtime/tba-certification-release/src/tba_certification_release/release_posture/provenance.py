from __future__ import annotations

from pathlib import Path

from .models import PROVENANCE_REQUIREMENTS, REPO_ROOT, ProvenanceRequirement


def build_release_provenance_requirements(repo_root: Path | None = None) -> dict[str, ProvenanceRequirement]:
    root = (repo_root or REPO_ROOT).resolve()
    requirements: dict[str, ProvenanceRequirement] = {}
    for standard, requirement in PROVENANCE_REQUIREMENTS.items():
        expected_paths = tuple(
            dict.fromkeys(
                (
                    *requirement["required"],
                    *requirement["generated"],
                    *requirement["disclosure"],
                )
            )
        )
        missing_paths = tuple(path for path in expected_paths if not (root / path).exists())
        requirements[standard] = ProvenanceRequirement(
            standard=standard,
            required_artifact_paths=requirement["required"],
            generated_projection_paths=requirement["generated"],
            release_gate_obligations=requirement["gates"],
            disclosure_paths=requirement["disclosure"],
            satisfied=not missing_paths,
            missing_paths=missing_paths,
        )
    return requirements
