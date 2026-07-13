"""My Account API assembly package for Tigrbl Auth."""

from __future__ import annotations

from .app import PRODUCT_SURFACE, app, build_app
from .common import MyAccountMutationOut
from .contract import MY_ACCOUNT_API_CONTRACT, MyAccountApiContract
from .profiles import (
    MyAccountPasswordChangeIn,
    MyAccountProfileOut,
    MyAccountProfileUpdateIn,
)
from .sessions import MyAccountSessionOut

__all__ = [
    "MY_ACCOUNT_API_CONTRACT",
    "MyAccountMutationOut",
    "MyAccountPasswordChangeIn",
    "MyAccountApiContract",
    "MyAccountProfileOut",
    "MyAccountProfileUpdateIn",
    "MyAccountSessionOut",
    "PRODUCT_SURFACE",
    "app",
    "build_app",
]
