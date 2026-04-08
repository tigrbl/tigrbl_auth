from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tigrbl_auth.cli.artifacts import deployment_from_options, write_openrpc_contract


def main() -> int:
    repo_root = ROOT
    write_openrpc_contract(repo_root, deployment_from_options())
    for profile_name in ("baseline", "production", "hardening", "fapi2-security", "peer-claim"):
        write_openrpc_contract(repo_root, deployment_from_options(profile=profile_name), profile_label=profile_name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
