from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tba_auth.cli.project_tree import run_migration_plan_check


if __name__ == '__main__':
    raise SystemExit(run_migration_plan_check(ROOT, strict=True))
