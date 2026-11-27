"""In-house DNS record codecs, including RFC 3597 opaque records."""

import base64
import ipaddress
import re
from collections.abc import Sequence
from dataclasses import FrozenInstanceError, dataclass, field
from datetime import datetime, timezone
from functools import total_ordering
from struct import Struct
from threading import Lock
from types import MappingProxyType
from typing import BinaryIO, Protocol

from tba_primitives_dns_name.name import Name as DomainName
from tba_primitives_dns_name.name import NameStyle
from tba_primitives_dns_name.names import (
    ROOT,
    Name,
    encode_idna2003,
    name_text,
    parse_name,
    parse_string,
    string_text,
)

from .record_formats import KINDS, parse_special, special_fields
from .svcb import ServiceBinding
from .tokenizer import Tokenizer, master_tokens
from .wire import (
    _EXTRA_TYPE_BY_NAME,
    _EXTRA_TYPE_BY_NUMBER,
    Parser,
    RecordClass,
    RecordType,
    ResourceRecord,
    WireError,
    _name_wire,
    _read_name,
    class_text,
    record_class,
    record_type,
    type_text,
)

_SCHEMAS = {
    "A": "4",
    "AAAA": "6",
    "NS": "n",
    "MD": "n",
    "MF": "n",
    "CNAME": "n",
    "SOA": "n n I t t t t",
    "MB": "n",
    "MG": "n",
    "MR": "n",
    "PTR": "n",
    "HINFO": "s s",
    "MINFO": "n n",
    "MX": "H n",
    "TXT": "S",
    "SPF": "S",
    "NINFO": "S",
    "WALLET": "S",
    "RP": "n n",
    "AFSDB": "H n",
    "X25": "s",
    "ISDN": "S",
    "RT": "H n",
    "NSAP": "a",
    "NSAP_PTR": "n",
    "SIG": "r B B t d d H n b",
    "KEY": "H B B b",
    "PX": "H n n",
    "GPOS": "s s s",
    "SRV": "H H H n",
    "NAPTR": "H H s s s n",
    "KX": "H n",
    "CERT": "H H B b",
    "DNAME": "n",
    "DS": "H B B x",
    "SSHFP": "B B x",
    "RRSIG": "r B B t d d H n b",
    "NSEC": "n m",
    "DNSKEY": "H B B b",
    "DHCID": "b",
    "NSEC3": "B B H X Y m",
    "NSEC3PARAM": "B B H X",
    "TLSA": "B B B x",
    "SMIMEA": "B B B x",
    "TALINK": "n n",
    "CDS": "H B B x",
    "CDNSKEY": "H B B b",
    "OPENPGPKEY": "b",
    "CSYNC": "I H m",
    "ZONEMD": "I B B x",
    "DSYNC": "r g H n",
    "NID": "H j",
    "L32": "H 4",
    "L64": "H j",
    "LP": "H n",
    "EUI48": "e",
    "EUI64": "E",
    "URI": "H H u",
    "CAA": "B s u",
    "AVC": "S",
    "RESINFO": "S",
    "TA": "H B B x",
    "DLV": "H B B x",
}
_FORMATS = {
    int(RecordType[key]): tuple(value.split()) for key, value in _SCHEMAS.items()
}
_NUMBERS = {
    symbol: Struct("!" + fmt)
    for symbol, fmt in {
        "B": "B",
        "H": "H",
        "I": "I",
        "t": "I",
        "d": "I",
        "r": "H",
        "g": "B",
    }.items()
}
_TTL_TOKEN = re.compile(r"([0-9]+)([wdhms]?)", re.IGNORECASE)
_TTL_UNITS = {"w": 604800, "d": 86400, "h": 3600, "m": 60, "s": 1, "": 1}


class RecordCodec(Protocol):
    """Presentation and wire conversion for an application-defined RDATA type."""

    def from_tokens(self, tokens: Sequence[str], origin: Name) -> bytes: ...

    def decode(self, record: ResourceRecord) -> tuple: ...

    def to_text(self, fields: tuple) -> str: ...

    def to_wire(self, fields: tuple, *, canonical: bool) -> bytes: ...


_CUSTOM: dict[tuple[int, int], RecordCodec] = {}
_REGISTRATION_LOCK = Lock()


_CUSTOM_CLASSES: dict[tuple[int, int], type] = {}
_SINGLETON_TYPES: set[int] = set()


