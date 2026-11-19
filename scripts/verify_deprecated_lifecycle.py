"""Validate deprecated lifecycle placement and verified graveyard receipts."""

import json
from deprecated_lifecycle import verify

if __name__ == "__main__":
    report = verify()
    print(json.dumps(report, indent=2))
    raise SystemExit(not report["passed"])
