"""Shared backend-application composition APIs."""

from .app import app, build_app, build_application_runtime_plan
from .plugin import TigrblAuthBackendAppPlugin, install
from .product import build_product_app, validate_backend_app_contract

__all__ = [
    "app",
    "build_app",
    "build_application_runtime_plan",
    "TigrblAuthBackendAppPlugin",
    "build_product_app",
    "install",
    "validate_backend_app_contract",
]