def register_type(
    implementation=None,
    rdtype=None,
    rdtype_text=None,
    is_singleton=False,
    rdclass=RecordClass.IN,
    *,
    codec=None,
) -> None:
    """Register an Rdata implementation or a native TBA record codec."""
    typed = isinstance(implementation, type) and issubclass(implementation, Rdata)
    if codec is not None:
        if implementation is not None or rdtype_text is not None:
            raise TypeError("specify one DNS RDATA implementation")
    elif not typed:
        rdclass, codec = implementation, rdtype_text
    number, kind = record_class(rdclass), record_type(rdtype)
    if (
        not number
        or number == RecordClass.NONE
        or not kind
        or kind in _FORMATS
        or kind in KINDS
        or kind in (RecordType.OPT, RecordType.SVCB, RecordType.HTTPS, RecordType.TSIG)
        or 249 <= kind <= 255
    ):
        raise ValueError("DNS RDATA type is built-in or reserved")
    key = number, kind
    with _REGISTRATION_LOCK:
        if key in _CUSTOM or key in _CUSTOM_CLASSES:
            raise ValueError("DNS RDATA implementation is already registered")
        if not typed:
            if codec is None:
                raise TypeError("DNS RDATA codec is required")
            _CUSTOM[key] = codec
            return
        if not isinstance(rdtype_text, str) or not re.fullmatch(
            r"[A-Za-z][A-Za-z0-9-]*", rdtype_text
        ):
            raise ValueError("invalid DNS record mnemonic")
        if (
            implementation.from_text.__func__ is Rdata.from_text.__func__
            or implementation.from_wire_parser.__func__
            is Rdata.from_wire_parser.__func__
        ):
            raise TypeError(
                "registered RDATA classes must supply text and wire parsers"
            )
        mnemonic = rdtype_text.upper()
        try:
            previous = record_type(mnemonic)
        except ValueError:
            previous = kind
        if previous != kind or _EXTRA_TYPE_BY_NUMBER.get(kind, mnemonic) != mnemonic:
            raise ValueError("DNS record mnemonic is already registered")
        _CUSTOM_CLASSES[key] = implementation
        _EXTRA_TYPE_BY_NAME[mnemonic] = kind
        _EXTRA_TYPE_BY_NUMBER[kind] = mnemonic
        if is_singleton:
            _SINGLETON_TYPES.add(kind)


def is_registered_singleton(rdtype):
    return record_type(rdtype) in _SINGLETON_TYPES


def _custom_class(rdclass, rdtype):
    return _CUSTOM_CLASSES.get((rdclass, rdtype)) or _CUSTOM_CLASSES.get(
        (RecordClass.ANY, rdtype)
    )


def _codec(rdclass: int, rdtype: int) -> RecordCodec | None:
    if rdclass == RecordClass.CH and rdtype == RecordType.A:
        from ._special_rdata import CHAOS_CODEC

        return CHAOS_CODEC
    return _CUSTOM.get((rdclass, rdtype)) or _CUSTOM.get((RecordClass.ANY, rdtype))


def parse_ttl(text: str) -> int:
    ttl = offset = 0
    for part in _TTL_TOKEN.finditer(text):
        if part.start() != offset or (not part[2] and part[1] != text):
            raise ValueError(f"invalid DNS TTL {text!r}")
        ttl += int(part[1]) * _TTL_UNITS[part[2].lower()]
        offset = part.end()
    if offset == 0 or offset != len(text) or ttl > 0xFFFFFFFF:
        raise ValueError(f"invalid DNS TTL {text!r}")
    return ttl


def _time_value(text: str) -> int:
    if not text.isascii() or not text.isdecimal():
        raise ValueError("invalid DNS signature time")
    if len(text) == 14:
        timestamp = datetime.strptime(text, "%Y%m%d%H%M%S").replace(tzinfo=timezone.utc)
        return int(timestamp.timestamp()) & 0xFFFFFFFF
    return int(text)


def type_bitmap(types: Sequence[int]) -> bytes:
    windows: dict[int, bytearray] = {}
    for value in sorted(set(types)):
        window, offset = divmod(record_type(value), 256)
        octet, bit = divmod(offset, 8)
        bitmap = windows.setdefault(window, bytearray())
        if octet >= len(bitmap):
            bitmap.extend(b"\x00" * (octet + 1 - len(bitmap)))
        bitmap[octet] |= 0x80 >> bit
    return b"".join(
        bytes((window, len(bitmap))) + bitmap for window, bitmap in windows.items()
    )


def bitmap_types(data: bytes) -> tuple[int, ...]:
    types = []
    offset, previous = 0, -1
    while offset < len(data):
        if offset + 2 > len(data):
            raise WireError("truncated DNS type bitmap")
        window, size = data[offset : offset + 2]
        start, end = offset + 2, offset + 2 + size
        if (
            not 1 <= size <= 32
            or end > len(data)
            or window <= previous
            or not data[end - 1]
        ):
            raise WireError("invalid DNS type bitmap window")
        for octet, value in enumerate(data[start:end]):
            types.extend(
                window * 256 + octet * 8 + bit
                for bit in range(8)
                if value & (128 >> bit)
            )
        offset, previous = end, window
    return tuple(types)


def _counted(data: bytes) -> bytes:
    if len(data) > 255:
        raise ValueError("DNS character string exceeds 255 octets")
    return bytes((len(data),)) + data


