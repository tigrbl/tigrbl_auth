"""Typed service binding parameters for SVCB and HTTPS."""

from dataclasses import dataclass
from enum import IntEnum
from ipaddress import IPv4Address, IPv6Address
from struct import Struct

from ..svcb import _alpn_parts, _key, _param_text

_H = Struct("!H")


class ParamKey(IntEnum):
    MANDATORY = 0
    ALPN = 1
    NO_DEFAULT_ALPN = 2
    PORT = 3
    IPV4HINT = 4
    ECH = 5
    IPV6HINT = 6
    DOHPATH = 7
    OHTTP = 8
    DOCPATH = 10

    @classmethod
    def make(cls, key):
        if isinstance(key, str):
            key = _key(key.lower())
        if not isinstance(key, int) or not 0 <= key < 65535:
            raise ValueError("invalid SVCB parameter key")
        return cls._value2member_map_.get(key, key)


class Param:
    def _wire(self):
        raise NotImplementedError

    def to_wire(self, file=None, origin=None):
        value = self._wire()
        if file is None:
            return value
        file.write(value)

    def to_text(self):
        return _param_text(self._key, self._wire())


@dataclass(frozen=True)
class GenericParam(Param):
    value: bytes
    _key = -1

    def _wire(self):
        return bytes(self.value)


@dataclass(frozen=True)
class MandatoryParam(Param):
    keys: tuple
    _key = ParamKey.MANDATORY

    def __post_init__(self):
        object.__setattr__(
            self, "keys", tuple(sorted(ParamKey.make(k) for k in self.keys))
        )

    def _wire(self):
        return b"".join(_H.pack(k) for k in self.keys)


@dataclass(frozen=True)
class ALPNParam(Param):
    ids: tuple[bytes, ...]
    _key = ParamKey.ALPN

    def __post_init__(self):
        values = tuple(
            part.encode() if isinstance(part, str) else bytes(part) for part in self.ids
        )
        if not values or any(not 1 <= len(part) <= 255 for part in values):
            raise ValueError("invalid SVCB ALPN identifiers")
        object.__setattr__(self, "ids", values)

    def _wire(self):
        return b"".join(bytes((len(part),)) + part for part in self.ids)


@dataclass(frozen=True)
class PortParam(Param):
    port: int
    _key = ParamKey.PORT

    def _wire(self):
        return self.port.to_bytes(2, "big")


@dataclass(frozen=True)
class _HintParam(Param):
    addresses: tuple[str, ...]

    def __post_init__(self):
        addresses = tuple(
            str(self._address_type(address)) for address in self.addresses
        )
        if not addresses or any("%" in address for address in addresses):
            raise ValueError("SVCB hints require unscoped addresses")
        object.__setattr__(self, "addresses", addresses)

    def _wire(self):
        return b"".join(
            self._address_type(address).packed for address in self.addresses
        )


class IPv4HintParam(_HintParam):
    _key = ParamKey.IPV4HINT
    _address_type = IPv4Address


class IPv6HintParam(_HintParam):
    _key = ParamKey.IPV6HINT
    _address_type = IPv6Address


@dataclass(frozen=True)
class ECHParam(Param):
    ech: bytes
    _key = ParamKey.ECH

    def _wire(self):
        return bytes(self.ech)


def decode_param(key, data):
    if key == ParamKey.MANDATORY:
        return MandatoryParam(tuple(k for (k,) in _H.iter_unpack(data)))
    if key == ParamKey.ALPN:
        return ALPNParam(_alpn_parts(data))
    if key == ParamKey.PORT:
        return PortParam(_H.unpack(data)[0])
    if key in (ParamKey.IPV4HINT, ParamKey.IPV6HINT):
        kind, width = (
            (IPv4HintParam, 4) if key == ParamKey.IPV4HINT else (IPv6HintParam, 16)
        )
        return kind(
            tuple(
                data[offset : offset + width] for offset in range(0, len(data), width)
            )
        )
    if key == ParamKey.ECH:
        return ECHParam(data)
    if key in (ParamKey.NO_DEFAULT_ALPN, ParamKey.OHTTP):
        return None
    return GenericParam(data)
