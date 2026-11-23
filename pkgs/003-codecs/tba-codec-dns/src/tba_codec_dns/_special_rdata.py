"""Typed DNS RDATA for records whose formats need dedicated codecs."""

import base64
from dataclasses import FrozenInstanceError, dataclass
from ipaddress import IPv4Address

from tba_primitives_dns_name.name import Name
from tba_primitives_dns_name.names import name_text, parse_name

from . import rdata
from .rdata import Rdata
from .record_formats import parse_special, special_fields
from .tkey import Tkey
from .tsig import TsigRecord
from .wire import Edns, RecordType, WireError, _name_wire


def _name(value, origin=None):
    name = Name((*value, b""))
    return name if origin is None else name.relativize(origin)


def _target(kind, value, origin=None):
    if kind == 0:
        return None
    if kind == 3:
        return _name(parse_name(value), origin)
    return value


class _Special(Rdata):
    _names = ()

    def __setattr__(self, name, value):
        raise FrozenInstanceError(f"cannot modify {type(self).__name__} RDATA")

    def __delattr__(self, name):
        raise FrozenInstanceError(f"cannot modify {type(self).__name__} RDATA")

    def __getattr__(self, field):
        if field in self._names:
            return self.fields[self._names.index(field)]
        raise AttributeError(field)

    def replace(self, **changes):
        if changes.keys() - set(self._names):
            raise ValueError("unknown DNS RDATA field")
        values = dict(zip(self._names, self.fields))
        values.update(changes)
        return type(self)(self.rdclass, self.rdtype, **values)


class _ChaosCodec:
    def from_tokens(self, tokens, origin):
        if len(tokens) != 2:
            raise ValueError("CHAOS A requires a domain and an octal address")
        return self.to_wire((parse_name(tokens[0], origin), int(tokens[1], 8)))

    def decode(self, record):
        domain, offset = record.read_name(0, canonical=False)
        if len(record.data) - offset != 2:
            raise WireError("invalid CHAOS A address length")
        return domain, int.from_bytes(record.data[offset:], "big")

    def to_text(self, fields):
        domain, address = fields
        return f"{name_text(domain)} {address:o}"

    def to_wire(self, fields, *, canonical=False):
        domain, address = fields
        if canonical:
            domain = tuple(label.lower() for label in domain)
        return _name_wire(domain) + address.to_bytes(2, "big")


CHAOS_CODEC = _ChaosCodec()


class ChaosA(_Special):
    _names = ("domain", "address")

    def __init__(self, rdclass, rdtype, domain, address):
        super().__init__(
            rdclass, rdtype, CHAOS_CODEC.to_wire((rdata._origin(domain), address))
        )

    @property
    def fields(self):
        domain, address = CHAOS_CODEC.decode(self.record(()))
        return _name(domain, self._display_origin), address


class WKS(_Special):
    _names = ("address", "protocol", "bitmap")

    def __init__(self, rdclass, rdtype, address, protocol, bitmap):
        super().__init__(
            rdclass,
            rdtype,
            IPv4Address(address).packed + bytes((protocol,)) + bytes(bitmap),
        )

    @property
    def fields(self):
        address, protocol, *_ = special_fields(self.record(()))
        return address, int(protocol), self.data[5:]


class TKEY(_Special):
    _names = ("algorithm", "inception", "expiration", "mode", "error", "key", "other")

    def __init__(
        self,
        rdclass,
        rdtype,
        algorithm,
        inception,
        expiration,
        mode,
        error,
        key,
        other=b"",
    ):
        super().__init__(
            rdclass,
            rdtype,
            Tkey(
                rdata._origin(algorithm), inception, expiration, mode, error, key, other
            ).to_wire(),
        )

    @property
    def fields(self):
        item = Tkey.from_wire(self.data)
        return (
            _name(item.algorithm, self._display_origin),
            item.inception,
            item.expiration,
            item.mode,
            item.error,
            item.key,
            item.other,
        )


class TSIG(_Special):
    _names = (
        "algorithm",
        "time_signed",
        "fudge",
        "mac",
        "original_id",
        "error",
        "other",
    )

    def __init__(
        self,
        rdclass,
        rdtype,
        algorithm,
        time_signed,
        fudge,
        mac,
        original_id,
        error,
        other=b"",
    ):
        super().__init__(
            rdclass,
            rdtype,
            TsigRecord(
                rdata._origin(algorithm),
                time_signed,
                fudge,
                mac,
                original_id,
                error,
                other,
            ).data(),
        )

    @property
    def fields(self):
        item = TsigRecord.from_data(self.data)
        return (
            _name(item.algorithm, self._display_origin),
            item.time_signed,
            item.fudge,
            item.mac,
            item.original_id,
            item.error,
            item.other,
        )


class OPT(_Special):
    _names = ("options",)

    def __init__(self, rdclass, rdtype, options=()):
        super().__init__(
            rdclass, rdtype, b"".join(option.to_wire() for option in options)
        )

    @property
    def fields(self):
        return (Edns.from_record(self.record(())).options,)

    @property
    def payload(self):
        return self.rdclass


