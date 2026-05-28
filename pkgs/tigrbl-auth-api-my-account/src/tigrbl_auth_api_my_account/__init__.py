"""My Account API assembly package for Tigrbl Auth."""

from __future__ import annotations

from .app import PRODUCT_SURFACE, app, build_app
from .contract import MY_ACCOUNT_API_CONTRACT, MyAccountApiContract

__all__ = [
    "MY_ACCOUNT_API_CONTRACT",
    "MyAccountApiContract",
    "PRODUCT_SURFACE",
    "app",
    "build_app",
]
