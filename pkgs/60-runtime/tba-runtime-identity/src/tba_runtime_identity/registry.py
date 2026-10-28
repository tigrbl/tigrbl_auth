from __future__ import annotations

from .base import RunnerAdapter
from .hypercorn import HypercornRunnerAdapter
from .tigrcorn import TigrcornRunnerAdapter
from .uvicorn import UvicornRunnerAdapter


_ADAPTERS: dict[str, RunnerAdapter] = {
    adapter.name: adapter
    for adapter in (
        UvicornRunnerAdapter(),
        HypercornRunnerAdapter(),
        TigrcornRunnerAdapter(),
    )
}


def get_runner_adapter(name: str) -> RunnerAdapter:
    try:
        return _ADAPTERS[name]
    except KeyError as exc:
        available = ", ".join(sorted(_ADAPTERS))
        raise KeyError(f"Unknown runner profile '{name}'. Registered profiles: {available}") from exc


def iter_runner_adapters() -> tuple[RunnerAdapter, ...]:
    return tuple(_ADAPTERS[name] for name in sorted(_ADAPTERS))


def registered_runner_names() -> tuple[str, ...]:
    return tuple(sorted(_ADAPTERS))


def runner_registry_manifest() -> list[dict[str, object]]:
    return [adapter.to_manifest() for adapter in iter_runner_adapters()]


__all__ = [
    "get_runner_adapter",
    "iter_runner_adapters",
    "registered_runner_names",
    "runner_registry_manifest",
]