def _parse_field(symbol: str, token: str, origin: Name, encode_label) -> bytes:
    if symbol in _NUMBERS:
        if symbol == "r":
            value = record_type(token)
        elif symbol == "t":
            value = parse_ttl(token)
        elif symbol == "d":
            value = _time_value(token)
        elif symbol == "g" and token.upper() == "NOTIFY":
            value = 1
        else:
            if not token.isascii() or not token.isdecimal():
                raise ValueError("DNS numeric field requires an unsigned integer")
            value = int(token)
        if not 0 <= value < 256 ** _NUMBERS[symbol].size:
            raise ValueError("DNS integer field out of range")
        return _NUMBERS[symbol].pack(value)
    if symbol == "n":
        return _name_wire(parse_name(token, origin, encode_label=encode_label))
    if symbol == "s":
        return _counted(parse_string(token))
    if symbol == "u":
        return parse_string(token)
    if symbol == "4":
        return ipaddress.IPv4Address(token).packed
    if symbol == "6":
        address = ipaddress.IPv6Address(token)
        if address.scope_id is not None:
            raise ValueError("AAAA data cannot contain a scope identifier")
        return address.packed
    if symbol == "b":
        return base64.b64decode(token, validate=True)
    if symbol == "x":
        return bytes.fromhex(token)
    if symbol == "X":
        return _counted(b"" if token == "-" else bytes.fromhex(token))
    if symbol == "Y":
        encoded = token.upper()
        value = base64.b32hexdecode(encoded + "=" * (-len(encoded) % 8))
        if base64.b32hexencode(value).decode().rstrip("=") != encoded:
            raise ValueError("noncanonical DNS Base32hex encoding")
        return _counted(value)
    if symbol == "j":
        if not re.fullmatch(r"[0-9A-Fa-f]{4}(?::[0-9A-Fa-f]{4}){3}", token):
            raise ValueError("DNS locator requires four 16-bit hexadecimal groups")
        return bytes.fromhex(token.replace(":", ""))
    if symbol == "a":
        if not token.lower().startswith("0x"):
            raise ValueError("NSAP addresses require hexadecimal 0x notation")
        return bytes.fromhex(token[2:].replace(".", ""))
    data = bytes.fromhex(token.replace("-", ""))
    if len(data) != (6 if symbol == "e" else 8):
        raise ValueError("invalid DNS EUI length")
    return data


_FINGERPRINT_LENGTHS = {
    RecordType.TLSA: {1: 32, 2: 64},
    RecordType.SMIMEA: {1: 32, 2: 64},
    RecordType.SSHFP: {1: 20, 2: 32},
}


def from_tokens(
    owner: Name,
    ttl: int,
    rdclass: int | str,
    rdtype: int | str,
    tokens: Sequence[str],
    *,
    origin: Name = ROOT,
    idna_codec=None,
) -> ResourceRecord:
    """Construct a record from master-file tokens or RFC 3597 hex data."""
    kind = record_type(rdtype)
    rdclass = record_class(rdclass)
    codec = _codec(rdclass, kind)
    encode_label = encode_idna2003 if idna_codec is None else idna_codec.encode
    custom = _custom_class(rdclass, kind)
    if not 0 <= ttl <= 0xFFFFFFFF:
        raise ValueError("DNS TTL out of range")
    if tokens and tokens[0] == r"\#":
        if len(tokens) < 2:
            raise ValueError("missing RFC 3597 record length")
        data = bytes.fromhex("".join(tokens[2:]))
        if len(data) != int(tokens[1]):
            raise ValueError("RFC 3597 record length mismatch")
    elif custom is not None:
        result = custom.from_text(
            rdclass, kind, " ".join(tokens), DomainName((*origin, b""))
        )
        data = result.to_wire()
    elif codec is not None:
        data = codec.from_tokens(tokens, origin)
    elif kind in (RecordType.SVCB, RecordType.HTTPS):
        data = ServiceBinding.from_tokens(
            tokens, origin, encode_label=encode_label
        ).to_wire()
    elif kind in KINDS:
        data = parse_special(kind, tokens, origin, encode_label=encode_label)
    else:
        fields = _FORMATS.get(kind)
        if fields is None:
            raise ValueError(f"{type_text(kind)} requires RFC 3597 hex data")
        offset = 0
        parts = []
        for symbol in fields:
            if symbol == "m":
                parts.append(
                    type_bitmap([record_type(token) for token in tokens[offset:]])
                )
                offset = len(tokens)
            elif symbol == "S":
                if offset == len(tokens):
                    raise ValueError("missing DNS character string")
                parts.extend(_counted(parse_string(token)) for token in tokens[offset:])
                offset = len(tokens)
            else:
                if offset >= len(tokens):
                    raise ValueError(f"incomplete {type_text(kind)} record")
                end = len(tokens) if symbol in ("b", "x") else offset + 1
                parts.append(
                    _parse_field(
                        symbol, "".join(tokens[offset:end]), origin, encode_label
                    )
                )
                offset = end
        if offset != len(tokens):
            raise ValueError(f"extra fields in {type_text(kind)} record")
        data = b"".join(parts)
    if len(data) > 65535:
        raise ValueError("DNS record data exceeds 65535 octets")
    record = ResourceRecord(owner, kind, rdclass, ttl, data)
    if codec is not None:
        codec.decode(record)
    elif kind in _FINGERPRINT_LENGTHS or kind == RecordType.NSEC3:
        decoded(record)
    return record


def _take(data: bytes, offset: int, size: int) -> tuple[bytes, int]:
    end = offset + size
    if end > len(data):
        raise WireError("truncated DNS record field")
    return data[offset:end], end


