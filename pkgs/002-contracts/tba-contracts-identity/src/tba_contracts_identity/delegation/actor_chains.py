from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DelegationActor:
    subject: str
    issuer: str | None = None


@dataclass(frozen=True, slots=True)
class DelegationActorChain:
    actors: tuple[DelegationActor, ...]

    def __post_init__(self) -> None:
        if not self.actors:
            raise ValueError("delegation actor chain cannot be empty")


__all__ = ["DelegationActor", "DelegationActorChain"]
