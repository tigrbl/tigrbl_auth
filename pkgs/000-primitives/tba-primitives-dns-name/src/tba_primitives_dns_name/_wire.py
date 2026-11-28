"""DNS name wire encoding and compression."""

from .names import Name, check_name


class WireError(ValueError):
    """Invalid DNS wire data."""


def _name_wire(labels: Name) -> bytes:
    check_name(labels)
    return b"".join(bytes((len(label),)) + label for label in labels) + b"\x00"


def _append_name(output: bytearray, labels: Name, offsets: dict[Name, int]) -> None:
    check_name(labels)
    for index, label in enumerate(labels):
        suffix = labels[index:]
        pointer = offsets.get(suffix)
        if pointer is not None:
            output.extend((0xC000 | pointer).to_bytes(2, "big"))
            return
        if len(output) < 0x4000:
            offsets[suffix] = len(output)
        output.extend(bytes((len(label),)) + label)
    output.append(0)


def _read_name(
    packet: bytes,
    start: int,
    *,
    canonical: bool = True,
    compress: bool = True,
    pointer_floor: int = 12,
) -> tuple[Name, int]:
    labels = []
    position = start
    end = None
    pointer_limit = start
    size = 1
    while position < len(packet):
        length = packet[position]
        if not length:
            return tuple(labels), position + 1 if end is None else end
        if length & 0xC0 == 0xC0:
            if not compress:
                raise WireError("compression is forbidden in this DNS name")
            if position + 1 >= len(packet):
                break
            target = ((length & 0x3F) << 8) | packet[position + 1]
            if not pointer_floor <= target < pointer_limit:
                raise WireError("invalid DNS compression pointer")
            if end is None:
                end = position + 2
            position = pointer_limit = target
            continue
        if length > 63 or position + 1 + length >= len(packet):
            break
        size += length + 1
        if size > 255:
            raise WireError("DNS name exceeds 255 wire octets")
        label = packet[position + 1 : position + 1 + length]
        labels.append(label.lower() if canonical else label)
        position += length + 1
    raise WireError("invalid or truncated DNS name")
