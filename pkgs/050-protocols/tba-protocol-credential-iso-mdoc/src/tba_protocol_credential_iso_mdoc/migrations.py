from typing import Mapping

from .versions import CURRENT_VERSION


def migrate_document(value: Mapping[str, object], *, source: str) -> dict[str, object]:
    if source != CURRENT_VERSION.value:
        raise ValueError(f"no ISO mdoc migration path from {source}")
    return dict(value)


__all__ = ["migrate_document"]