def decoded(record: ResourceRecord) -> tuple:
    """Decode the RDATA into immutable field values in presentation order."""
    codec = _codec(record.rdclass, record.type)
    if codec is not None:
        return codec.decode(record)
    if record.type in (RecordType.SVCB, RecordType.HTTPS):
        return (ServiceBinding.from_record(record),)
    if record.type in KINDS:
        return special_fields(record)
    fields = _FORMATS.get(record.type)
    if fields is None:
        return (record.data,)
    data, offset = record.data, 0
    values = []
    for symbol in fields:
        if symbol in _NUMBERS:
            number = _NUMBERS[symbol]
            raw, offset = _take(data, offset, number.size)
            values.append(number.unpack(raw)[0])
        elif symbol == "n":
            name, offset = record.read_name(offset, canonical=False)
            values.append(name)
        elif symbol in ("s", "X", "Y"):
            size, offset = _take(data, offset, 1)
            value, offset = _take(data, offset, size[0])
            values.append(value)
        elif symbol in ("4", "6", "e", "E", "j"):
            raw, offset = _take(
                data, offset, {"4": 4, "6": 16, "e": 6, "E": 8, "j": 8}[symbol]
            )
            values.append(ipaddress.ip_address(raw) if symbol in "46" else raw)
        else:
            tail = data[offset:]
            if symbol == "m":
                values.append(bitmap_types(tail))
            elif symbol == "S":
                strings = []
                while offset < len(data):
                    size, offset = _take(data, offset, 1)
                    value, offset = _take(data, offset, size[0])
                    strings.append(value)
                if not strings:
                    raise WireError("empty DNS character string list")
                values.append(tuple(strings))
            else:
                values.append(tail)
            offset = len(data)
    if offset != len(data):
        raise WireError("trailing data in DNS record")
    if record.type in _FINGERPRINT_LENGTHS:
        expected = _FINGERPRINT_LENGTHS[record.type].get(values[-2])
        if expected is not None and len(values[-1]) != expected:
            raise WireError(
                f"{type_text(record.type)} data must contain {expected} octets"
            )
    if record.type == RecordType.NSEC3 and not values[4]:
        raise WireError("NSEC3 next owner hash must be nonempty")
    return tuple(values)


def _format_field(symbol: str, value) -> str:
    if symbol == "n":
        return name_text(value)
    if symbol == "r":
        return type_text(value)
    if symbol == "g" and value == 1:
        return "NOTIFY"
    if symbol == "j":
        return value.hex(":", 2)
    if symbol == "a":
        return "0x" + value.hex()
    if symbol == "d":
        return datetime.fromtimestamp(value, timezone.utc).strftime("%Y%m%d%H%M%S")
    if symbol in "su":
        return string_text(value)
    if symbol == "S":
        return " ".join(map(string_text, value))
    if symbol == "b":
        return base64.b64encode(value).decode()
    if symbol in "xX":
        return value.hex().upper() if symbol == "x" or value else "-"
    if symbol == "Y":
        return base64.b32hexencode(value).decode().rstrip("=")
    if symbol in "eE":
        return value.hex("-")
    if symbol == "m":
        return " ".join(map(type_text, value))
    return str(value)


def rdata_text(record: ResourceRecord) -> str:
    if not record.data and record.rdclass in (RecordClass.NONE, RecordClass.ANY):
        return r"\# 0"
    codec = _codec(record.rdclass, record.type)
    if codec is not None:
        return codec.to_text(codec.decode(record))
    if record.type in (RecordType.SVCB, RecordType.HTTPS):
        return ServiceBinding.from_record(record).to_text()
    if record.type in KINDS:
        return " ".join(special_fields(record))
    fields = _FORMATS.get(record.type)
    if fields is None:
        return f"\\# {len(record.data)} {record.data.hex().upper()}".rstrip()
    return " ".join(
        _format_field(symbol, value) for symbol, value in zip(fields, decoded(record))
    ).rstrip()


def record_text(record: ResourceRecord) -> str:
    return f"{name_text(record.name)} {record.ttl} {class_text(record.rdclass)} {type_text(record.type)} {rdata_text(record)}".rstrip()


def uncompressed_data(record: ResourceRecord, *, canonical: bool = False) -> bytes:
    codec = _codec(record.rdclass, record.type)
    if codec is not None and (
        record.data or record.rdclass not in (RecordClass.NONE, RecordClass.ANY)
    ):
        return codec.to_wire(codec.decode(record), canonical=canonical)
    fields = _FORMATS.get(record.type, ())
    if not record.data or "n" not in fields:
        return record.data
    if not record._packet and not canonical:
        return record.data
    fold = canonical and record.type in {
        RecordType.NS,
        RecordType.MD,
        RecordType.MF,
        RecordType.CNAME,
        RecordType.SOA,
        RecordType.MB,
        RecordType.MG,
        RecordType.MR,
        RecordType.PTR,
        RecordType.MINFO,
        RecordType.MX,
        RecordType.RP,
        RecordType.AFSDB,
        RecordType.RT,
        RecordType.SIG,
        RecordType.PX,
        RecordType.NAPTR,
        RecordType.KX,
        RecordType.SRV,
        RecordType.DNAME,
        RecordType.RRSIG,
    }
    data, offset = record.data, 0
    output = bytearray()
    last_name = len(fields) - tuple(reversed(fields)).index("n")
    for symbol in fields[:last_name]:
        if symbol == "n":
            name, offset = record.read_name(offset, canonical=fold)
            output.extend(_name_wire(name))
        else:
            size = (
                _NUMBERS[symbol].size
                if symbol in _NUMBERS
                else _take(data, offset, 1)[0][0] + 1
            )
            value, offset = _take(data, offset, size)
            output.extend(value)
    return bytes(output) + data[offset:]


