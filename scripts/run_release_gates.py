from __future__ import annotations

import json
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tigrbl_auth.cli.reports import run_release_gates


def main() -> int:
    parser = argparse.ArgumentParser(description="Run release gates for the retained certification boundary.")
    parser.add_argument("gate", nargs="?", default=None, help="Optional gate name to run instead of the full gate order.")
    args = parser.parse_args()

    payload = run_release_gates(ROOT, gate_name=args.gate)
    print(json.dumps(payload, indent=2))
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