class HIP(_Special):
    _names = ("hit", "algorithm", "key", "servers")

    def __init__(self, rdclass, rdtype, hit, algorithm, key, servers=()):
        tokens = (
            str(algorithm),
            bytes(hit).hex(),
            base64.b64encode(key).decode("ascii"),
            *(name_text(rdata._origin(name)) for name in servers),
        )
        super().__init__(rdclass, rdtype, parse_special(RecordType.HIP, tokens, ()))

    @property
    def fields(self):
        algorithm, hit, key, *servers = special_fields(self.record(()))
        return (
            bytes.fromhex(hit),
            int(algorithm),
            base64.b64decode(key),
            tuple(_name(parse_name(name), self._display_origin) for name in servers),
        )


class AMTRELAY(_Special):
    _names = ("precedence", "discovery_optional", "relay_type", "relay")

    def __init__(
        self, rdclass, rdtype, precedence, discovery_optional, relay_type, relay=None
    ):
        target = "." if relay is None else str(relay)
        args = tuple(
            map(str, (precedence, int(discovery_optional), relay_type, target))
        )
        super().__init__(rdclass, rdtype, parse_special(RecordType.AMTRELAY, args, ()))

    @property
    def fields(self):
        precedence, optional, kind, target = special_fields(self.record(()))
        return (
            int(precedence),
            bool(int(optional)),
            int(kind),
            _target(int(kind), target, self._display_origin),
        )


class IPSECKEY(_Special):
    _names = ("precedence", "gateway_type", "algorithm", "gateway", "key")

    def __init__(
        self, rdclass, rdtype, precedence, gateway_type, algorithm, gateway, key
    ):
        target = "." if gateway is None else str(gateway)
        args = (
            *map(str, (precedence, gateway_type, algorithm, target)),
            base64.b64encode(key).decode("ascii") or ".",
        )
        super().__init__(rdclass, rdtype, parse_special(RecordType.IPSECKEY, args, ()))

    @property
    def fields(self):
        precedence, kind, algorithm, target, key = special_fields(self.record(()))
        return (
            int(precedence),
            int(kind),
            int(algorithm),
            _target(int(kind), target, self._display_origin),
            base64.b64decode(key) if key != "." else b"",
        )


@dataclass(frozen=True)
class APLItem:
    family: int
    negation: bool
    address: str
    prefix: int

    def __str__(self):
        return (
            f"{'!' if self.negation else ''}{self.family}:{self.address}/{self.prefix}"
        )


class APL(_Special):
    _names = ("items",)

    def __init__(self, rdclass, rdtype, items):
        super().__init__(
            rdclass, rdtype, parse_special(RecordType.APL, tuple(map(str, items)), ())
        )

    @property
    def fields(self):
        items = []
        for text in special_fields(self.record(())):
            negation = text.startswith("!")
            family, address = text.lstrip("!").split(":", 1)
            host, prefix = address.rsplit("/", 1)
            items.append(APLItem(int(family), negation, host, int(prefix)))
        return (tuple(items),)


class LOC(_Special):
    _names = (
        "latitude",
        "longitude",
        "altitude",
        "size",
        "horizontal_precision",
        "vertical_precision",
    )

    def __init__(
        self,
        rdclass,
        rdtype,
        latitude,
        longitude,
        altitude,
        size=100,
        horizontal_precision=1000000,
        vertical_precision=1000,
        *,
        hprec=None,
        vprec=None,
    ):
        horizontal_precision = horizontal_precision if hprec is None else hprec
        vertical_precision = vertical_precision if vprec is None else vprec

        def angle(value, positive, negative):
            if isinstance(value, (int, float)):
                return f"{abs(value):.10f} {negative if value < 0 else positive}"
            degrees, minutes, seconds, milliseconds, sign = value
            return f"{degrees} {minutes} {seconds}.{milliseconds:03} {negative if sign < 0 else positive}"

        text = f"{angle(latitude, 'N', 'S')} {angle(longitude, 'E', 'W')} {altitude / 100} {size / 100} {horizontal_precision / 100} {vertical_precision / 100}"
        super().__init__(
            rdclass, rdtype, parse_special(RecordType.LOC, text.split(), ())
        )

    @property
    def fields(self):
        tokens = special_fields(self.record(()))

        def angle(parts):
            deg, mins, seconds, hemisphere = parts
            whole, _, fraction = seconds.partition(".")
            return (
                int(deg),
                int(mins),
                int(whole),
                int(fraction.ljust(3, "0")),
                -1 if hemisphere in "SW" else 1,
            )

        return (
            angle(tokens[:4]),
            angle(tokens[4:8]),
            *(round(float(t.removesuffix("m")) * 100) for t in tokens[8:]),
        )

    @staticmethod
    def _decimal_angle(value):
        deg, mins, secs, msecs, sign = value
        return sign * (deg + mins / 60 + (secs + msecs / 1000) / 3600)

    @property
    def float_latitude(self):
        return self._decimal_angle(self.latitude)

    @property
    def float_longitude(self):
        return self._decimal_angle(self.longitude)


SPECIAL_CLASSES = {
    RecordType[cls.__name__]: cls
    for cls in (WKS, TKEY, TSIG, OPT, HIP, AMTRELAY, IPSECKEY, APL, LOC)
}
