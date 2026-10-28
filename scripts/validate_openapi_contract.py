from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tba_auth.cli.reports import validate_openapi_contract


def main() -> int:
    report = validate_openapi_contract(ROOT)
    print(json.dumps({"kind": report.kind, "passed": report.passed, "summary": report.summary, "failures": report.failures}, indent=2))
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
