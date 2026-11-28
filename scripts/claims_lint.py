from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tba_auth.cli.claims import run_lint


if __name__ == "__main__":
    raise SystemExit(run_lint(ROOT, strict=True))
