from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tigrbl_auth.cli.reports import generate_certification_evidence_index


def main() -> int:
    payload = generate_certification_evidence_index(ROOT)
    print(json.dumps(payload.get("summary", {}), indent=2, sort_keys=True))
    return 0 if payload.get("passed", False) else 1


if __name__ == "__main__":
    raise SystemExit(main())
