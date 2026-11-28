from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tba_auth.migrations import apply_all_async, verify_schema_async


async def _main() -> int:
    apply_result = await apply_all_async()
    verification = await verify_schema_async()
    payload = {
        "apply": apply_result.__dict__,
        "verify": verification.__dict__,
    }
    print(json.dumps(payload, indent=2))
    return 0 if verification.passed else 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(_main()))
