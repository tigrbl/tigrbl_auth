from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tba_auth.cli.runtime import run_runtime_foundation_check


def main() -> int:
    return run_runtime_foundation_check(ROOT, strict=False)


if __name__ == "__main__":
    raise SystemExit(main())
