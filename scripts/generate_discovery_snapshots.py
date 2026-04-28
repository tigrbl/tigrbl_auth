from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tigrbl_auth.cli.artifacts import deployment_from_options, write_discovery_artifacts
from tigrbl_auth.config.deployment import VALID_PROFILES


PROFILES = VALID_PROFILES


def write_discovery_reference(repo_root: Path) -> None:
    lines = [
        "# Discovery Profile Snapshots",
        "",
        "The following profile-specific discovery snapshots are committed from executable deployment metadata:",
        "",
    ]
    for profile_name in PROFILES:
        lines.append(f"- `{profile_name}`")
        profile_dir = repo_root / "specs" / "discovery" / "profiles" / profile_name
        for name in sorted(path.name for path in profile_dir.glob("*.json")):
            lines.append(f"  - `specs/discovery/profiles/{profile_name}/{name}`")
    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- snapshot files are generated from `tigrbl_auth.cli.artifacts.write_discovery_artifacts` using executable deployment metadata",
            "- JWKS snapshots intentionally omit live signing material and record only a deterministic public-artifact shape",
            "- current authoritative CLI/runtime/discovery docs are those listed in `docs/reference/README.md`",
            "",
        ]
    )
    (repo_root / "docs" / "reference" / "DISCOVERY_PROFILE_SNAPSHOTS.md").write_text("\n".join(lines), encoding="utf-8")



def main() -> int:
    for profile_name in PROFILES:
        deployment = deployment_from_options(profile=profile_name)
        write_discovery_artifacts(ROOT, deployment, profile_label=profile_name)
    write_discovery_reference(ROOT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
