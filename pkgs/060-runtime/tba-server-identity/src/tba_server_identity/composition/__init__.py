"""Carrier-neutral identity runtime composition exports."""

from .app import build_application_runtime_plan
from .lifecycle import AssemblyFactory, SurfaceInitializer, register_lifecycle

__all__ = [
    "AssemblyFactory",
    "SurfaceInitializer",
    "build_application_runtime_plan",
    "register_lifecycle",
]