_PROPERTY_NAMES = {
    RecordType.A: ("address",),
    RecordType.AAAA: ("address",),
    RecordType.NS: ("target",),
    RecordType.CNAME: ("target",),
    RecordType.DNAME: ("target",),
    RecordType.PTR: ("target",),
    RecordType.MB: ("target",),
    RecordType.MD: ("target",),
    RecordType.MF: ("target",),
    RecordType.MG: ("target",),
    RecordType.MR: ("target",),
    RecordType.NSAP_PTR: ("target",),
    RecordType.HINFO: ("cpu", "os"),
    RecordType.MINFO: ("rmailbx", "emailbx"),
    RecordType.RP: ("mbox", "txt"),
    RecordType.AFSDB: ("subtype", "hostname"),
    RecordType.RT: ("preference", "host"),
    RecordType.KX: ("preference", "exchange"),
    RecordType.PX: ("preference", "map822", "mapx400"),
    RecordType.X25: ("address",),
    RecordType.ISDN: ("strings",),
    RecordType.NSAP: ("address",),
    RecordType.GPOS: ("longitude", "latitude", "altitude"),
    RecordType.TXT: ("strings",),
    RecordType.SPF: ("strings",),
    RecordType.NINFO: ("strings",),
    RecordType.WALLET: ("strings",),
    RecordType.AVC: ("strings",),
    RecordType.RESINFO: ("strings",),
    RecordType.MX: ("preference", "exchange"),
    RecordType.SOA: (
        "mname",
        "rname",
        "serial",
        "refresh",
        "retry",
        "expire",
        "minimum",
    ),
    RecordType.SRV: ("priority", "weight", "port", "target"),
    RecordType.NAPTR: (
        "order",
        "preference",
        "flags",
        "service",
        "regexp",
        "replacement",
    ),
    RecordType.CAA: ("flags", "tag", "value"),
    RecordType.DNSKEY: ("flags", "protocol", "algorithm", "key"),
    RecordType.CDNSKEY: ("flags", "protocol", "algorithm", "key"),
    RecordType.KEY: ("flags", "protocol", "algorithm", "key"),
    RecordType.DS: ("key_tag", "algorithm", "digest_type", "digest"),
    RecordType.CDS: ("key_tag", "algorithm", "digest_type", "digest"),
    RecordType.RRSIG: (
        "type_covered",
        "algorithm",
        "labels",
        "original_ttl",
        "expiration",
        "inception",
        "key_tag",
        "signer",
        "signature",
    ),
    RecordType.TLSA: ("usage", "selector", "mtype", "cert"),
    RecordType.SMIMEA: ("usage", "selector", "mtype", "cert"),
    RecordType.SSHFP: ("algorithm", "fp_type", "fingerprint"),
    RecordType.TALINK: ("previous", "next"),
    RecordType.CERT: ("certificate_type", "key_tag", "algorithm", "certificate"),
    RecordType.OPENPGPKEY: ("key",),
    RecordType.DHCID: ("data_value",),
    RecordType.NSEC: ("next", "types"),
    RecordType.NSEC3: ("algorithm", "flags", "iterations", "salt", "next", "types"),
    RecordType.NSEC3PARAM: ("algorithm", "flags", "iterations", "salt"),
    RecordType.CSYNC: ("serial", "flags", "types"),
    RecordType.ZONEMD: ("serial", "scheme", "hash_algorithm", "digest"),
    RecordType.NID: ("preference", "nodeid"),
    RecordType.L32: ("preference", "locator"),
    RecordType.L64: ("preference", "locator"),
    RecordType.LP: ("preference", "fqdn"),
    RecordType.DSYNC: ("rrtype", "scheme", "port", "target"),
    RecordType.EUI48: ("eui",),
    RecordType.EUI64: ("eui",),
    RecordType.URI: ("priority", "weight", "target"),
}
for _alias, _base in (
    (RecordType.SIG, RecordType.RRSIG),
    (RecordType.TA, RecordType.DS),
    (RecordType.DLV, RecordType.DS),
):
    _PROPERTY_NAMES[_alias] = _PROPERTY_NAMES[_base]


@dataclass(frozen=True)
class RdataStyle(NameStyle):
    txt_is_utf8: bool = False
    base64_chunk_size: int = 32
    base64_chunk_separator: str = " "
    hex_chunk_size: int = 128
    hex_chunk_separator: str = " "
    truncate_crypto: bool = False


_FIELD_ALIASES = {
    RecordType.AFSDB: {"exchange": "hostname", "preference": "subtype"},
    RecordType.DHCID: {"data": "data_value"},
    RecordType.L32: {"locator32": "locator"},
    RecordType.L64: {"locator64": "locator"},
    RecordType.RT: {"exchange": "host"},
}


def _window_types(windows):
    windows = tuple(windows)
    if not windows or isinstance(windows[0], int):
        return windows
    return bitmap_types(
        b"".join(bytes((number, len(bitmap))) + bitmap for number, bitmap in windows)
    )


def _bitmap_windows(types):
    data = type_bitmap(types)
    offset = 0
    output = []
    while offset < len(data):
        size = data[offset + 1]
        output.append((data[offset], data[offset + 2 : offset + 2 + size]))
        offset += 2 + size
    return tuple(output)


def _styled_string(value, utf8):
    if not utf8:
        return string_text(value)
    try:
        text = value.decode("utf-8")
    except UnicodeDecodeError:
        return string_text(value)
    if any(not char.isprintable() for char in text):
        return string_text(value)
    return '"' + text.replace(chr(92), chr(92) * 2).replace('"', chr(92) + '"') + '"'


