from __future__ import annotations

import asyncio
import importlib
import importlib.util
from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any, TYPE_CHECKING

from .types import ASGIApp, Receive, RunnerCapability, RunnerFlagMetadata, RuntimeDiagnostic, Scope, Send

if TYPE_CHECKING:
    from .plan import RuntimePlan


class LazyASGIApplication:
    """Materialize an ASGI app only when the runtime actually calls it.

    This keeps package imports lightweight for governance/reporting workflows in
    environments where the full Tigrbl runtime dependency set is not installed.

    The wrapper also proxies attribute access to the materialized application so
    test and operator workflows can interact with ``app.router`` / ``app.state``
    / ``app.openapi()`` without eagerly constructing the runtime during import.
    """

    def __init__(self, factory: Callable[[], ASGIApp]):
        self._factory = factory
        self._app: ASGIApp | None = None

    def materialize(self) -> ASGIApp:
        if self._app is None:
            self._app = self._factory()
        return self._app

    def __getattr__(self, name: str) -> Any:
        if name.startswith("__"):
            raise AttributeError(name)
        return getattr(self.materialize(), name)

    def __dir__(self) -> list[str]:
        return sorted(set(super().__dir__()) | set(dir(self.materialize())))

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        await self.materialize()(scope, receive, send)


class RunnerAdapter(ABC):
    name: str = "unknown"
    display_name: str = "Unknown"
    module_candidates: tuple[str, ...] = ()
    capabilities: tuple[RunnerCapability, ...] = ()
    flag_metadata: tuple[RunnerFlagMetadata, ...] = ()

    def available_module_name(self) -> str | None:
        for module_name in self.module_candidates:
            try:
                spec = importlib.util.find_spec(module_name)
            except (ImportError, ModuleNotFoundError):
                spec = None
            if spec is not None:
                return module_name
        return None

    def is_available(self) -> bool:
        return self.available_module_name() is not None

    def import_module(self):
        module_name = self.available_module_name()
        if module_name is None:
            candidates = ", ".join(self.module_candidates) or self.name
            raise ModuleNotFoundError(f"Runner profile '{self.name}' is not installed; expected one of: {candidates}")
        return importlib.import_module(module_name)

    def base_validation(self, plan: "RuntimePlan") -> tuple[RuntimeDiagnostic, ...]:
        diagnostics: list[RuntimeDiagnostic] = []
        if plan.runtime_style != "standalone":
            diagnostics.append(
                RuntimeDiagnostic(
                    code="runtime-style-not-standalone",
                    level="error",
                    message="Runner-backed runtime plans require standalone runtime style.",
                    runner=self.name,
                    field="runtime_style",
                )
            )
        if plan.runner != self.name:
            diagnostics.append(
                RuntimeDiagnostic(
                    code="runner-mismatch",
                    level="error",
                    message=f"Runtime plan targets runner '{plan.runner}', not '{self.name}'.",
                    runner=self.name,
                    field="runner",
                )
            )
        if not self.is_available():
            diagnostics.append(
                RuntimeDiagnostic(
                    code="runner-not-installed",
                    level="warning",
                    message="Runner adapter is declared but the backing server package is not installed in this environment.",
                    runner=self.name,
                )
            )
        if plan.workers < 1:
            diagnostics.append(
                RuntimeDiagnostic(
                    code="invalid-workers",
                    level="error",
                    message="Worker count must be at least 1.",
                    runner=self.name,
                    field="workers",
                )
            )
        if plan.port < 1 or plan.port > 65535:
            diagnostics.append(
                RuntimeDiagnostic(
                    code="invalid-port",
                    level="error",
                    message="Port must be between 1 and 65535 when UDS is not used.",
                    runner=self.name,
                    field="port",
                )
            )
        if plan.uds and plan.workers > 1:
            diagnostics.append(
                RuntimeDiagnostic(
                    code="uds-workers-advisory",
                    level="warning",
                    message="Multi-worker behavior with UDS depends on the selected runner profile and deployment topology.",
                    runner=self.name,
                    field="workers",
                )
            )
        if plan.lifespan not in {"auto", "on", "off"}:
            diagnostics.append(
                RuntimeDiagnostic(
                    code="invalid-lifespan",
                    level="error",
                    message="Lifespan must be one of auto, on, or off.",
                    runner=self.name,
                    field="lifespan",
                )
            )
        if plan.graceful_timeout < 0:
            diagnostics.append(
                RuntimeDiagnostic(
                    code="invalid-graceful-timeout",
                    level="error",
                    message="Graceful timeout must be zero or greater.",
                    runner=self.name,
                    field="graceful_timeout",
                )
            )
        return tuple(diagnostics)

    def validate(self, plan: "RuntimePlan") -> tuple[RuntimeDiagnostic, ...]:
        return self.base_validation(plan)

    def to_manifest(self) -> dict[str, Any]:
        available_module = self.available_module_name()
        return {
            "name": self.name,
            "display_name": self.display_name,
            "module_candidates": list(self.module_candidates),
            "available_module": available_module,
            "installed": available_module is not None,
            "capabilities": [item.to_manifest() for item in self.capabilities],
            "flag_metadata": [item.to_manifest() for item in self.flag_metadata],
        }

    @abstractmethod
    async def serve(
        self,
        app: ASGIApp,
        plan: "RuntimePlan",
        *,
        shutdown_event: asyncio.Event | None = None,
        startup_callback: Callable[[dict[str, Any]], Any] | None = None,
    ) -> int:
        raise NotImplementedError


__all__ = ["LazyASGIApplication", "RunnerAdapter"]
