"""Translate E.164 telephone numbers to and from ENUM owner names."""

from .name import Name, from_text

e164_domain = from_text("e164.arpa.")


def from_e164(text: str, origin: Name | None = e164_domain) -> Name:
    digits = [
        digit.encode("ascii") for digit in text if digit.isascii() and digit.isdecimal()
    ]
    if not 1 <= len(digits) <= 15:
        raise ValueError("E.164 numbers require one to fifteen ASCII digits")
    relative = Name(reversed(digits))
    return relative if origin is None else relative.concatenate(origin)


def to_e164(
    name: Name, origin: Name | None = e164_domain, want_plus_prefix: bool = True
) -> str:
    if origin is not None:
        if not name.is_subdomain(origin):
            raise ValueError("DNS name is outside the ENUM origin")
        name = name.relativize(origin)
    if not 1 <= len(name) <= 15 or any(
        len(label) != 1 or not label.isdigit() for label in name
    ):
        raise ValueError("invalid E.164 DNS name")
    return ("+" if want_plus_prefix else "") + b"".join(reversed(name.labels)).decode(
        "ascii"
    )
