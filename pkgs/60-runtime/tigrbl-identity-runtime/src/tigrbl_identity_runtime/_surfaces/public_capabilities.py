from __future__ import annotations

from typing import Any, Final

from ._public_capabilities_core import CORE_PUBLIC_CAPABILITIES
from ._public_capabilities_protocols import PROTOCOL_PUBLIC_CAPABILITIES

PUBLIC_CAPABILITIES: Final[tuple[dict[str, Any], ...]] = (
    *PROTOCOL_PUBLIC_CAPABILITIES,
    *CORE_PUBLIC_CAPABILITIES,
)

