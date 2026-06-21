from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def enabled_tenant_record(repo_root: Path, tenant_slug: str) -> dict[str, Any] | None:
    record_path = Path(repo_root) / ".operator-state" / "tenant" / f"{tenant_slug}.json"
    if not record_path.exists():
        return None

    record = json.loads(record_path.read_text(encoding="utf-8"))
    if record is None:
        return None

    status = str(record.get("status") or "").lower()
    if status in {"deleted", "disabled", "revoked"}:
        return None
    if record.get("enabled") is False:
        return None
    return record


__all__ = ["enabled_tenant_record"]
