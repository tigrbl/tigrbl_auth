"""Load the canonical numbered package-layer policy.

The package directory remains the ownership declaration for an individual
package.  ``pkgs/layers.toml`` is the single source for the recognized layer
index and its cross-layer categories.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import tomllib


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_POLICY_PATH = ROOT / "pkgs" / "layers.toml"


@dataclass(frozen=True, slots=True)
class LayerDefinition:
    id: str
    order: int
    category: str
    terminal: bool = False
    javascript: bool = False
    distribution_prefix: str | None = None


@dataclass(frozen=True, slots=True)
class LayerPolicy:
    schema_version: int
    layers: tuple[LayerDefinition, ...]

    @property
    def layer_ids(self) -> tuple[str, ...]:
        return tuple(layer.id for layer in self.layers)

    @property
    def by_id(self) -> dict[str, LayerDefinition]:
        return {layer.id: layer for layer in self.layers}

    @property
    def terminal_layers(self) -> frozenset[str]:
        return frozenset(layer.id for layer in self.layers if layer.terminal)


def load_layer_policy(path: Path = DEFAULT_POLICY_PATH) -> LayerPolicy:
    payload = tomllib.loads(path.read_text(encoding="utf-8"))
    schema_version = payload.get("schema_version")
    if schema_version != 1:
        raise ValueError(f"unsupported package-layer schema: {schema_version!r}")

    raw_layers = payload.get("layers")
    if not isinstance(raw_layers, list) or not raw_layers:
        raise ValueError("package-layer policy must define at least one layer")

    layers = tuple(
        LayerDefinition(
            id=str(item["id"]),
            order=int(item["order"]),
            category=str(item["category"]),
            terminal=bool(item.get("terminal", False)),
            javascript=bool(item.get("javascript", False)),
            distribution_prefix=(
                str(item["distribution_prefix"])
                if item.get("distribution_prefix") is not None
                else None
            ),
        )
        for item in raw_layers
    )
    ids = [layer.id for layer in layers]
    orders = [layer.order for layer in layers]
    if len(ids) != len(set(ids)):
        raise ValueError("package-layer ids must be unique")
    if len(orders) != len(set(orders)):
        raise ValueError("package-layer orders must be unique")
    if tuple(orders) != tuple(sorted(orders)):
        raise ValueError("package layers must be ordered by their numeric order")
    return LayerPolicy(schema_version=schema_version, layers=layers)


def dependency_allowed(
    consumer_layer: str,
    target_layer: str,
    policy: LayerPolicy,
) -> bool:
    """Return whether a terminal-layer dependency is permitted.

    General production-layer rules are enforced by the boundary validator's
    domain-specific guards.  This helper owns the universal terminal rule:
    production cannot consume examples or tests, and examples cannot consume
    test-only packages.
    """

    layers = policy.by_id
    consumer = layers[consumer_layer]
    target = layers[target_layer]
    if not target.terminal:
        return True
    if not consumer.terminal:
        return False
    return not (consumer.category == "example" and target.category == "test")


__all__ = [
    "DEFAULT_POLICY_PATH",
    "LayerDefinition",
    "LayerPolicy",
    "dependency_allowed",
    "load_layer_policy",
]
