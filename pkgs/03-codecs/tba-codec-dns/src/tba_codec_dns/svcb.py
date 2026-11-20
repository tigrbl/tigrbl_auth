"""SVCB and HTTPS resource data (RFC 9460 and registered parameters)."""

import base64
import ipaddress
import re
from collections.abc import Sequence
from dataclasses import dataclass
from struct import Struct

from tba_primitives_dns_name.names import (
    Name,
    name_text,
    parse_name,
    parse_string,
    string_text,
)

from .wire import ResourceRecord, WireError, _name_wire, _read_name

_H = Struct("!H")
_HEADER = Struct("!HH")
_KEYS = {
    "mandatory": 0,
    "alpn": 1,
    "no-default-alpn": 2,
    "port": 3,
    "ipv4hint": 4,
    "ech": 5,
    "ipv6hint": 6,
    "dohpath": 7,
    "ohttp": 8,
    "docpath": 10,
}
_NAMES = {value: key for key, value in _KEYS.items()}
_NUMBER = re.compile(r"key([0-9]+)")


def _key(text: str) -> int:
    if text in _KEYS:
        return _KEYS[text]
    match = _NUMBER.fullmatch(text)
    if match is None or int(match[1]) >= 65535:
        raise ValueError(f"invalid SVCB parameter key {text!r}")
    return int(match[1])


def _name(key: int) -> str:
    return _NAMES.get(key, f"key{key}")


def _alpn_parts(data: bytes) -> tuple[bytes, ...]:
    parts = []
    offset = 0
    while offset < len(data):
        end = offset + 1 + data[offset]
        if end == offset + 1 or end > len(data):
            raise WireError("invalid SVCB ALPN identifier length")
        parts.append(data[offset + 1 : end])
        offset = end
    if not parts:
        raise WireError("SVCB ALPN list cannot be empty")
    return tuple(parts)


def _alpn_text(data: bytes) -> str:
    escaped = (
        part.replace(b"\\", b"\\\\").replace(b",", b"\\,") for part in _alpn_parts(data)
    )
    return string_text(b",".join(escaped))


def _parse_alpn(data: bytes) -> bytes:
    parts = [bytearray()]
    escaped = False
    for byte in data:
        if escaped:
            if byte not in (44, 92):
                raise ValueError("invalid escape in SVCB ALPN list")
            parts[-1].append(byte)
            escaped = False
        elif byte == 92:
            escaped = True
        elif byte == 44:
            parts.append(bytearray())
        else:
            parts[-1].append(byte)
    if escaped or any(not 1 <= len(part) <= 255 for part in parts):
        raise ValueError("invalid SVCB ALPN identifier")
    return b"".join(bytes((len(part),)) + part for part in parts)


def _param_data(key: int, raw: bytes) -> bytes:
    if key == 0:
        required = sorted(_key(token) for token in raw.decode("ascii").split(","))
        return b"".join(_H.pack(value) for value in required)
    if key == 1:
        return _parse_alpn(raw)
    if key == 3:
        if not raw.isdigit() or not 0 <= int(raw) <= 65535:
            raise ValueError("invalid SVCB port")
        return _H.pack(int(raw))
    if key in (4, 6):
        family = ipaddress.IPv4Address if key == 4 else ipaddress.IPv6Address
        tokens = raw.decode("ascii").split(",")
        if any("%" in token for token in tokens):
            raise ValueError("SVCB hints require unscoped addresses")
        return b"".join(family(token).packed for token in tokens)
    if key == 5:
        return base64.b64decode(raw, validate=True)
    return raw


def _param_text(key: int, raw: bytes) -> str:
    if key == 0:
        return ",".join(_name(value) for (value,) in _H.iter_unpack(raw))
    if key == 1:
        return _alpn_text(raw)
    if key == 3:
        return str(_H.unpack(raw)[0])
    if key in (4, 6):
        width = 4 if key == 4 else 16
        return ",".join(
            str(ipaddress.ip_address(raw[offset : offset + width]))
            for offset in range(0, len(raw), width)
        )
    if key == 5:
        return base64.b64encode(raw).decode("ascii")
    return string_text(raw)


@dataclass(frozen=True)
class ServiceBinding:
    priority: int
    target: Name
    params: tuple[tuple[int, bytes], ...] = ()

    def __post_init__(self) -> None:
        keys = [key for key, _ in self.params]
        if (
            not 0 <= self.priority <= 65535
            or keys != sorted(set(keys))
            or any(not 0 <= key < 65535 for key in keys)
        ):
            raise WireError("invalid SVCB priority or parameter order")
        values = dict(self.params)
        for key, value in self.params:
            if key == 0:
                if not value or len(value) % 2:
                    raise WireError("invalid SVCB mandatory parameter")
                required = [item for (item,) in _H.iter_unpack(value)]
                if required != sorted(set(required)) or any(
                    item == 0 or item not in values for item in required
                ):
                    raise WireError("invalid or missing required SVCB parameter")
            elif key == 1:
                _alpn_parts(value)
            elif key in (2, 8) and value:
                raise WireError("unexpected value for empty SVCB parameter")
            elif key == 3 and len(value) != 2:
                raise WireError("invalid SVCB port length")
            elif key in (4, 6) and (not value or len(value) % (4 if key == 4 else 16)):
                raise WireError("invalid SVCB address hints")
        if 2 in values and 1 not in values:
            raise WireError("SVCB no-default-alpn requires an alpn list")

    @classmethod
    def from_tokens(cls, tokens: Sequence[str], origin: Name) -> "ServiceBinding":
        if len(tokens) < 2 or not tokens[0].isascii() or not tokens[0].isdecimal():
            raise ValueError("SVCB record requires a priority and target")
        params = []
        for token in tokens[2:]:
            name, _, value = token.partition("=")
            key = _key(name)
            data = parse_string(value)
            params.append((key, _param_data(key, data) if name in _KEYS else data))
        priority = int(tokens[0])
        if priority == 0 and params:
            raise ValueError("SVCB AliasMode records cannot specify parameters")
        return cls(priority, parse_name(tokens[1], origin), tuple(sorted(params)))

    @classmethod
    def from_record(cls, rr: ResourceRecord) -> "ServiceBinding":
        if len(rr.data) < 3:
            raise WireError("truncated SVCB record")
        priority = _H.unpack_from(rr.data)[0]
        target, offset = _read_name(rr.data, 2, canonical=False, compress=False)
        params = []
        while offset < len(rr.data):
            if offset + 4 > len(rr.data):
                raise WireError("truncated SVCB parameter header")
            key, size = _HEADER.unpack_from(rr.data, offset)
            offset += 4
            end = offset + size
            if end > len(rr.data):
                raise WireError("truncated SVCB parameter")
            params.append((key, rr.data[offset:end]))
            offset = end
        return cls(priority, target, tuple(params))

    def to_wire(self) -> bytes:
        return (
            _H.pack(self.priority)
            + _name_wire(self.target)
            + b"".join(
                _HEADER.pack(key, len(value)) + value for key, value in self.params
            )
        )

    def to_text(self) -> str:
        params = (
            _name(key) if not value else f"{_name(key)}={_param_text(key, value)}"
            for key, value in self.params
        )
        return " ".join((str(self.priority), name_text(self.target), *params))
