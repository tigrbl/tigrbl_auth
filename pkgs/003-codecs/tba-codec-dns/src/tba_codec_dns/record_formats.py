"""Variable-layout DNS record formats."""

import base64
import ipaddress
import socket
from collections.abc import Sequence
from decimal import Decimal, InvalidOperation
from struct import Struct

from tba_primitives_dns_name.names import Name, encode_idna2003, name_text, parse_name

from .tkey import Tkey
from .wire import RecordType, ResourceRecord, WireError, _name_wire, _read_name

_APL = Struct("!HBB")
_HIP = Struct("!BBH")
_LOC = Struct("!4B3I")
_GATEWAY_WIDTH = {0: 0, 1: 4, 2: 16}


def _gateway_from_text(kind: int, text: str, origin: Name) -> bytes:
    if kind == 0 and text == ".":
        return b""
    if kind in (1, 2):
        address = ipaddress.ip_address(text)
        if len(address.packed) == _GATEWAY_WIDTH[kind] and "%" not in text:
            return address.packed
    if kind == 3:
        return _name_wire(parse_name(text, origin))
    raise ValueError("invalid DNS relay or gateway")


def _gateway_from_wire(kind: int, data: bytes, offset: int) -> tuple[str, int]:
    if kind == 3:
        name, end = _read_name(data, offset, canonical=False, compress=False)
        return name_text(name), end
    width = _GATEWAY_WIDTH.get(kind)
    if width is None or offset + width > len(data):
        raise WireError("invalid DNS relay or gateway length")
    return (
        "." if width == 0 else str(ipaddress.ip_address(data[offset : offset + width]))
    ), offset + width


def _decimal(text: str, limit: int) -> int:
    if not text.isascii() or not text.isdecimal() or int(text) > limit:
        raise ValueError("DNS integer out of range")
    return int(text)


def _loc_decimal(token: str) -> Decimal:
    try:
        value = Decimal(token)
        if value.is_finite():
            return value
    except InvalidOperation:
        pass
    raise ValueError("invalid DNS LOC measurement")


def _loc_angle(parts: Sequence[str], hemispheres: str, maximum: int) -> int:
    if not 2 <= len(parts) <= 4 or parts[-1].upper() not in tuple(hemispheres):
        raise ValueError("malformed DNS LOC angle")
    degrees = _decimal(parts[0], maximum)
    minutes = _decimal(parts[1], 59) if len(parts) >= 3 else 0
    seconds = _loc_decimal(parts[2]) if len(parts) == 4 else Decimal(0)
    if not 0 <= seconds < 60 or (degrees == maximum and (minutes or seconds)):
        raise ValueError("DNS LOC angle exceeds its range")
    distance = int((degrees * 3600 + minutes * 60 + seconds) * 1000)
    return 2**31 + (distance if parts[-1].upper() == hemispheres[0] else -distance)


def _loc_distance(token: str) -> int:
    return int(_loc_decimal(token.lower().removesuffix("m")) * 100)


def _precision(centimeters: int) -> int:
    if not 0 <= centimeters <= 9 * 10**9:
        raise ValueError("DNS LOC size or precision exceeds its range")
    exponent = 0
    while centimeters > 9:
        centimeters //= 10
        exponent += 1
    return (centimeters << 4) | exponent


def _loc_text(number: int, hemispheres: str) -> tuple[str, ...]:
    offset = number - 2**31
    degrees, rest = divmod(abs(offset), 3_600_000)
    minutes, rest = divmod(rest, 60_000)
    seconds = Decimal(rest) / 1000
    return str(degrees), str(minutes), str(seconds), hemispheres[int(offset < 0)]


def _to_loc(tokens: Sequence[str]) -> bytes:
    latitude_end = next(
        (i + 1 for i, x in enumerate(tokens) if x.upper() in ("N", "S")), 0
    )
    longitude_end = next(
        (i + 1 for i, x in enumerate(tokens) if x.upper() in ("E", "W")), 0
    )
    if not latitude_end < longitude_end or not 1 <= len(tokens) - longitude_end <= 4:
        raise ValueError("LOC requires latitude, longitude, and altitude")
    latitude = _loc_angle(tokens[:latitude_end], "NS", 90)
    longitude = _loc_angle(tokens[latitude_end:longitude_end], "EW", 180)
    altitude = _loc_distance(tokens[longitude_end]) + 10_000_000
    if not 0 <= altitude <= 0xFFFFFFFF:
        raise ValueError("DNS LOC altitude exceeds its range")
    values = [_loc_distance(token) for token in tokens[longitude_end + 1 :]]
    defaults = [100, 1_000_000, 1000]
    defaults[: len(values)] = values
    return _LOC.pack(0, *map(_precision, defaults), latitude, longitude, altitude)


