from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TrustDomain:
    name: str

    def __post_init__(self) -> None:
        if not self.name or "/" in self.name or self.name != self.name.lower():
            raise ValueError("trust domain must be a lowercase authority name")


@dataclass(frozen=True, slots=True)
class SpiffeId:
    trust_domain: TrustDomain
    path: str

    @classmethod
    def parse(cls, value: str) -> "SpiffeId":
        if not value.startswith("spiffe://"):
            raise ValueError("SPIFFE ID must use the spiffe URI scheme")
        authority, separator, path = value[len("spiffe://") :].partition("/")
        if not authority or not separator or not path or ".." in path.split("/"):
            raise ValueError("SPIFFE ID requires a normalized workload path")
        return cls(TrustDomain(authority), f"/{path}")

    def __str__(self) -> str:
        return f"spiffe://{self.trust_domain.name}{self.path}"


__all__ = ["SpiffeId", "TrustDomain"]
