"""My Account backend application package for Tigrbl Auth."""

from __future__ import annotations

from .app import PRODUCT_SURFACE, app, build_app
from .common import MyAccountMutationOut
from .contract import MY_ACCOUNT_BACKEND_APP_CONTRACT, MyAccountBackendAppContract
from .profiles import (
    MyAccountPasswordChangeIn,
    MyAccountProfileOut,
    MyAccountProfileUpdateIn,
)
from .sessions import MyAccountSessionOut

__all__ = [
    "MY_ACCOUNT_BACKEND_APP_CONTRACT",
    "MyAccountMutationOut",
    "MyAccountPasswordChangeIn",
    "MyAccountBackendAppContract",
    "MyAccountProfileOut",
    "MyAccountProfileUpdateIn",
    "MyAccountSessionOut",
    "PRODUCT_SURFACE",
    "app",
    "build_app",
]
