from dataclasses import dataclass

RFC_REVISION = "RFC 9711"
EAT_MEDIA_TYPES = frozenset({"application/eat+cwt", "application/eat+jwt"})


@dataclass(frozen=True, slots=True)
class EatProfile:
    identifier: str | int

    def __post_init__(self):
        if isinstance(self.identifier, str) and not self.identifier:
            raise ValueError("EAT profile identifier cannot be empty")
        if not isinstance(self.identifier, (str, int)) or isinstance(
            self.identifier, bool
        ):
            raise ValueError("EAT profile must be a URI or OID identifier")


__all__ = ["EAT_MEDIA_TYPES", "RFC_REVISION", "EatProfile"]