def _styled_field(symbol, value, style):
    if symbol == "n":
        return DomainName((*value, b"")).to_styled_text(style)
    if symbol == "S":
        return " ".join(_styled_string(part, style.txt_is_utf8) for part in value)
    if symbol in "su":
        return _styled_string(value, style.txt_is_utf8)
    if symbol in ("b", "x", "X", "Y"):
        text = _format_field(symbol, value)
        if style.truncate_crypto and len(text) > 16:
            return f"{text[:8]}...{text[-8:]}"
        if symbol == "b":
            size, separator = style.base64_chunk_size, style.base64_chunk_separator
        else:
            size, separator = style.hex_chunk_size, style.hex_chunk_separator
        if size > 0:
            return separator.join(text[i : i + size] for i in range(0, len(text), size))
    return _format_field(symbol, value)


@total_ordering
@dataclass(frozen=True, eq=False)
class Rdata:
    """Immutable detached RDATA, with wire and presentation conversions."""

    rdclass: int
    rdtype: int
    data: bytes
    _display_origin: DomainName | None = field(default=None, repr=False, compare=False)

    def __post_init__(self):
        object.__setattr__(self, "rdclass", record_class(self.rdclass))
        object.__setattr__(self, "rdtype", record_type(self.rdtype))
        object.__setattr__(self, "data", bytes(self.data))
        if len(self.data) > 65535:
            raise ValueError("DNS record data exceeds 65535 octets")

    def record(self, owner: Name, ttl: int = 0) -> ResourceRecord:
        if not 0 <= ttl <= 0xFFFFFFFF:
            raise ValueError("DNS TTL is outside its wire range")
        return ResourceRecord(owner, self.rdtype, self.rdclass, ttl, self.data)

    @property
    def fields(self) -> tuple:
        return decoded(self.record(()))

    def __getattr__(self, field: str):
        kind = object.__getattribute__(self, "rdtype")
        names = _PROPERTY_NAMES.get(kind, ())
        if field == "windows" and names and names[-1] == "types":
            return _bitmap_windows(self.fields[-1])
        if kind == RecordType.ISDN and field in ("address", "subaddress"):
            strings = self.fields[0]
            return (
                strings[0]
                if field == "address"
                else (strings[1] if len(strings) > 1 else None)
            )
        field = _FIELD_ALIASES.get(kind, {}).get(field, field)
        if field not in names:
            raise AttributeError(field)
        position = names.index(field)
        value = self.fields[position]
        symbol = _FORMATS[kind][position]
        if symbol == "n":
            name = DomainName((*value, b""))
            return (
                name
                if self._display_origin is None
                else name.relativize(self._display_origin)
            )
        return str(value) if symbol in ("4", "6") else value

    def covers(self) -> int:
        return (
            self.fields[0] if self.rdtype in (RecordType.SIG, RecordType.RRSIG) else 0
        )

    def to_text(
        self,
        origin: DomainName | None = None,
        relativize: bool = True,
        style: RdataStyle | None = None,
    ) -> str:
        if style is not None:
            return self.to_styled_text(style)
        if origin is None:
            origin = self._display_origin
        schema = _FORMATS.get(self.rdtype)
        if schema is None or origin is None or not relativize or "n" not in schema:
            return rdata_text(self.record(()))
        fields = []
        for symbol, value in zip(schema, self.fields):
            fields.append(
                DomainName((*value, b"")).relativize(origin).to_text()
                if symbol == "n"
                else _format_field(symbol, value)
            )
        return " ".join(fields).rstrip()

    def to_styled_text(self, style: RdataStyle) -> str:
        schema = _FORMATS.get(self.rdtype)
        record = self.record(())
        if schema is None or _codec(self.rdclass, self.rdtype) is not None:
            return rdata_text(record)
        return " ".join(
            _styled_field(symbol, value, style)
            for symbol, value in zip(schema, decoded(record))
        ).rstrip()

    def to_wire(
        self,
        file: BinaryIO | None = None,
        compress: dict[DomainName, int] | None = None,
        origin: DomainName | None = None,
        canonicalize: bool = False,
    ) -> bytes | None:
        data = self.record(()).uncompressed_data(canonical=canonicalize)
        if file is None:
            return data
        if compress is not None and not canonicalize and self.rdtype in _COMPRESSIBLE:
            fields = _FORMATS[self.rdtype]
            last_name = len(fields) - tuple(reversed(fields)).index("n")
            offset = 0
            for symbol in fields[:last_name]:
                if symbol == "n":
                    labels, offset = _read_name(
                        data, offset, canonical=False, compress=False
                    )
                    DomainName((*labels, b"")).to_wire(file, compress, origin)
                else:
                    size = _NUMBERS[symbol].size
                    file.write(data[offset : offset + size])
                    offset += size
            data = data[offset:]
        file.write(data)
        return None

    def to_digestable(self, origin: DomainName | None = None) -> bytes:
        return self.record(()).uncompressed_data(canonical=True)

    def __str__(self) -> str:
        return self.to_text()

    def _ordering(self) -> tuple[int, int, bytes]:
        return self.rdclass, self.rdtype, self.to_digestable()

    def __eq__(self, other):
        return (
            self._ordering() == other._ordering()
            if isinstance(other, Rdata)
            else NotImplemented
        )

    def __lt__(self, other):
        return (
            self._ordering() < other._ordering()
            if isinstance(other, Rdata)
            else NotImplemented
        )

    def __hash__(self):
        return hash(self._ordering())

    def replace(self, **changes) -> "Rdata":
        names = _PROPERTY_NAMES.get(self.rdtype, ())
        changes = {
            _FIELD_ALIASES.get(self.rdtype, {}).get(key, key): value
            for key, value in changes.items()
        }
        if "windows" in changes and names and names[-1] == "types":
            changes["types"] = _window_types(changes.pop("windows"))
        if not names or changes.keys() - set(names):
            raise ValueError("unknown or unsupported DNS RDATA field")
        values = tuple(
            changes.get(field, previous) for field, previous in zip(names, self.fields)
        )
        return from_text(
            self.rdclass,
            self.rdtype,
            _constructor_text(self.rdtype, values, self._display_origin),
            relativize=self._display_origin is not None,
            relativize_to=self._display_origin,
        )

    @classmethod
    def from_text(cls, rdclass, rdtype, text, origin=None) -> "Rdata":
        result = from_text(rdclass, rdtype, text, origin)
        if not isinstance(result, cls):
            raise ValueError("RDATA does not match the requested class")
        return result

    @classmethod
    def from_wire_parser(cls, rdclass, rdtype, parser) -> "Rdata":
        result = from_wire_parser(rdclass, rdtype, parser)
        if not isinstance(result, cls):
            raise ValueError("RDATA does not match the requested class")
        return result


