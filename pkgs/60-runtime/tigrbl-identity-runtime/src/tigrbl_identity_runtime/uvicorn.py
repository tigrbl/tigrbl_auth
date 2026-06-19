from __future__ import annotations

import asyncio
from contextlib import suppress
from typing import Any

from .base import RunnerAdapter
from .types import RunnerCapability, RunnerFlagMetadata


class UvicornRunnerAdapter(RunnerAdapter):
    name = "uvicorn"
    display_name = "Uvicorn"
    module_candidates = ("uvicorn",)
    capabilities = (
        RunnerCapability("http", "HTTP/1.1 ASGI serving", portable=True),
        RunnerCapability("websocket", "WebSocket ASGI serving", portable=True),
        RunnerCapability("lifespan", "ASGI lifespan integration", portable=True),
        RunnerCapability("uds", "Unix domain socket binding", portable=True),
        RunnerCapability("workers", "Process workers", portable=True),
        RunnerCapability("proxy-headers", "Proxy header processing", portable=True),
    )
    flag_metadata = (
        RunnerFlagMetadata("server", ("--server",), "Select the Uvicorn runner profile.", portable=True, default="uvicorn", choices=("uvicorn",), value_type="choice"),
        RunnerFlagMetadata("host", ("--host",), "Bind host.", portable=True, default="127.0.0.1"),
        RunnerFlagMetadata("port", ("--port",), "Bind port.", portable=True, default=8000, value_type="int"),
        RunnerFlagMetadata("workers", ("--workers",), "Worker count.", portable=True, default=1, value_type="int"),
        RunnerFlagMetadata("uds", ("--uds",), "Unix domain socket path.", portable=True),
        RunnerFlagMetadata("proxy_headers", ("--proxy-headers",), "Honor forwarded proxy headers.", portable=True, default=False, value_type="bool"),
        RunnerFlagMetadata("uvicorn_loop", ("--uvicorn-loop",), "Uvicorn event-loop implementation.", portable=False, default="auto", choices=("auto", "asyncio", "uvloop"), value_type="choice"),
        RunnerFlagMetadata("uvicorn_http", ("--uvicorn-http",), "Uvicorn HTTP protocol implementation.", portable=False, default="auto", choices=("auto", "h11", "httptools"), value_type="choice"),
        RunnerFlagMetadata("uvicorn_ws", ("--uvicorn-ws",), "Uvicorn WebSocket implementation.", portable=False, default="auto", choices=("auto", "websockets", "wsproto", "none"), value_type="choice"),
    )

    async def serve(
        self,
        app,
        plan,
        *,
        shutdown_event: asyncio.Event | None = None,
        startup_callback=None,
    ) -> int:
        module = self.import_module()
        runner_options = dict(plan.runner_options)
        config = module.Config(
            app=app,
            host=plan.host,
            port=plan.port,
            uds=plan.uds,
            workers=plan.workers,
            log_level=str(plan.log_level).lower(),
            access_log=bool(plan.access_log),
            lifespan=plan.lifespan,
            proxy_headers=plan.proxy_headers,
            loop=runner_options.get("uvicorn_loop", "auto"),
            http=runner_options.get("uvicorn_http", "auto"),
            ws=runner_options.get("uvicorn_ws", "auto"),
            timeout_graceful_shutdown=plan.graceful_timeout,
        )
        server = module.Server(config)
        if hasattr(server, "install_signal_handlers"):
            server.install_signal_handlers = lambda: None

        watcher: asyncio.Task[Any] | None = None
        if shutdown_event is not None:
            async def _watch_shutdown() -> None:
                await shutdown_event.wait()
                server.should_exit = True
                await asyncio.sleep(max(float(plan.graceful_timeout), 0.0))
                if not getattr(server, "force_exit", False):
                    server.force_exit = True

            watcher = asyncio.create_task(_watch_shutdown())

        if startup_callback is not None:
            maybe_result = startup_callback(
                {
                    "runner": self.name,
                    "available_module": self.available_module_name(),
                    "bind": {"host": plan.host, "port": plan.port, "uds": plan.uds},
                }
            )
            if asyncio.iscoroutine(maybe_result):
                await maybe_result

        try:
            await server.serve()
            return 0
        finally:
            if watcher is not None:
                watcher.cancel()
                with suppress(asyncio.CancelledError):
                    await watcher


__all__ = ["UvicornRunnerAdapter"]
