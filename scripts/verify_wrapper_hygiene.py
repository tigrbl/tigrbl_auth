from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tigrbl_auth.cli.boundary import run_wrapper_hygiene_check


if __name__ == "__main__":
    raise SystemExit(run_wrapper_hygiene_check(ROOT, strict=True, enforce_capability_strictness=True))
