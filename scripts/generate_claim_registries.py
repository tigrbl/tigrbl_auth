from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tigrbl_auth.cli.claim_registry import generate_claim_registries, verify_claim_registries


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate or verify canonical claim registries.")
    parser.add_argument("--verify", action="store_true", help="Verify the registry model without rewriting files.")
    args = parser.parse_args()

    payload = verify_claim_registries(ROOT) if args.verify else generate_claim_registries(ROOT)
    print(json.dumps(payload, indent=2))
    return 0 if payload.get("passed", False) else 1


if __name__ == "__main__":
    raise SystemExit(main())
