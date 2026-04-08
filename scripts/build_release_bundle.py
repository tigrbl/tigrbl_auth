from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tigrbl_auth.cli.artifacts import deployment_from_options
from tigrbl_auth.cli.reports import build_release_bundle


PROFILES = ("baseline", "production", "hardening", "fapi2-security", "peer-claim")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--allow-dirty", action="store_true", help="Permit release bundle generation from a dirty checkout.")
    args = parser.parse_args()
    bundles = []
    for profile in PROFILES:
        deployment = deployment_from_options(profile=profile)
        path = build_release_bundle(ROOT, deployment, require_clean_checkout=not args.allow_dirty)
        bundles.append({"profile": profile, "bundle_dir": str(path.relative_to(ROOT))})
    print(json.dumps({"bundles": bundles}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
