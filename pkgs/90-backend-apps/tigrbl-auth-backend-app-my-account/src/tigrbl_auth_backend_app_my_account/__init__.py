"""My Account backend application package for Tigrbl Auth."""

from __future__ import annotations

from .common import MyAccountMutationOut
from .contract import MY_ACCOUNT_BACKEND_APP_CONTRACT, MyAccountBackendAppContract
from .profiles import (
    MyAccountPasswordChangeIn,
    MyAccountProfileOut,
    MyAccountProfileUpdateIn,
)
from .sessions import MyAccountSessionOut

PRODUCT_SURFACE = "my-account-app"


def __getattr__(name: str):
    if name in {"app", "build_app"}:
        from .app import app, build_app

        return app if name == "app" else build_app
    raise AttributeError(name)

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
