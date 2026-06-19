from __future__ import annotations

import asyncio
from contextlib import suppress

from .base import RunnerAdapter
from .types import RunnerCapability, RunnerFlagMetadata, RuntimeDiagnostic


class HypercornRunnerAdapter(RunnerAdapter):
    name = "hypercorn"
    display_name = "Hypercorn"
    module_candidates = ("hypercorn",)
    capabilities = (
        RunnerCapability("http", "HTTP ASGI serving", portable=True),
        RunnerCapability("websocket", "WebSocket ASGI serving", portable=True),
        RunnerCapability("lifespan", "ASGI lifespan integration", portable=True),
        RunnerCapability("uds", "Unix domain socket binding", portable=True),
        RunnerCapability("workers", "Worker configuration", portable=True),
        RunnerCapability("http2", "HTTP/2 support where configured", portable=False),
    )
    flag_metadata = (
        RunnerFlagMetadata("server", ("--server",), "Select the Hypercorn runner profile.", portable=True, default="hypercorn", choices=("hypercorn",), value_type="choice"),
        RunnerFlagMetadata("host", ("--host",), "Bind host.", portable=True, default="127.0.0.1"),
        RunnerFlagMetadata("port", ("--port",), "Bind port.", portable=True, default=8000, value_type="int"),
        RunnerFlagMetadata("workers", ("--workers",), "Worker count.", portable=True, default=1, value_type="int"),
        RunnerFlagMetadata("uds", ("--uds",), "Unix domain socket path.", portable=True),
        RunnerFlagMetadata("hypercorn_worker_class", ("--hypercorn-worker-class",), "Hypercorn worker class.", portable=False, default="asyncio", choices=("asyncio", "trio", "uvloop"), value_type="choice"),
        RunnerFlagMetadata("hypercorn_http2", ("--hypercorn-http2",), "Enable HTTP/2 ALPN for Hypercorn.", portable=False, default=True, value_type="bool"),
    )

    def validate(self, plan):
        diagnostics = list(self.base_validation(plan))
        if plan.uds and plan.host != "127.0.0.1":
            diagnostics.append(
                RuntimeDiagnostic(
                    code="uds-host-ignored",
                    level="warning",
                    message="Hypercorn ignores the TCP host when a UDS binding is requested.",
                    runner=self.name,
                    field="host",
                )
            )
        return tuple(diagnostics)

    async def serve(
        self,
        app,
        plan,
        *,
        shutdown_event: asyncio.Event | None = None,
        startup_callback=None,
    ) -> int:
        from hypercorn.asyncio import serve
        from hypercorn.config import Config

        config = Config()
        config.bind = [f"unix:{plan.uds}"] if plan.uds else [f"{plan.host}:{plan.port}"]
        config.workers = plan.workers
        config.accesslog = "-" if plan.access_log else None
        config.errorlog = "-"
        config.loglevel = str(plan.log_level).lower()
        config.graceful_timeout = max(float(plan.graceful_timeout), 0.0)
        config.use_reloader = False
        config.worker_class = str(plan.runner_options.get("hypercorn_worker_class", "asyncio"))
        if not bool(plan.runner_options.get("hypercorn_http2", True)):
            config.alpn_protocols = ["http/1.1"]

        shutdown_trigger = shutdown_event.wait if shutdown_event is not None else None
        if startup_callback is not None:
            maybe_result = startup_callback(
                {
                    "runner": self.name,
                    "available_module": self.available_module_name(),
                    "bind": list(config.bind),
                    "worker_class": config.worker_class,
                }
            )
            if asyncio.iscoroutine(maybe_result):
                await maybe_result

        try:
            await serve(app, config, shutdown_trigger=shutdown_trigger, mode="asgi")
            return 0
        finally:
            if shutdown_event is not None and not shutdown_event.is_set():
                shutdown_event.set()
                with suppress(asyncio.CancelledError):
                    await asyncio.sleep(0)


__all__ = ["HypercornRunnerAdapter"]
