from __future__ import annotations

import asyncio
import socket
import types
from contextlib import suppress
from pathlib import Path

import pytest

from tigrbl_auth.cli.main import build_parser
from tigrbl_auth.cli.reports import generate_state_reports
from tigrbl_auth.config.deployment import resolve_deployment
from tigrbl_auth.runtime import build_runtime_plan, get_runner_adapter

ROOT = Path(__file__).resolve().parents[2]


async def _dummy_asgi_app(scope, receive, send):
    if scope["type"] == "lifespan":
        while True:
            message = await receive()
            if message["type"] == "lifespan.startup":
                await send({"type": "lifespan.startup.complete"})
            elif message["type"] == "lifespan.shutdown":
                await send({"type": "lifespan.shutdown.complete"})
                return
    if scope["type"] == "http":
        await send({"type": "http.response.start", "status": 204, "headers": []})
        await send({"type": "http.response.body", "body": b""})


def _free_port() -> int:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 0))
    port = int(sock.getsockname()[1])
    sock.close()
    return port


def _runtime_plan(runner: str) -> object:
    deployment = resolve_deployment(profile="baseline", runtime_style="standalone")
    return build_runtime_plan(
        deployment=deployment,
        runner=runner,
        environment="test",
        host="127.0.0.1",
        port=_free_port(),
        workers=1,
        access_log=False,
        graceful_timeout=0,
    )


async def _run_with_shutdown(adapter, plan) -> int:
    shutdown_event = asyncio.Event()

    async def _trigger_shutdown() -> None:
        await asyncio.sleep(0.2)
        shutdown_event.set()

    task = asyncio.create_task(_trigger_shutdown())
    try:
        return await adapter.serve(_dummy_asgi_app, plan, shutdown_event=shutdown_event)
    finally:
        task.cancel()
        with suppress(asyncio.CancelledError):
            await task


def test_cli_serve_accepts_portable_and_backend_runtime_flags():
    parser = build_parser()
    args = parser.parse_args(
        [
            "serve",
            "--server",
            "uvicorn",
            "--access-log",
            "--lifespan",
            "on",
            "--graceful-timeout",
            "45",
            "--pid-file",
            "/tmp/tigrbl-auth.pid",
            "--uvicorn-loop",
            "asyncio",
            "--uvicorn-http",
            "h11",
            "--uvicorn-ws",
            "none",
            "--check",
        ]
    )

    assert args.command == "serve"
    assert args.server == "uvicorn"
    assert args.access_log is True
    assert args.lifespan == "on"
    assert args.graceful_timeout == 45
    assert args.pid_file == "/tmp/tigrbl-auth.pid"
    assert args.uvicorn_loop == "asyncio"
    assert args.uvicorn_http == "h11"
    assert args.uvicorn_ws == "none"
    assert args.check is True


@pytest.mark.parametrize("runner", ["uvicorn", "hypercorn"])
def test_installed_runner_profiles_can_launch_dummy_app_live(runner: str):
    adapter = get_runner_adapter(runner)
    if not adapter.is_available():
        pytest.skip(f"{runner} is not installed in this environment")

    plan = _runtime_plan(runner)
    assert asyncio.run(_run_with_shutdown(adapter, plan)) == 0


def test_tigrcorn_adapter_can_launch_dummy_contract(monkeypatch: pytest.MonkeyPatch):
    adapter = get_runner_adapter("tigrcorn")
    calls: dict[str, object] = {}

    async def fake_serve(**kwargs):
        calls.update(kwargs)
        shutdown_trigger = kwargs.get("shutdown_trigger")
        if callable(shutdown_trigger):
            await shutdown_trigger()
        return None

    fake_module = types.SimpleNamespace(serve=fake_serve)
    monkeypatch.setattr(adapter, "available_module_name", lambda: "tigrcorn")
    monkeypatch.setattr(adapter, "import_module", lambda: fake_module)

    plan = _runtime_plan("tigrcorn")
    shutdown_event = asyncio.Event()

    async def _trigger_shutdown() -> None:
        await asyncio.sleep(0)
        shutdown_event.set()

    async def _run() -> int:
        task = asyncio.create_task(_trigger_shutdown())
        try:
            return await adapter.serve(_dummy_asgi_app, plan, shutdown_event=shutdown_event)
        finally:
            task.cancel()
            with suppress(asyncio.CancelledError):
                await task

    assert asyncio.run(_run()) == 0
    assert calls["mode"] == "asgi"
    assert callable(calls["shutdown_trigger"])


def test_state_report_tracks_runtime_launcher_checkpoint():
    payload = generate_state_reports(ROOT)
    summary = payload["current_state"]
    gaps = payload["certification_state"]["open_gaps"]

    assert summary["serve_runtime_launcher_present"] is True
    assert summary["runtime_profile_report_present"] is True
    assert summary["runtime_profile_missing_count"] >= 0
    assert summary["runtime_profile_invalid_count"] >= 0
    assert summary["runtime_profile_ready_count"] >= 0
    runtime_launcher_gap_present = any(
        ("serve operator now launches through runner adapters" in gap)
        or ("runtime validation stack now executes real app-factory" in gap)
        for gap in gaps
    )
    assert runtime_launcher_gap_present or summary["runtime_completion_required_count"] == 0
