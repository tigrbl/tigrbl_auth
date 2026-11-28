from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tba_auth.cli.artifacts import deployment_from_options
from tba_auth.cli.reports import build_evidence_bundle


def main() -> int:
    path = build_evidence_bundle(ROOT, deployment_from_options(profile="baseline"), tier="3", profile_label="baseline")
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
