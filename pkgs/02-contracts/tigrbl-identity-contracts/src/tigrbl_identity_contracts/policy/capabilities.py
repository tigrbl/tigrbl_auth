from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PolicyServiceCapabilities:
    evaluation: bool = True
    search: bool = False
    entity_types: tuple[str, ...] = ()


__all__ = ["PolicyServiceCapabilities"]
