from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from ..session_service import (
    exchange_token_for_context,
    get_token_for_context,
    introspect_token_for_context,
    list_tokens_for_context,
    revoke_all_tokens_for_context,
    revoke_token_for_context,
)


def parse_token_patch(raw_patch: dict[str, Any] | None) -> dict[str, Any]:
    patch = dict(raw_patch or {})
    patch.setdefault(
        "issued_at",
        patch.get("iat")
        or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    )
    if "token_type" not in patch and "typ" in patch:
        patch["token_type"] = patch["typ"]
    return patch