class GenericRdata(Rdata):
    def to_text(self, origin: DomainName | None = None, relativize: bool = True) -> str:
        return f"\\# {len(self.data)} {self.data.hex().upper()}".rstrip()


# RFC 1035 types whose RDATA name fields allow message compression.
_COMPRESSIBLE = frozenset(
    {
        RecordType.NS,
        RecordType.MD,
        RecordType.MF,
        RecordType.CNAME,
        RecordType.SOA,
        RecordType.MB,
        RecordType.MG,
        RecordType.MR,
        RecordType.PTR,
        RecordType.MINFO,
        RecordType.MX,
    }
)


class SVCB(Rdata):
    _record_type = RecordType.SVCB

    def __init__(self, rdclass, rdtype, priority, target, params=()):
        if record_type(rdtype) != self._record_type:
            raise ValueError(f"expected {self._record_type.name} RDATA")
        from .rdtypes.svcbbase import Param, ParamKey

        pairs = params.items() if hasattr(params, "items") else params
        fields = tuple(
            sorted(
                (
                    ParamKey.make(code),
                    b""
                    if value is None
                    else value.to_wire()
                    if isinstance(value, Param)
                    else bytes(value),
                )
                for code, value in pairs
            )
        )
        if priority == 0 and fields:
            raise ValueError("SVCB AliasMode records cannot specify parameters")
        binding = ServiceBinding(priority, _origin(target), fields)
        super().__init__(rdclass, self._record_type, binding.to_wire())

    @property
    def priority(self):
        return self.fields[0].priority

    @property
    def target(self):
        return DomainName((*self.fields[0].target, b""))

    @property
    def params(self):
        from .rdtypes.svcbbase import ParamKey, decode_param

        return MappingProxyType(
            {
                ParamKey.make(key): decode_param(key, value)
                for key, value in self.fields[0].params
            }
        )

    @property
    def raw_params(self):
        return dict(self.fields[0].params)

    def replace(self, **changes):
        fields = {
            "priority": self.priority,
            "target": self.target,
            "params": self.params,
        }
        if changes.keys() - fields.keys():
            raise ValueError("unknown SVCB RDATA field")
        fields.update(changes)
        return type(self)(self.rdclass, self.rdtype, **fields)


class HTTPS(SVCB):
    _record_type = RecordType.HTTPS


def _constructor_text(
    kind: int, values: tuple, origin: DomainName | None = None
) -> str:
    output = []
    for symbol, value in zip(_FORMATS[kind], values):
        if symbol == "n":
            if isinstance(value, str):
                value = parse_name(value, _origin(origin))
            elif isinstance(value, DomainName):
                value = _origin(
                    value.derelativize(origin) if origin is not None else value
                )
        if symbol in ("s", "u") and isinstance(value, str):
            value = value.encode()
        if symbol == "S":
            value = tuple(
                part.encode() if isinstance(part, str) else part for part in value
            )
        if symbol == "r":
            value = record_type(value)
        if symbol == "m":
            value = _window_types(value)
        output.append(_format_field(symbol, value))
    return " ".join(output)


