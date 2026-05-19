from __future__ import annotations

import asyncio
import inspect
from typing import Any

from .base import RunnerAdapter
from .types import RunnerCapability, RunnerFlagMetadata, RuntimeDiagnostic


def _call_with_supported_kwargs(target, **kwargs):
    signature = inspect.signature(target)
    accepts_var_kw = any(parameter.kind == inspect.Parameter.VAR_KEYWORD for parameter in signature.parameters.values())
    if accepts_var_kw:
        return target(**kwargs)
    filtered = {key: value for key, value in kwargs.items() if key in signature.parameters}
    return target(**filtered)


class TigrcornRunnerAdapter(RunnerAdapter):
    name = "tigrcorn"
    display_name = "Tigrcorn"
    module_candidates = ("tigrcorn", "tigrbl.tigrcorn")
    capabilities = (
        RunnerCapability("http", "HTTP ASGI serving", portable=True),
        RunnerCapability("websocket", "WebSocket ASGI serving", portable=True),
        RunnerCapability("lifespan", "ASGI lifespan integration", portable=True),
        RunnerCapability("uds", "Unix domain socket binding", portable=True),
        RunnerCapability("workers", "Worker model", portable=True),
        RunnerCapability("runner-contract", "External Tigrcorn adapter contract", portable=False),
    )
    flag_metadata = (
        RunnerFlagMetadata("server", ("--server",), "Select the Tigrcorn runner profile.", portable=True, default="tigrcorn", choices=("tigrcorn",), value_type="choice"),
        RunnerFlagMetadata("host", ("--host",), "Bind host.", portable=True, default="127.0.0.1"),
        RunnerFlagMetadata("port", ("--port",), "Bind port.", portable=True, default=8000, value_type="int"),
        RunnerFlagMetadata("workers", ("--workers",), "Worker count.", portable=True, default=1, value_type="int"),
        RunnerFlagMetadata("uds", ("--uds",), "Unix domain socket path.", portable=True),
        RunnerFlagMetadata("tigrcorn_contract", ("--tigrcorn-contract",), "Preferred Tigrcorn adapter contract.", portable=False, default="auto", choices=("auto", "serve", "run", "server"), value_type="choice"),
        RunnerFlagMetadata("tigrcorn_mode", ("--tigrcorn-mode",), "Preferred Tigrcorn runtime mode hint.", portable=False, default="asgi", choices=("asgi", "auto"), value_type="choice"),
    )

    def validate(self, plan):
        diagnostics = list(self.base_validation(plan))
        contract = str(plan.runner_options.get("tigrcorn_contract", "auto"))
        if contract not in {"auto", "serve", "run", "server"}:
            diagnostics.append(
                RuntimeDiagnostic(
                    code="invalid-tigrcorn-contract",
                    level="error",
                    message="Tigrcorn contract must be one of auto, serve, run, or server.",
                    runner=self.name,
                    field="tigrcorn_contract",
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
        module = self.import_module()
        runner_options = dict(plan.runner_options)
        contract = str(runner_options.get("tigrcorn_contract", "auto"))
        launch_kwargs = {
            "app": app,
            "host": plan.host,
            "port": plan.port,
            "uds": plan.uds,
            "workers": plan.workers,
            "log_level": plan.log_level,
            "access_log": plan.access_log,
            "lifespan": plan.lifespan,
            "proxy_headers": plan.proxy_headers,
            "graceful_timeout": plan.graceful_timeout,
            "shutdown_trigger": shutdown_event.wait if shutdown_event is not None else None,
            "mode": runner_options.get("tigrcorn_mode", "asgi"),
        }
        if startup_callback is not None:
            maybe_result = startup_callback(
                {
                    "runner": self.name,
                    "available_module": self.available_module_name(),
                    "contract": contract,
                    "bind": {"host": plan.host, "port": plan.port, "uds": plan.uds},
                }
            )
            if asyncio.iscoroutine(maybe_result):
                await maybe_result

        if hasattr(module, "serve") and contract in {"auto", "serve"}:
            result = _call_with_supported_kwargs(module.serve, **launch_kwargs)
            if inspect.isawaitable(result):
                await result
            return 0
        if hasattr(module, "run") and contract in {"auto", "run"}:
            result = _call_with_supported_kwargs(module.run, **launch_kwargs)
            if inspect.isawaitable(result):
                await result
            return 0
        if hasattr(module, "Config") and hasattr(module, "Server") and contract in {"auto", "server"}:
            config = _call_with_supported_kwargs(getattr(module, "Config"), **launch_kwargs)
            server = _call_with_supported_kwargs(getattr(module, "Server"), config=config, app=app)
            serve_method = getattr(server, "serve", None)
            if serve_method is None:
                raise RuntimeError("Tigrcorn adapter found Config/Server but no serve() method.")
            result = serve_method()
            if inspect.isawaitable(result):
                await result
            return 0
        raise RuntimeError(
            "Installed Tigrcorn module does not expose a supported adapter contract. "
            "Expected one of: serve(...), run(...), or Config/Server with serve()."
        )


__all__ = ["TigrcornRunnerAdapter"]
