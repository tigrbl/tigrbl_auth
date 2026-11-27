"""Typed EDNS options with lossless handling of unrecognized options."""

import ipaddress
from dataclasses import dataclass
from struct import Struct

from .wire import EdnsOption, WireError

_ECS = Struct("!HBB")
_H = Struct("!H")
_I = Struct("!I")


@dataclass(frozen=True)
class ClientSubnet:
    network: ipaddress.IPv4Network | ipaddress.IPv6Network
    scope: int = 0

    @classmethod
    def from_text(cls, network: str, *, scope: int = 0) -> "ClientSubnet":
        return cls(ipaddress.ip_network(network, strict=False), scope)

    def to_option(self) -> EdnsOption:
        if not 0 <= self.scope <= self.network.max_prefixlen:
            raise ValueError("EDNS subnet scope out of range")
        length = (self.network.prefixlen + 7) // 8
        return EdnsOption(
            8,
            _ECS.pack(
                1 if self.network.version == 4 else 2,
                self.network.prefixlen,
                self.scope,
            )
            + self.network.network_address.packed[:length],
        )

    @classmethod
    def from_option(cls, option: EdnsOption) -> "ClientSubnet":
        if option.code != 8 or len(option.data) < _ECS.size:
            raise WireError("invalid EDNS client subnet option")
        family, prefix, scope = _ECS.unpack_from(option.data)
        width = {1: 32, 2: 128}.get(family)
        address = option.data[_ECS.size :]
        if (
            width is None
            or prefix > width
            or scope > width
            or len(address) != (prefix + 7) // 8
        ):
            raise WireError(
                "invalid EDNS client subnet family, prefix, or address length"
            )
        ip = ipaddress.ip_address(address.ljust(width // 8, b"\0"))
        try:
            return cls(ipaddress.ip_network((ip, prefix)), scope)
        except ValueError as exc:
            raise WireError("EDNS client subnet has nonzero host bits") from exc


@dataclass(frozen=True)
class Cookie:
    client: bytes
    server: bytes = b""

    def __post_init__(self) -> None:
        if len(self.client) != 8 or self.server and not 8 <= len(self.server) <= 32:
            raise WireError("invalid EDNS cookie length")

    def to_option(self) -> EdnsOption:
        return EdnsOption(10, self.client + self.server)

    @classmethod
    def from_option(cls, option: EdnsOption) -> "Cookie":
        if option.code != 10:
            raise WireError("expected an EDNS cookie")
        return cls(option.data[:8], option.data[8:])


@dataclass(frozen=True)
class ExtendedError:
    info_code: int
    text: str = ""

    def to_option(self) -> EdnsOption:
        return EdnsOption(15, _H.pack(self.info_code) + self.text.encode("utf-8"))

    @classmethod
    def from_option(cls, option: EdnsOption) -> "ExtendedError":
        if option.code != 15 or len(option.data) < 2:
            raise WireError("invalid EDNS extended error option")
        try:
            return cls(_H.unpack_from(option.data)[0], option.data[2:].decode("utf-8"))
        except UnicodeError as exc:
            raise WireError("invalid EDNS extended error text") from exc


@dataclass(frozen=True)
class Expire:
    seconds: int | None = None

    def to_option(self) -> EdnsOption:
        return EdnsOption(9, b"" if self.seconds is None else _I.pack(self.seconds))

    @classmethod
    def from_option(cls, option: EdnsOption) -> "Expire":
        if option.code != 9 or len(option.data) not in (0, 4):
            raise WireError("invalid EDNS expire option")
        return cls(_I.unpack(option.data)[0] if option.data else None)


@dataclass(frozen=True)
class Keepalive:
    units: int | None = None

    def to_option(self) -> EdnsOption:
        return EdnsOption(11, b"" if self.units is None else _H.pack(self.units))

    @classmethod
    def from_option(cls, option: EdnsOption) -> "Keepalive":
        if option.code != 11 or len(option.data) not in (0, 2):
            raise WireError("invalid EDNS keepalive option")
        return cls(_H.unpack(option.data)[0] if option.data else None)


def padding(size: int) -> EdnsOption:
    if not 0 <= size <= 65531:
        raise ValueError("EDNS padding size out of range")
    return EdnsOption(12, b"\0" * size)


def decoded_option(
    option: EdnsOption,
) -> ClientSubnet | Cookie | ExtendedError | Expire | Keepalive | EdnsOption:
    codec = {
        8: ClientSubnet,
        9: Expire,
        10: Cookie,
        11: Keepalive,
        15: ExtendedError,
    }.get(option.code)
    return option if codec is None else codec.from_option(option)
