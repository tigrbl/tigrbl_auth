"""
tigrbl_identity_core.typing
==================

Pure-typing utilities for the AuthN service.
No runtime dependencies outside stdlib.

Key exports
-----------
StrUUID       : Type alias for canonical 36-char UUID strings.
"""

from __future__ import annotations

import uuid
from typing import NewType

# ---------------------------------------------------------------------
# UUID helpers
# ---------------------------------------------------------------------
StrUUID = NewType("StrUUID", str)  # 36-char uuid string, runtime = str


def uuid_str() -> StrUUID:
    """Return a new random UUID *string* in canonical form."""
    return StrUUID(str(uuid.uuid4()))


__all__ = ["StrUUID", "uuid_str"]
