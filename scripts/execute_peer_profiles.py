from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tigrbl_auth.cli.artifacts import deployment_from_options
from tigrbl_auth.cli.reports import execute_peer_profiles


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Emit runtime-foundation checkpoint3 peer-profile execution manifests and coverage checks.")
    parser.add_argument("--profile", default="hardening", help="Deployment profile to bind into execution manifests.")
    parser.add_argument(
        "--execution-mode",
        choices=("self-check", "planned", "external"),
        default="self-check",
        help="Execution mode recorded in the emitted manifests.",
    )
    parser.add_argument(
        "--external-root",
        type=Path,
        default=None,
        help="Optional root containing externally generated peer artifacts organized by peer profile id.",
    )
    args = parser.parse_args(argv)
    if args.external_root is not None:
        os.environ["TIGRBL_AUTH_PEER_ARTIFACTS_ROOT"] = str(args.external_root.resolve())
    payload = execute_peer_profiles(ROOT, deployment_from_options(profile=args.profile), execution_mode=args.execution_mode)
    print(json.dumps(payload, indent=2))
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
