"""Load and evaluate the canonical numbered package-layer policy."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
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
class DependencyRule:
    consumer_layer: str
    allowed_target_layers: frozenset[str]


@dataclass(frozen=True, slots=True)
class DependencyException:
    consumer: str
    target: str
    reason: str


@dataclass(frozen=True, slots=True)
class LayerPolicy:
    schema_version: int
    layers: tuple[LayerDefinition, ...]
    dependency_rules: tuple[DependencyRule, ...]
    dependency_exceptions: tuple[DependencyException, ...] = ()

    @property
    def layer_ids(self) -> tuple[str, ...]:
        return tuple(layer.id for layer in self.layers)

    @property
    def by_id(self) -> dict[str, LayerDefinition]:
        return {layer.id: layer for layer in self.layers}

    @property
    def rules_by_consumer(self) -> dict[str, DependencyRule]:
        return {rule.consumer_layer: rule for rule in self.dependency_rules}

    @property
    def exception_pairs(self) -> frozenset[tuple[str, str]]:
        return frozenset((item.consumer, item.target) for item in self.dependency_exceptions)

    @property
    def terminal_layers(self) -> frozenset[str]:
        return frozenset(layer.id for layer in self.layers if layer.terminal)


def _normalize_distribution(value: str) -> str:
    return re.sub(r"[-_.]+", "-", value).lower()


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
            distribution_prefix=(str(item["distribution_prefix"]) if item.get("distribution_prefix") is not None else None),
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

    raw_rules = payload.get("dependency_rules")
    if not isinstance(raw_rules, list) or not raw_rules:
        raise ValueError("package-layer policy must define dependency rules")
    rules = tuple(
        DependencyRule(
            consumer_layer=str(item["consumer_layer"]),
            allowed_target_layers=frozenset(str(value) for value in item["allowed_target_layers"]),
        )
        for item in raw_rules
    )
    consumers = [rule.consumer_layer for rule in rules]
    if len(consumers) != len(set(consumers)):
        raise ValueError("dependency-rule consumers must be unique")
    if set(consumers) != set(ids):
        raise ValueError("dependency rules must cover every package layer exactly once")
    unknown_targets = set().union(*(rule.allowed_target_layers for rule in rules)) - set(ids)
    if unknown_targets:
        raise ValueError(f"dependency rules name unknown target layers: {sorted(unknown_targets)}")

    exceptions = tuple(
        DependencyException(
            consumer=_normalize_distribution(str(item["consumer"])),
            target=_normalize_distribution(str(item["target"])),
            reason=str(item["reason"]),
        )
        for item in payload.get("dependency_exceptions", ())
    )
    pairs = [(item.consumer, item.target) for item in exceptions]
    if len(pairs) != len(set(pairs)):
        raise ValueError("dependency exceptions must be unique")
    return LayerPolicy(schema_version, layers, rules, exceptions)


def classify_layer(path: Path, policy: LayerPolicy, packages_root: Path | None = None) -> str:
    """Classify a package path from its authoritative numbered directory."""
    candidate = path.resolve()
    root = (packages_root or ROOT / "pkgs").resolve()
    try:
        relative = candidate.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"path is outside package root: {path}") from exc
    if not relative.parts or relative.parts[0] not in policy.by_id:
        raise ValueError(f"unknown package layer for path: {path}")
    return relative.parts[0]


def dependency_allowed(consumer_layer: str, target_layer: str, policy: LayerPolicy) -> bool:
    try:
        return target_layer in policy.rules_by_consumer[consumer_layer].allowed_target_layers
    except KeyError as exc:
        raise ValueError(f"unknown dependency layer: {exc.args[0]}") from exc


def package_dependency_allowed(
    consumer: str, consumer_layer: str, target: str, target_layer: str, policy: LayerPolicy
) -> bool:
    if dependency_allowed(consumer_layer, target_layer, policy):
        return True
    return (_normalize_distribution(consumer), _normalize_distribution(target)) in policy.exception_pairs


__all__ = [
    "DEFAULT_POLICY_PATH",
    "DependencyException",
    "DependencyRule",
    "LayerDefinition",
    "LayerPolicy",
    "classify_layer",
    "dependency_allowed",
    "load_layer_policy",
    "package_dependency_allowed",
]
