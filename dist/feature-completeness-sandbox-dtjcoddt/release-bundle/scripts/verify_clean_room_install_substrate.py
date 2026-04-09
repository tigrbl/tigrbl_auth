from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tigrbl_auth.cli.install_substrate import PROFILE_TOGGLES, write_install_substrate_report


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify the clean-room install substrate from published artifacts only.")
    parser.add_argument(
        "--profile",
        default=None,
        choices=sorted(PROFILE_TOGGLES),
        help="Install profile to probe in the current environment. Defaults to TIGRBL_AUTH_INSTALL_PROFILE or 'base'.",
    )
    parser.add_argument(
        "--report-dir",
        default=str(ROOT / "docs" / "compliance"),
        help="Directory where install substrate reports should be written.",
    )
    parser.add_argument(
        "--artifact-dir",
        default=str(ROOT / "dist" / "install-substrate"),
        help="Directory where the profile-specific install substrate artifact should be written.",
    )
    parser.add_argument(
        "--strict-manifest",
        action="store_true",
        help="Exit non-zero when the static manifest/workflow/tox checks fail.",
    )
    parser.add_argument(
        "--strict-imports",
        action="store_true",
        help="Exit non-zero when the current environment import probe fails.",
    )
    parser.add_argument(
        "--skip-import-probes",
        action="store_true",
        help="Skip module import probes and only validate manifests/workflows/tox wiring.",
    )
    args = parser.parse_args()

    import os

    profile = args.profile or os.environ.get("TIGRBL_AUTH_INSTALL_PROFILE", "base")

    payload = write_install_substrate_report(
        ROOT,
        profile=profile,
        report_dir=Path(args.report_dir),
        artifact_dir=Path(args.artifact_dir),
        execute_import_probes=not args.skip_import_probes,
    )
    print(json.dumps(payload, indent=2))

    rc = 0
    if args.strict_manifest and not payload.get("summary", {}).get("static_manifest_passed", False):
        rc = 1
    if args.strict_imports and not payload.get("summary", {}).get("current_profile_import_probe_passed", False):
        rc = 1
    if args.strict_imports and not payload.get("summary", {}).get("runtime_surface_probe_passed", False):
        rc = 1
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
