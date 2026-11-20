from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SdJwtSerialization:
    issuer_jwt: str
    disclosures: tuple[str, ...]
    key_binding_jwt: str | None = None

    def serialize(self) -> str:
        components = [self.issuer_jwt, *self.disclosures]
        if self.key_binding_jwt is not None:
            components.append(self.key_binding_jwt)
        return "~".join(components) + "~"


def parse_sd_jwt_serialization(value: str) -> SdJwtSerialization:
    parts = value.split("~")
    if not parts or parts[0].count(".") != 2:
        raise ValueError("SD-JWT must begin with a compact issuer JWS")
    tail = [part for part in parts[1:] if part]
    key_binding = tail.pop() if tail and tail[-1].count(".") == 2 else None
    if any(part.count(".") for part in tail):
        raise ValueError("disclosures must be base64url values")
    return SdJwtSerialization(parts[0], tuple(tail), key_binding)


__all__ = ["SdJwtSerialization", "parse_sd_jwt_serialization"]