def _from_loc(data: bytes) -> tuple[str, ...]:
    if len(data) != _LOC.size:
        raise WireError("invalid DNS LOC record length")
    version, size, horiz, vert, lat, lon, altitude = _LOC.unpack(data)
    if version or abs(lat - 2**31) > 324_000_000 or abs(lon - 2**31) > 648_000_000:
        raise WireError("invalid DNS LOC version or coordinates")

    def meters(value: int) -> str:
        return str(Decimal(value) / 100) + "m"

    precisions = []
    for value in (size, horiz, vert):
        mantissa, power = divmod(value, 16)
        if mantissa > 9 or power > 9:
            raise WireError("invalid DNS LOC precision")
        precisions.append(meters(mantissa * 10**power))
    return (
        *_loc_text(lat, "NS"),
        *_loc_text(lon, "EW"),
        meters(altitude - 10_000_000),
        *precisions,
    )


def _to_apl(tokens: Sequence[str]) -> bytes:
    output = bytearray()
    for token in tokens:
        flag = token.startswith("!")
        family, rest = token.removeprefix("!").split(":", 1)
        address, prefix = rest.rsplit("/", 1)
        number = _decimal(family, 65535)
        bits = _decimal(prefix, 255)
        if number in (1, 2):
            spec = ipaddress.ip_network(f"{address}/{bits}", strict=False)
            if spec.version != (4 if number == 1 else 6):
                raise ValueError("mismatched DNS APL family")
            octets = spec.network_address.packed.rstrip(b"\0")
        else:
            octets = bytes.fromhex(address)
        if len(octets) > 127:
            raise ValueError("DNS APL address exceeds limit")
        output.extend(_APL.pack(number, bits, len(octets) | (0x80 if flag else 0)))
        output.extend(octets)
    return bytes(output)


def _from_apl(data: bytes) -> tuple[str, ...]:
    offset = 0
    items = []
    while offset < len(data):
        if offset + _APL.size > len(data):
            raise WireError("truncated APL item")
        family, prefix, flags = _APL.unpack_from(data, offset)
        size = flags & 0x7F
        start = offset + _APL.size
        offset = start + size
        width = {1: 4, 2: 16}.get(family)
        if offset > len(data) or (
            width is not None and (size > width or prefix > width * 8)
        ):
            raise WireError("invalid APL address length")
        address = data[start:offset]
        if width is not None:
            address = str(ipaddress.ip_address(address.ljust(width, b"\0")))
        else:
            address = address.hex()
        items.append(f"{'!' if flags & 0x80 else ''}{family}:{address}/{prefix}")
    return tuple(items)


KINDS = frozenset(
    {
        RecordType.APL,
        RecordType.LOC,
        RecordType.IPSECKEY,
        RecordType.HIP,
        RecordType.AMTRELAY,
        RecordType.WKS,
        RecordType.TKEY,
    }
)


