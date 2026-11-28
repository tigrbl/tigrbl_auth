from __future__ import annotations

import asyncio
import types
from contextlib import suppress

import pytest

from tba_auth.config.deployment import resolve_deployment
from tba_auth.runtime import build_runtime_plan, get_runner_adapter


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


@pytest.mark.integration
def test_tigrcorn_runner_profile_contract_can_launch_via_supported_adapter(monkeypatch: pytest.MonkeyPatch) -> None:
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

    plan = build_runtime_plan(
        deployment=resolve_deployment(profile="baseline", runtime_style="standalone"),
        runner="tigrcorn",
        environment="test",
        host="127.0.0.1",
        port=8042,
        workers=1,
        access_log=False,
        graceful_timeout=0,
    )
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
