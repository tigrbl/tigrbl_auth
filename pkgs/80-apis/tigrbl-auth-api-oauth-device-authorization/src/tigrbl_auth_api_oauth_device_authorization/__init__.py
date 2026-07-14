"""RFC 8628 device-authorization HTTP carrier."""

from .binding import (
    DatabaseDependency,
    DeviceAuthorizationTarget,
    build_device_authorization_router,
    include_device_authorization_endpoint,
)

__all__ = [
    "DatabaseDependency",
    "DeviceAuthorizationTarget",
    "build_device_authorization_router",
    "include_device_authorization_endpoint",
]
