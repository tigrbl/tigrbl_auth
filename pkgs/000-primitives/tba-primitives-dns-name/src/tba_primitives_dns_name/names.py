"""DNS presentation names and octet escapes."""

from collections.abc import Callable

Name = tuple[bytes, ...]
ROOT: Name = ()
_DOTS = ".\u3002\uff0e\uff61"


def check_name(name: Name) -> Name:
    if any(not 1 <= len(label) <= 63 for label in name):
        raise ValueError("invalid DNS label length")
    if sum(len(label) + 1 for label in name) > 254:
        raise ValueError("DNS name exceeds 255 wire octets")
    return name


def _escape(text: str, offset: int) -> tuple[bytes, int]:
    if offset >= len(text):
        raise ValueError("unfinished DNS escape")
    char = text[offset]
    if not char.isascii() or not char.isdecimal():
        return char.encode("utf-8"), offset + 1
    digits = text[offset : offset + 3]
    if (
        len(digits) != 3
        or not digits.isascii()
        or not digits.isdecimal()
        or int(digits) > 255
    ):
        raise ValueError("DNS numeric escape must contain three digits in 000..255")
    return bytes((int(digits),)), offset + 3


def encode_idna2003(label: str) -> bytes:
    return label.encode("idna")


def encode_idna2008(label: str) -> bytes:
    import idna

    return idna.encode(label, uts46=True)


def parse_name(
    text: str,
    origin: Name = ROOT,
    *,
    canonical: bool = False,
    encode_label: Callable[[str], bytes] = encode_idna2003,
) -> Name:
    """Parse a name relative to origin, handling escaped label separators."""
    if text == "@":
        return origin
    if len(text) == 1 and text in _DOTS:
        return ROOT
    labels = []
    label = bytearray()
    start = offset = 0
    escaped = False
    while offset < len(text):
        char = text[offset]
        if char == "\\":
            part, offset = _escape(text, offset + 1)
            label.extend(part)
            escaped = True
            continue
        if char in _DOTS:
            labels.append(bytes(label) if escaped else encode_label(text[start:offset]))
            label.clear()
            start = offset + 1
            escaped = False
        else:
            label.extend(char.encode("utf-8"))
        offset += 1
    if start < offset:
        labels.append(bytes(label) if escaped else encode_label(text[start:]))
        labels.extend(origin)
    elif not labels:
        raise ValueError("empty DNS name")
    if canonical:
        labels = [part.lower() for part in labels]
    return check_name(tuple(labels))


def parse_string(text: str) -> bytes:
    if text.startswith('"') and text.endswith('"') and len(text) >= 2:
        text = text[1:-1]
    output = bytearray()
    offset = 0
    while offset < len(text):
        if text[offset] == "\\":
            part, offset = _escape(text, offset + 1)
            output.extend(part)
        else:
            output.extend(text[offset].encode("utf-8"))
            offset += 1
    return bytes(output)


def _print_octets(data: bytes, specials: bytes) -> str:
    return "".join(
        f"\\{byte:03d}"
        if not 32 <= byte <= 126
        else "\\" + chr(byte)
        if byte in specials
        else chr(byte)
        for byte in data
    )


def name_text(name: Name) -> str:
    if not name:
        return "."
    return ".".join(_print_octets(label, b' .;\\()"@$') for label in name) + "."


def string_text(data: bytes) -> str:
    return '"' + _print_octets(data, b'"\\') + '"'


def is_subdomain(name: Name, origin: Name) -> bool:
    return not origin or tuple(x.lower() for x in name[-len(origin) :]) == tuple(
        x.lower() for x in origin
    )


def canonical_order(name: Name) -> tuple[bytes, ...]:
    return tuple(label.lower() for label in reversed(name))


def relativize(name: Name, origin: Name) -> Name:
    if not is_subdomain(name, origin):
        raise ValueError("name is outside the DNS origin")
    return name[: len(name) - len(origin)]


def concatenate(prefix: Name, suffix: Name) -> Name:
    return check_name(prefix + suffix)


def parent(name: Name) -> Name:
    if not name:
        raise ValueError("the DNS root has no parent")
    return name[1:]


def common_ancestor(left: Name, right: Name) -> Name:
    length = 0
    for a, b in zip(reversed(left), reversed(right)):
        if a.lower() != b.lower():
            break
        length += 1
    return left[len(left) - length :]


def is_absolute_text(name: str) -> bool:
    if not name or name[-1] not in _DOTS:
        return False
    prefix = name[:-1]
    return (len(prefix) - len(prefix.rstrip("\\"))) % 2 == 0


def normalize_domain(domain: str) -> str:
    """Normalize an IDNA hostname for use in application protocols."""
    import idna

    try:
        return idna.encode(
            domain.removesuffix("."), uts46=True, std3_rules=True
        ).decode()
    except (idna.IDNAError, UnicodeError) as exc:
        raise ValueError("invalid DNS domain") from exc
