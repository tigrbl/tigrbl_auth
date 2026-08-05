"""Explicit late binding for optional cross-component ORM relationships."""

from __future__ import annotations

from typing import Any

from sqlalchemy.orm import relationship


def bind_relationship(
    *,
    parent: type[Any],
    attribute: str,
    child: type[Any],
    back_attribute: str | None = None,
    **options: Any,
) -> None:
    """Bind an optional child relationship after both components are selected."""

    if hasattr(parent, attribute):
        return
    kwargs = dict(options)
    if back_attribute is not None:
        kwargs["back_populates"] = back_attribute
    setattr(parent, attribute, relationship(child, **kwargs))


__all__ = ["bind_relationship"]