def parse_special(
    kind: int, args: Sequence[str], origin: Name, *, encode_label=encode_idna2003
) -> bytes:
    if kind == RecordType.LOC:
        return _to_loc(args)
    if kind == RecordType.APL:
        return _to_apl(args)
    if kind == RecordType.WKS:
        if len(args) < 2:
            raise ValueError("WKS requires an address and IP protocol")
        address = ipaddress.IPv4Address(args[0]).packed
        protocol = {"tcp": 6, "udp": 17}.get(args[1].lower())
        if protocol is None:
            protocol = _decimal(args[1], 255)
        bitmap = bytearray()
        for token in args[2:]:
            if token.isascii() and token.isdecimal():
                port = _decimal(token, 65535)
            else:
                proto_name = {6: "tcp", 17: "udp"}.get(protocol)
                if not proto_name:
                    raise ValueError("WKS service names require TCP or UDP")
                try:
                    port = socket.getservbyname(token, proto_name)
                except OSError as exc:
                    raise ValueError("unknown WKS service name") from exc
            octet, bit = divmod(port, 8)
            if octet >= len(bitmap):
                bitmap.extend(b"\0" * (octet + 1 - len(bitmap)))
            bitmap[octet] |= 0x80 >> bit
        return address + bytes((protocol,)) + bitmap
    if kind == RecordType.TKEY:
        if not 6 <= len(args) <= 7:
            raise ValueError("TKEY requires an algorithm, times, mode, error, and key")
        algorithm, inception, expiration, mode, error, token, *other = args
        key = b"" if token == "-" else base64.b64decode(token, validate=True)
        data = (
            b""
            if not other or other[0] == "-"
            else base64.b64decode(other[0], validate=True)
        )
        return Tkey(
            parse_name(algorithm, origin, encode_label=encode_label),
            _decimal(inception, 0xFFFFFFFF),
            _decimal(expiration, 0xFFFFFFFF),
            _decimal(mode, 65535),
            _decimal(error, 65535),
            key,
            data,
        ).to_wire()
    if kind == RecordType.HIP:
        if len(args) < 3:
            raise ValueError("HIP requires an algorithm, HIT, and key")
        algorithm = _decimal(args[0], 255)
        hit = bytes.fromhex(args[1])
        key = base64.b64decode(args[2], validate=True)
        return (
            _HIP.pack(len(hit), algorithm, len(key))
            + hit
            + key
            + b"".join(
                _name_wire(parse_name(name, origin, encode_label=encode_label))
                for name in args[3:]
            )
        )
    if len(args) < 4:
        raise ValueError("relay or gateway record is incomplete")
    precedence = _decimal(args[0], 255)
    if kind == RecordType.AMTRELAY:
        if len(args) != 4:
            raise ValueError("AMTRELAY takes four fields")
        optional, relay = _decimal(args[1], 1), _decimal(args[2], 127)
        return bytes((precedence, (optional << 7) | relay)) + _gateway_from_text(
            relay, args[3], origin
        )
    gateway, algorithm = _decimal(args[1], 3), _decimal(args[2], 255)
    public = "".join(args[4:])
    key = b"" if public == "." else base64.b64decode(public, validate=True)
    return (
        bytes((precedence, gateway, algorithm))
        + _gateway_from_text(gateway, args[3], origin)
        + key
    )


def special_fields(record: ResourceRecord) -> tuple[str, ...]:
    data = record.data
    if record.type == RecordType.LOC:
        return _from_loc(data)
    if record.type == RecordType.APL:
        return _from_apl(data)
    if record.type == RecordType.WKS:
        if not 5 <= len(data) <= 8197:
            raise WireError("invalid WKS record size")
        ports = [
            str(octet * 8 + bit)
            for octet, value in enumerate(data[5:])
            for bit in range(8)
            if value & (128 >> bit)
        ]
        return (str(ipaddress.IPv4Address(data[:4])), str(data[4]), *ports)
    if record.type == RecordType.TKEY:
        tkey = Tkey.from_wire(data)
        return (
            name_text(tkey.algorithm),
            *map(str, (tkey.inception, tkey.expiration, tkey.mode, tkey.error)),
            base64.b64encode(tkey.key).decode("ascii") or "-",
            base64.b64encode(tkey.other).decode("ascii") or "-",
        )
    if record.type == RecordType.HIP:
        if len(data) < _HIP.size:
            raise WireError("truncated HIP record")
        hit_size, algorithm, key_size = _HIP.unpack_from(data)
        hit_end = _HIP.size + hit_size
        offset = hit_end + key_size
        if offset > len(data):
            raise WireError("truncated HIP public key")
        names = []
        while offset < len(data):
            name, offset = _read_name(data, offset, canonical=False, compress=False)
            names.append(name_text(name))
        return (
            str(algorithm),
            data[_HIP.size : hit_end].hex().upper(),
            base64.b64encode(data[hit_end : hit_end + key_size]).decode("ascii"),
            *names,
        )
    if record.type == RecordType.AMTRELAY:
        if len(data) < 2:
            raise WireError("truncated AMTRELAY record")
        gateway, end = _gateway_from_wire(data[1] & 127, data, 2)
        if end != len(data):
            raise WireError("trailing AMTRELAY data")
        return str(data[0]), str(data[1] >> 7), str(data[1] & 127), gateway
    if len(data) < 3:
        raise WireError("truncated IPSECKEY record")
    gateway, end = _gateway_from_wire(data[1], data, 3)
    key = base64.b64encode(data[end:]).decode("ascii") or "."
    return (*map(str, data[:3]), gateway, key)
