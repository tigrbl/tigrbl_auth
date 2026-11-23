from __future__ import annotations

import asyncio
import socket
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


def _free_port() -> int:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 0))
    port = int(sock.getsockname()[1])
    sock.close()
    return port


async def _run_with_shutdown(adapter, plan):
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


@pytest.mark.integration
def test_hypercorn_runner_profile_can_launch_dummy_asgi_application() -> None:
    adapter = get_runner_adapter("hypercorn")
    if not adapter.is_available():
        pytest.skip("hypercorn is not installed in this environment")
    plan = build_runtime_plan(
        deployment=resolve_deployment(profile="baseline", runtime_style="standalone"),
        runner="hypercorn",
        environment="test",
        host="127.0.0.1",
        port=_free_port(),
        workers=1,
        access_log=False,
        graceful_timeout=0,
    )
    assert asyncio.run(_run_with_shutdown(adapter, plan)) == 0
    assert any(meta.name == "hypercorn_worker_class" for meta in adapter.flag_metadata)
