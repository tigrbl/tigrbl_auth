from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
root_value = str(ROOT)
if root_value not in sys.path:
    sys.path.insert(0, root_value)
for src in (ROOT / "pkgs").glob("*/src"):
    value = str(src)
    if value not in sys.path:
        sys.path.append(value)