def _typed_class(kind: int, names: tuple[str, ...]) -> type[Rdata]:
    class_name = RecordType(kind).name

    def __init__(self, rdclass, rdtype, *values, **fields):
        if record_type(rdtype) != kind:
            raise ValueError(f"expected {class_name} RDATA")
        fields = {
            _FIELD_ALIASES.get(kind, {}).get(key, key): value
            for key, value in fields.items()
        }
        if "windows" in fields and names[-1] == "types":
            fields["types"] = fields.pop("windows")
        if kind == RecordType.ISDN:
            if "address" in fields:
                values = (fields.pop("address"), fields.pop("subaddress", None))
            if values and isinstance(values[0], (str, bytes)):
                values = (tuple(value for value in values if value is not None),)
        if len(values) > len(names):
            raise TypeError(f"too many {class_name} RDATA fields")
        remaining = names[len(values) :]
        if set(fields) != set(remaining):
            raise TypeError(f"{class_name} requires fields {', '.join(names)}")
        values += tuple(fields[field] for field in remaining)
        parsed = from_text(rdclass, kind, _constructor_text(kind, values))
        Rdata.__init__(self, parsed.rdclass, kind, parsed.data)

    def immutable(self, name, *unused):
        raise FrozenInstanceError(f"cannot modify {class_name} RDATA field {name!r}")

    return type(
        class_name,
        (Rdata,),
        {
            "__module__": __name__,
            "__init__": __init__,
            "__slots__": (),
            "__setattr__": immutable,
            "__delattr__": immutable,
        },
    )


_RDATA_CLASSES = {
    kind: _typed_class(kind, names) for kind, names in _PROPERTY_NAMES.items()
}
_RDATA_CLASSES.update({RecordType.SVCB: SVCB, RecordType.HTTPS: HTTPS})
globals().update({cls.__name__: cls for cls in _RDATA_CLASSES.values()})


def get_rdata_class(
    rdclass: int | str, rdtype: int | str, use_generic: bool = True
) -> type[Rdata] | None:
    """Find the detached RDATA class for a DNS class and type."""
    number, kind = record_class(rdclass), record_type(rdtype)
    from ._special_rdata import SPECIAL_CLASSES, ChaosA

    custom = _custom_class(number, kind)
    if custom is not None:
        return custom
    if number == RecordClass.CH and kind == RecordType.A:
        return ChaosA
    if kind in SPECIAL_CLASSES:
        return SPECIAL_CLASSES[kind]
    if kind in _RDATA_CLASSES:
        return _RDATA_CLASSES[kind]
    if (
        kind in _FORMATS
        or kind in KINDS
        or kind in (RecordType.SVCB, RecordType.HTTPS)
        or _codec(number, kind) is not None
    ):
        return Rdata
    return GenericRdata if use_generic else None


def _origin(name: DomainName | str | None) -> Name:
    if name is None:
        return ROOT
    if isinstance(name, str):
        return parse_name(name)
    if not name.is_absolute():
        raise ValueError("DNS RDATA origin must be absolute")
    return name.labels[:-1]


def _rdata(record: ResourceRecord) -> Rdata:
    custom = _custom_class(record.rdclass, record.type)
    if custom is not None:
        packet = record._packet if record._packet else record.data
        start = record._offset if record._packet else 0
        parser = Parser(packet, start)
        with parser.restrict_to(len(record.data)):
            return custom.from_wire_parser(record.rdclass, record.type, parser)
    data = record.uncompressed_data()
    cls = get_rdata_class(record.rdclass, record.type)
    result = object.__new__(cls)
    Rdata.__init__(result, record.rdclass, record.type, data)
    if cls is not GenericRdata:
        result.fields
    return result


def from_text(
    rdclass: int | str,
    rdtype: int | str,
    text: str | Tokenizer,
    origin: DomainName | str | None = None,
    relativize: bool = False,
    relativize_to: DomainName | str | None = None,
    idna_codec=None,
) -> Rdata:
    if isinstance(text, Tokenizer):
        tokens = tuple(token.value for token in text._remaining(presentation=True))
        if idna_codec is None:
            idna_codec = text.idna_codec
    else:
        lines = tuple(master_tokens(text))
        if len(lines) > 1:
            raise ValueError("expected one DNS RDATA value")
        tokens = lines[0][2] if lines else ()
    result = _rdata(
        from_tokens(
            (),
            0,
            rdclass,
            rdtype,
            tokens,
            origin=_origin(origin),
            idna_codec=idna_codec,
        )
    )
    if relativize:
        display_origin = _origin(origin if relativize_to is None else relativize_to)
        object.__setattr__(
            result, "_display_origin", DomainName((*display_origin, b""))
        )
    return result


def from_wire(
    rdclass: int | str,
    rdtype: int | str,
    wire: bytes,
    current: int = 0,
    rdlen: int | None = None,
    origin: DomainName | str | None = None,
) -> Rdata:
    end = len(wire) if rdlen is None else current + rdlen
    if not 0 <= current <= end <= len(wire):
        raise WireError("DNS RDATA lies outside the packet")
    result = _rdata(
        ResourceRecord(
            (),
            record_type(rdtype),
            record_class(rdclass),
            0,
            wire[current:end],
            wire,
            current,
        )
    )
    if origin is not None:
        object.__setattr__(
            result, "_display_origin", DomainName((*_origin(origin), b""))
        )
    return result


def from_record(record: ResourceRecord) -> Rdata:
    return _rdata(record)


def from_wire_parser(
    rdclass: int | str, rdtype: int | str, parser: Parser, origin=None
) -> Rdata:
    result = from_wire(
        rdclass, rdtype, parser.wire, parser.current, parser.remaining(), origin
    )
    parser.get_remaining()
    return result


def load_all_types() -> None:
    """Load the built-in DNS RDATA implementations."""
    from ._special_rdata import SPECIAL_CLASSES

    for kind in (*_RDATA_CLASSES, *SPECIAL_CLASSES):
        get_rdata_class(RecordClass.IN, kind)
