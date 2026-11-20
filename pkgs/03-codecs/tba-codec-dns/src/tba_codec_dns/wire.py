"""DNS names, questions, and resource records (RFC 1035)."""

import secrets
from contextlib import contextmanager
from dataclasses import dataclass, field, replace
from enum import IntEnum
from pathlib import Path
from struct import Struct

from tba_primitives_dns_name._wire import (
    WireError,
    _append_name,
    _name_wire,
    _read_name,
)
from tba_primitives_dns_name.name import Name as DomainName
from tba_primitives_dns_name.name import from_text as name_from_text
from tba_primitives_dns_name.names import Name, parse_name
from tba_primitives_dns_name.names import check_name as check_name

_HEADER = Struct("!6H")
_QUESTION = Struct("!2H")
_RECORD = Struct("!HHIH")
_UNSPECIFIED_KEYRING = object()


class TooBig(WireError):
    """A DNS message cannot be rendered within the requested limit."""


class ShortHeader(WireError):
    """The packet does not contain the complete DNS header."""


class TrailingJunk(WireError):
    """The packet contains data beyond the advertised DNS sections."""


class BadTSIG(WireError):
    """A TSIG record is misplaced or has invalid metadata."""


class UnknownTSIGKey(WireError):
    """No verification key matches a signed DNS message."""


@dataclass(frozen=True)
class MessageError:
    exception: WireError
    offset: int


class Truncated(WireError):
    """A DNS reply is flagged as truncated."""

    def __init__(self, message: str, partial: "Message | None" = None):
        super().__init__(message)
        self.partial = partial


class Parser:
    """A bounded cursor for parsing DNS wire fields."""

    def __init__(self, wire: bytes, current: int = 0) -> None:
        if not 0 <= current <= len(wire):
            raise WireError("DNS parser offset outside the packet")
        self.wire = bytes(wire)
        self.current = self.furthest = current
        self._start = 0
        self.end = len(wire)

    def remaining(self) -> int:
        return self.end - self.current

    def seek(self, position: int) -> None:
        if not self._start <= position <= self.end:
            raise WireError("DNS parser offset outside the current bounds")
        self.current = position

    def get_bytes(self, size: int) -> bytes:
        if not 0 <= size <= self.remaining():
            raise WireError("truncated DNS wire field")
        start = self.current
        self.current += size
        self.furthest = max(self.furthest, self.current)
        return self.wire[start : self.current]

    def get_remaining(self) -> bytes:
        return self.get_bytes(self.remaining())

    def get_counted_bytes(self, length: int = 1) -> bytes:
        if not 1 <= length <= 8:
            raise ValueError("DNS length field requires one to eight octets")
        return self.get_bytes(int.from_bytes(self.get_bytes(length), "big"))

    def get_uint8(self) -> int:
        return self.get_bytes(1)[0]

    def get_uint16(self) -> int:
        return int.from_bytes(self.get_bytes(2), "big")

    def get_uint32(self) -> int:
        return int.from_bytes(self.get_bytes(4), "big")

    def get_uint48(self) -> int:
        return int.from_bytes(self.get_bytes(6), "big")

    def get_struct(self, format: str | Struct) -> tuple:
        spec = Struct(format) if isinstance(format, str) else format
        return spec.unpack(self.get_bytes(spec.size))

    def get_name(self, origin=None):
        from tba_primitives_dns_name.name import from_wire as parse_name_wire

        name, size = parse_name_wire(self.wire, self.current)
        self.get_bytes(size)
        return name.relativize(origin) if origin is not None else name

    @contextmanager
    def restrict_to(self, size: int):
        if not 0 <= size <= self.remaining():
            raise WireError("DNS parser bound exceeds the packet")
        old = self._start, self.end
        self._start = self.current
        self.end = self.current + size
        try:
            yield self
            if self.current != self.end:
                raise WireError("unconsumed DNS field data")
        finally:
            self._start, self.end = old

    @contextmanager
    def restore_furthest(self):
        try:
            yield self
        finally:
            self.seek(min(self.end, max(self._start, self.furthest)))


class RecordType(IntEnum):
    A = 1
    NS = 2
    MD = 3
    MF = 4
    CNAME = 5
    SOA = 6
    MB = 7
    MG = 8
    MR = 9
    NULL = 10
    WKS = 11
    PTR = 12
    HINFO = 13
    MINFO = 14
    MX = 15
    TXT = 16
    RP = 17
    AFSDB = 18
    X25 = 19
    ISDN = 20
    RT = 21
    NSAP = 22
    NSAP_PTR = 23
    SIG = 24
    KEY = 25
    PX = 26
    GPOS = 27
    AAAA = 28
    LOC = 29
    NXT = 30
    EID = 31
    NIMLOC = 32
    SRV = 33
    ATMA = 34
    NAPTR = 35
    KX = 36
    CERT = 37
    A6 = 38
    DNAME = 39
    SINK = 40
    OPT = 41
    APL = 42
    DS = 43
    SSHFP = 44
    IPSECKEY = 45
    RRSIG = 46
    NSEC = 47
    DNSKEY = 48
    DHCID = 49
    NSEC3 = 50
    NSEC3PARAM = 51
    TLSA = 52
    SMIMEA = 53
    HIP = 55
    NINFO = 56
    RKEY = 57
    TALINK = 58
    CDS = 59
    CDNSKEY = 60
    OPENPGPKEY = 61
    CSYNC = 62
    ZONEMD = 63
    SVCB = 64
    HTTPS = 65
    DSYNC = 66
    HHIT = 67
    BRID = 68
    SPF = 99
    NID = 104
    L32 = 105
    L64 = 106
    LP = 107
    EUI48 = 108
    EUI64 = 109
    NXNAME = 128
    TKEY = 249
    TSIG = 250
    IXFR = 251
    AXFR = 252
    MAILB = 253
    MAILA = 254
    ANY = 255
    URI = 256
    CAA = 257
    AVC = 258
    DOA = 259
    AMTRELAY = 260
    RESINFO = 261
    WALLET = 262
    CLA = 263
    IPN = 264
    TA = 32768
    DLV = 32769


class RecordClass(IntEnum):
    IN = 1
    CH = 3
    HS = 4
    NONE = 254
    ANY = 255


class Section(IntEnum):
    QUESTION = 0
    ANSWER = 1
    AUTHORITY = 2
    ADDITIONAL = 3


class CopyMode(IntEnum):
    NOTHING = 0
    QUESTION = 1
    EVERYTHING = 2


def _number(value: int | str, enum: type[IntEnum], prefix: str) -> int:
    if isinstance(value, str):
        token = value.upper().replace("-", "_")
        if (
            token.startswith(prefix)
            and token[len(prefix) :].isascii()
            and token[len(prefix) :].isdecimal()
        ):
            value = int(token[len(prefix) :])
        else:
            try:
                value = enum[token]
            except KeyError as exc:
                raise ValueError(f"unknown DNS {prefix.lower()} {value!r}") from exc
    if not 0 <= value <= 65535:
        raise ValueError(f"DNS {prefix.lower()} is outside 0..65535")
    return value


_EXTRA_TYPE_BY_NAME: dict[str, int] = {}
_EXTRA_TYPE_BY_NUMBER: dict[int, str] = {}


def record_type(value: int | str) -> int:
    if isinstance(value, str):
        value = _EXTRA_TYPE_BY_NAME.get(value.upper(), value)
    return _number(value, RecordType, "TYPE")


def record_class(value: int | str) -> int:
    return _number(value, RecordClass, "CLASS")


def type_text(value: int) -> str:
    try:
        return RecordType(value).name.replace("_", "-")
    except ValueError:
        return _EXTRA_TYPE_BY_NUMBER.get(value, f"TYPE{value}")


def class_text(value: int) -> str:
    try:
        return RecordClass(value).name
    except ValueError:
        return f"CLASS{value}"


@dataclass(frozen=True)
class Question:
    name: Name
    type: int
    rdclass: int = 1

    @classmethod
    def _read(cls, packet: bytes, offset: int) -> tuple["Question", int]:
        name, offset = _read_name(packet, offset)
        if offset + _QUESTION.size > len(packet):
            raise WireError("truncated DNS question")
        rdtype, rdclass = _QUESTION.unpack_from(packet, offset)
        return cls(name, rdtype, rdclass), offset + _QUESTION.size

    @classmethod
    def from_text(
        cls,
        name: str | DomainName,
        rdtype: int | str,
        rdclass: int | str = 1,
        *,
        idna_codec=None,
    ) -> "Question":
        kind, class_number = record_type(rdtype), record_class(rdclass)
        if not kind or not class_number:
            raise ValueError("DNS record type and class must be in 1..65535")
        if isinstance(name, DomainName) or idna_codec is not None:
            parsed = (
                name
                if isinstance(name, DomainName)
                else name_from_text(name, idna_codec=idna_codec)
            )
            labels = parsed.labels[:-1] if parsed.is_absolute() else parsed.labels
            return cls(tuple(label.lower() for label in labels), kind, class_number)
        return cls(parse_name(name, canonical=True), kind, class_number)

    def to_wire(self) -> bytes:
        return _name_wire(self.name) + _QUESTION.pack(self.type, self.rdclass)

    def query_wire(
        self,
        identifier: int,
        *,
        edns_payload: int | None = None,
        want_dnssec: bool = False,
        edns_options: tuple["EdnsOption", ...] = (),
    ) -> bytes:
        return self.query_message(
            identifier,
            edns_payload=edns_payload,
            want_dnssec=want_dnssec,
            edns_options=edns_options,
        ).to_wire()

    def query_message(
        self,
        identifier: int,
        *,
        edns_payload: int | None = None,
        want_dnssec: bool = False,
        edns_options: tuple["EdnsOption", ...] = (),
    ) -> "Message":
        if (want_dnssec or edns_options) and edns_payload is None:
            edns_payload = 1232
        additional = ()
        if edns_payload is not None:
            additional = (
                opt_record(
                    edns_payload,
                    flags=0x8000 if want_dnssec else 0,
                    options=edns_options,
                ),
            )
        return Message(identifier, 0x0100, (self,), additional=additional)


@dataclass(frozen=True)
class ResourceRecord:
    name: Name
    type: int
    rdclass: int
    ttl: int
    data: bytes
    _packet: bytes = field(default=b"", repr=False, compare=False)
    _offset: int = field(default=0, repr=False, compare=False)
    _start: int = field(default=0, repr=False, compare=False)

    def uncompressed_data(self, *, canonical: bool = False) -> bytes:
        from .rdata import uncompressed_data

        return uncompressed_data(self, canonical=canonical)

    def to_wire(self, *, canonical: bool = False) -> bytes:
        name = tuple(label.lower() for label in self.name) if canonical else self.name
        data = self.uncompressed_data(canonical=canonical)
        return (
            _name_wire(name)
            + _RECORD.pack(self.type, self.rdclass, self.ttl, len(data))
            + data
        )

    @property
    def strings(self) -> tuple[bytes, ...]:
        if self.type != RecordType.TXT:
            raise ValueError("record must have type TXT")
        parts = []
        position = 0
        if not self.data:
            raise WireError("empty TXT payload")
        while position < len(self.data):
            end = position + 1 + self.data[position]
            if end > len(self.data):
                raise WireError("truncated TXT string")
            parts.append(self.data[position + 1 : end])
            position = end
        return tuple(parts)

    def read_name(self, offset: int = 0, *, canonical: bool = True) -> tuple[Name, int]:
        """Decode a possibly compressed name within this record's data."""
        if not 0 <= offset < len(self.data):
            raise WireError("name starts outside DNS record")
        packet = self._packet or self.data
        name, end = _read_name(
            packet,
            self._offset + offset,
            canonical=canonical,
            compress=bool(self._packet),
        )
        if end > self._offset + len(self.data):
            raise WireError("name extends outside DNS record")
        return name, end - self._offset


def _rrset_boundaries(records: tuple[ResourceRecord, ...]):
    """Yield contiguous ranges that never split an RRset."""
    identities = []
    last = {}
    for index, rr in enumerate(records):
        covered = rr.data[:2] if rr.type in (RecordType.RRSIG, RecordType.SIG) else b""
        identity = (
            tuple(label.lower() for label in rr.name),
            rr.rdclass,
            rr.type,
            covered,
        )
        identities.append(identity)
        last[identity] = index
    start = stop = 0
    for index, identity in enumerate(identities):
        stop = max(stop, last[identity])
        if index == stop:
            yield start, stop + 1
            start = stop + 1


@dataclass(frozen=True)
class Message:
    id: int
    flags: int
    questions: tuple[Question, ...] = ()
    answers: tuple[ResourceRecord, ...] = ()
    authority: tuple[ResourceRecord, ...] = ()
    additional: tuple[ResourceRecord, ...] = ()
    _wire: bytes = field(default=b"", repr=False, compare=False)
    _pad: int = field(default=0, repr=False, compare=False)
    errors: tuple[MessageError, ...] = field(default=(), compare=False)
    tsig_key: object | None = field(default=None, repr=False, compare=False)
    tsig_ctx: object | None = field(default=None, repr=False, compare=False)
    request_mac: bytes = field(default=b"", repr=False, compare=False)
    _fudge: int = field(default=300, repr=False, compare=False)
    _sign_on_wire: bool = field(default=False, repr=False, compare=False)
    _original_id: int | None = field(default=None, repr=False, compare=False)
    _tsig_error: int = field(default=0, repr=False, compare=False)
    _other_data: bytes = field(default=b"", repr=False, compare=False)
    origin: DomainName | None = field(default=None, repr=False, compare=False)
    xfr: bool = field(default=False, compare=False)
    one_rr_per_rrset: bool = field(default=False, compare=False)
    request_payload: int = field(default=0, compare=False)
    time: float = field(default=0.0, compare=False)

    @property
    def had_tsig(self) -> bool:
        return bool(self.additional and self.additional[-1].type == RecordType.TSIG)

    @property
    def mac(self) -> bytes | None:
        from .tsig import TsigRecord

        return (
            TsigRecord.from_data(self.additional[-1].data).mac
            if self.had_tsig
            else None
        )

    def use_tsig(
        self,
        keyring,
        keyname=None,
        fudge: int = 300,
        original_id: int | None = None,
        tsig_error: int = 0,
        other_data: bytes = b"",
        algorithm="hmac-sha256.",
        *,
        request_mac: bytes = b"",
    ) -> "Message":
        """Return a message configured to sign its rendered wire data."""
        from .tsig import signing_key

        key = signing_key(keyring, keyname, algorithm)
        if not 0 <= fudge <= 65535:
            raise ValueError("TSIG fudge outside its wire range")
        return replace(
            self,
            tsig_key=key,
            request_mac=request_mac,
            _fudge=fudge,
            _sign_on_wire=True,
            _original_id=original_id,
            _tsig_error=tsig_error,
            _other_data=bytes(other_data),
        )

    @property
    def sections(self) -> tuple:
        return self.questions, self.answers, self.authority, self.additional

    @property
    def wire(self) -> bytes:
        return self._wire

    def is_response(self, response: "Message") -> bool:
        if self.flags & 0x8000 or not response.flags & 0x8000:
            return False
        if self.id != response.id or self.opcode != response.opcode:
            return False
        if not response.questions and (
            self.opcode == 5 or response.rcode in (1, 2, 4, 5)
        ):
            return True

        def normalized(questions):
            return tuple(
                (tuple(label.lower() for label in q.name), q.type, q.rdclass)
                for q in questions
            )

        return normalized(self.questions) == normalized(response.questions)

    def section_number(self, section) -> Section:
        if isinstance(section, str):
            try:
                return Section[section.upper()]
            except KeyError as exc:
                raise ValueError("unknown DNS message section") from exc
        if isinstance(section, int):
            return Section(section)
        for position, records in enumerate(self.sections):
            if section is records:
                return Section(position)
        raise ValueError("section does not belong to the DNS message")

    def rrsets(self, section) -> tuple:
        """Return the section as grouped RRsets, excluding OPT and TSIG."""
        from .rrset import RRset

        number = self.section_number(section)
        records = self.sections[number]
        if number == Section.QUESTION:
            return tuple(
                RRset(q.name, q.rdclass, q.type, 0, (), self.origin) for q in records
            )
        groups = {}
        for i, rr in enumerate(records):
            if rr.type in (RecordType.OPT, RecordType.TSIG):
                continue
            covers = (
                rr.data[:2] if rr.type in (RecordType.RRSIG, RecordType.SIG) else b""
            )
            separate = self.one_rr_per_rrset or (self.xfr and rr.type == RecordType.SOA)
            key = (
                tuple(label.lower() for label in rr.name),
                rr.rdclass,
                rr.type,
                covers,
                i if separate else -1,
            )
            groups.setdefault(key, []).append(rr)
        return tuple(
            RRset(*key[:3], min(rr.ttl for rr in values), tuple(values), self.origin)
            for key, values in groups.items()
        )

    def get_rrset(
        self,
        section,
        name,
        rdclass: int | str,
        rdtype: int | str,
        covers: int | str = 0,
    ):
        from .rdata import decoded
        from .rrset import RRset

        number = self.section_number(section)
        if isinstance(name, str):
            labels = () if self.origin is None else self.origin.labels[:-1]
            owner = parse_name(name, labels, canonical=True)
        elif isinstance(name, DomainName):
            if not name.is_absolute():
                if self.origin is None:
                    raise ValueError("DNS message owner must be an absolute name")
                name = name.derelativize(self.origin)
            owner = tuple(label.lower() for label in name.labels[:-1])
        else:
            owner = tuple(label.lower() for label in name)
        identity = (owner, record_class(rdclass), record_type(rdtype))
        matches = tuple(
            rr
            for rr in self.sections[number]
            if (tuple(label.lower() for label in rr.name), rr.rdclass, rr.type)
            == identity
        )
        if number == Section.QUESTION:
            return RRset(*identity, 0, (), self.origin) if matches else None
        covering = record_type(covers)
        if identity[2] in (RecordType.RRSIG, RecordType.SIG):
            matches = tuple(
                rr for rr in matches if rr.data and decoded(rr)[0] == covering
            )
        elif covering:
            return None
        if not matches:
            return None
        if self.one_rr_per_rrset or (self.xfr and identity[2] == RecordType.SOA):
            matches = matches[:1]
        return RRset(*identity, min(rr.ttl for rr in matches), matches, self.origin)

    def find_rrset(
        self,
        section,
        name,
        rdclass: int | str,
        rdtype: int | str,
        covers: int | str = 0,
    ):
        rrset = self.get_rrset(section, name, rdclass, rdtype, covers)
        if rrset is None:
            raise KeyError((section, name, rdclass, rdtype, covers))
        return rrset

    @property
    def opcode(self) -> int:
        return (self.flags >> 11) & 15

    @property
    def edns(self) -> "Edns | None":
        opt = next((rr for rr in self.additional if rr.type == RecordType.OPT), None)
        return None if opt is None else Edns.from_record(opt)

    def get_options(self, option_type: int) -> tuple["EdnsOption", ...]:
        edns = self.edns
        if edns is None:
            return ()
        return tuple(option for option in edns.options if option.code == option_type)

    def extended_errors(self):
        from .edns import ExtendedError

        return tuple(
            ExtendedError.from_option(option) for option in self.get_options(15)
        )

    def to_wire(
        self,
        *,
        compress: bool = False,
        max_size: int = 0,
        prefer_truncation: bool = False,
        prepend_length: bool = False,
        tsig_ctx=None,
    ) -> bytes:
        max_size = max_size or self.request_payload or 65535
        if not _HEADER.size <= max_size <= 65535:
            raise ValueError("DNS wire size limit is outside the protocol range")
        packet = self._render(compress, max_size, prefer_truncation)
        if self._pad:
            packet = self._render_padding(packet, compress, max_size, prefer_truncation)
        if self._sign_on_wire and not self.had_tsig:
            from .tsig import sign

            packet, _ = sign(
                packet,
                self.tsig_key,
                request_mac=self.request_mac or None,
                fudge=self._fudge,
                original_id=self._original_id,
                error=self._tsig_error,
                other=self._other_data,
                context=tsig_ctx,
            )
            if len(packet) > max_size:
                raise TooBig("signed DNS message exceeds the wire size limit")
        return len(packet).to_bytes(2, "big") + packet if prepend_length else packet

    def _render_padding(
        self, packet: bytes, compress: bool, limit: int, truncate: bool
    ) -> bytes:
        size = (-len(packet) - 4) % self._pad
        if len(packet) + 4 + size > limit or any(
            rr.type == RecordType.TSIG for rr in self.additional
        ):
            return packet
        option = EdnsOption(12, bytes(size)).to_wire()
        padded = replace(
            self,
            additional=tuple(
                replace(rr, data=rr.data + option) if rr.type == RecordType.OPT else rr
                for rr in self.additional
            ),
        )
        return padded._render(compress, limit, truncate)

    def _render(self, compress: bool, limit: int, truncate: bool) -> bytes:
        has_tsig = any(rr.type == RecordType.TSIG for rr in self.additional)
        if has_tsig and self._wire:
            if self != Message.from_wire(self._wire):
                raise WireError("changed DNS message must be signed again")
            if len(self._wire) > limit:
                raise TooBig("signed DNS message exceeds the wire size limit")
            return self._wire
        output = bytearray(_HEADER.size)
        offsets: dict[Name, int] = {}

        def append(item: Question | ResourceRecord) -> None:
            if not compress or has_tsig:
                output.extend(item.to_wire())
                return
            _append_name(output, item.name, offsets)
            if isinstance(item, Question):
                output.extend(_QUESTION.pack(item.type, item.rdclass))
            else:
                data = item.uncompressed_data()
                output.extend(
                    _RECORD.pack(item.type, item.rdclass, item.ttl, len(data))
                )
                output.extend(data)

        flags = self.flags
        truncate = (
            truncate and bool(flags & 0x8000) and self.opcode == 0 and not has_tsig
        )
        additional = self.additional
        opt = b""
        if truncate:
            opts = tuple(rr for rr in additional if rr.type == RecordType.OPT)
            if len(opts) > 1:
                raise WireError("duplicate EDNS OPT record")
            if opts:
                opt = opts[0].to_wire()
            additional = tuple(rr for rr in additional if rr.type != RecordType.OPT)
        if _HEADER.size + len(opt) > limit:
            raise TooBig("EDNS exceeds the DNS wire size limit")
        counts = [len(self.questions), 0, 0, 0]
        for item in self.questions:
            append(item)
            if len(output) + len(opt) > limit:
                raise TooBig("DNS question and EDNS exceed the wire size limit")
        for number, section in enumerate((self.answers, self.authority, additional), 1):
            ranges = (
                _rrset_boundaries(section)
                if truncate
                else ((i, i + 1) for i in range(len(section)))
            )
            for start, end in ranges:
                initial_size = len(output)
                for index in range(start, end):
                    append(section[index])
                    if len(output) + len(opt) > limit:
                        break
                if len(output) + len(opt) > limit:
                    if not truncate:
                        raise TooBig("DNS message exceeds the wire size limit")
                    del output[initial_size:]
                    if number != Section.ADDITIONAL:
                        flags |= 0x0200
                    break
                counts[number] += end - start
            else:
                continue
            break
        if opt:
            output.extend(opt)
            counts[Section.ADDITIONAL] += 1
        _HEADER.pack_into(output, 0, self.id, flags, *counts)
        return bytes(output)

    def to_text(self) -> str:
        from .presentation import message_text

        return message_text(self)

    @classmethod
    def from_text(cls, text: str) -> "Message":
        from .presentation import parse_message

        return parse_message(text)

    @classmethod
    def from_file(cls, source) -> "Message":
        if not hasattr(source, "readline"):
            with Path(source).open(encoding="utf-8") as handle:
                return cls.from_file(handle)
        lines = []
        while line := source.readline():
            if not line.strip():
                if lines:
                    break
                continue
            lines.append(line.decode("utf-8") if isinstance(line, bytes) else line)
        return cls.from_text("".join(lines))

    @property
    def rcode(self) -> int:
        extended = next(
            (rr.ttl >> 24 for rr in self.additional if rr.type == RecordType.OPT), 0
        )
        return (extended << 4) | (self.flags & 15)

    @classmethod
    def from_wire(
        cls,
        packet: bytes,
        keyring=_UNSPECIFIED_KEYRING,
        *,
        question_only: bool = False,
        ignore_trailing: bool = False,
        raise_on_truncation: bool = False,
        continue_on_error: bool = False,
        request_mac: bytes | None = None,
        multi: bool = False,
        tsig_ctx=None,
        origin=None,
        xfr: bool = False,
        one_rr_per_rrset: bool = False,
    ) -> "Message":
        if isinstance(origin, str):
            origin = name_from_text(origin)
        if origin is not None and (
            not isinstance(origin, DomainName) or not origin.is_absolute()
        ):
            raise ValueError("DNS message origin must be an absolute name")
        if len(packet) < _HEADER.size:
            raise ShortHeader("DNS message has an incomplete header")
        if len(packet) > 65535:
            raise WireError("invalid DNS message size")
        ident, flags, qd, an, ns, ar = _HEADER.unpack_from(packet)
        offset = _HEADER.size
        questions = []
        for _ in range(qd):
            question, offset = Question._read(packet, offset)
            questions.append(question)
        if raise_on_truncation and flags & 0x0200:
            partial = cls(ident, flags, tuple(questions), _wire=packet)
            raise Truncated("truncated DNS response", partial)
        if question_only:
            return cls(
                ident,
                flags,
                tuple(questions),
                _wire=packet,
                origin=origin,
                xfr=xfr,
                one_rr_per_rrset=one_rr_per_rrset,
            )
        sections = []
        errors = []
        framing_lost = False
        for section, count in enumerate((an, ns, ar), 1):
            records = []
            for index in range(0 if framing_lost else count):
                start = offset
                try:
                    name, header = _read_name(packet, offset)
                    if header + _RECORD.size > len(packet):
                        raise WireError("truncated DNS record header")
                    rdtype, rdclass, ttl, size = _RECORD.unpack_from(packet, header)
                    body = header + _RECORD.size
                    offset = body + size
                    if offset > len(packet):
                        raise WireError("truncated DNS record data")
                except WireError as exc:
                    if not continue_on_error:
                        raise
                    errors.append(MessageError(exc, start))
                    framing_lost = True
                    break
                record = ResourceRecord(
                    name, rdtype, rdclass, ttl, packet[body:offset], packet, body, start
                )
                if rdtype == RecordType.TSIG and (
                    section != Section.ADDITIONAL or index != count - 1
                ):
                    raise BadTSIG(
                        "TSIG must be the final record in the additional section"
                    )
                if (
                    continue_on_error
                    and rdtype not in (RecordType.OPT, RecordType.TSIG)
                    and (size or rdclass not in (RecordClass.ANY, RecordClass.NONE))
                ):
                    from .rdata import from_record

                    try:
                        from_record(record)
                    except ValueError as exc:
                        error = (
                            exc if isinstance(exc, WireError) else WireError(str(exc))
                        )
                        errors.append(MessageError(error, start))
                        continue
                records.append(record)
            sections.append(tuple(records))
        if not framing_lost and offset != len(packet) and not ignore_trailing:
            extra = TrailingJunk("unexpected trailing bytes in DNS message")
            if not continue_on_error:
                raise extra
            errors.append(MessageError(extra, offset))
        answers, authority, additional = sections
        options = tuple(rr for rr in additional if rr.type == RecordType.OPT)
        if len(options) > 1 or any(
            rr.type == RecordType.OPT for rr in (*answers, *authority)
        ):
            raise WireError("misplaced or duplicate EDNS OPT record")
        if options:
            Edns.from_record(options[0])
        result = cls(
            ident,
            flags,
            tuple(questions),
            answers,
            authority,
            additional,
            packet,
            errors=tuple(errors),
            request_mac=request_mac or b"",
            origin=origin,
            xfr=xfr,
            one_rr_per_rrset=one_rr_per_rrset,
        )
        if keyring is not False and (
            keyring is not _UNSPECIFIED_KEYRING or request_mac or tsig_ctx is not None
        ):
            from .tsig import authenticate_message

            return authenticate_message(result, keyring, multi=multi, context=tsig_ctx)
        return result


from_wire = Message.from_wire
from_text = Message.from_text
from_file = Message.from_file


@dataclass(frozen=True)
class EdnsOption:
    code: int
    data: bytes = b""

    def to_wire(self) -> bytes:
        return _QUESTION.pack(self.code, len(self.data)) + self.data


@dataclass(frozen=True)
class Edns:
    payload: int
    version: int
    flags: int
    extended_rcode: int
    options: tuple[EdnsOption, ...]

    @classmethod
    def from_record(cls, record: ResourceRecord) -> "Edns":
        if record.name or record.type != RecordType.OPT:
            raise WireError("EDNS OPT must have a root owner")
        options = []
        offset = 0
        while offset < len(record.data):
            if offset + _QUESTION.size > len(record.data):
                raise WireError("truncated EDNS option header")
            code, size = _QUESTION.unpack_from(record.data, offset)
            offset += _QUESTION.size
            end = offset + size
            if end > len(record.data):
                raise WireError("truncated EDNS option")
            options.append(EdnsOption(code, record.data[offset:end]))
            offset = end
        return cls(
            record.rdclass,
            (record.ttl >> 16) & 255,
            record.ttl & 65535,
            record.ttl >> 24,
            tuple(options),
        )


def opt_record(
    payload: int = 1232,
    *,
    version: int = 0,
    flags: int = 0,
    rcode: int = 0,
    options: tuple[EdnsOption, ...] = (),
) -> ResourceRecord:
    if not (
        512 <= payload <= 65535
        and 0 <= version <= 255
        and 0 <= flags <= 65535
        and 0 <= rcode <= 255
    ):
        raise ValueError("EDNS parameters out of range")
    return ResourceRecord(
        (),
        RecordType.OPT,
        payload,
        (rcode << 24) | (version << 16) | flags,
        b"".join(option.to_wire() for option in options),
    )


def make_query(
    name: str | DomainName,
    rdtype: int | str = RecordType.A,
    rdclass: int | str = RecordClass.IN,
    *,
    identifier: int | None = None,
    edns_payload: int | None = None,
    want_dnssec: bool = False,
    edns_options: tuple[EdnsOption, ...] = (),
    pad: int = 0,
    use_edns: int | bool | None = None,
    ednsflags: int = 0,
    payload: int | None = None,
    request_payload: int = 0,
    options=None,
    idna_codec=None,
    id: int | None = None,
    flags: int = 0x0100,
) -> Message:
    question = Question.from_text(name, rdtype, rdclass, idna_codec=idna_codec)
    if id is not None:
        if identifier is not None and identifier != id:
            raise ValueError("conflicting DNS query identifiers")
        identifier = id
    if payload is not None:
        if edns_payload is not None and edns_payload != payload:
            raise ValueError("conflicting EDNS payload sizes")
        edns_payload = payload
    if options is not None:
        if edns_options:
            raise ValueError("specify only one EDNS option collection")
        edns_options = tuple(options)
    if not 0 <= pad <= 65535:
        raise ValueError("DNS padding block size is outside the wire range")
    if not 0 <= flags <= 65535 or not 0 <= ednsflags <= 65535:
        raise ValueError("DNS flags are outside the wire range")
    if request_payload and not _HEADER.size <= request_payload <= 65535:
        raise ValueError("DNS request payload is outside the wire range")
    identifier = secrets.randbits(16) if identifier is None else identifier
    if use_edns is False or use_edns == -1:
        return Message(identifier, flags, (question,), request_payload=request_payload)
    if (use_edns is not None or ednsflags) and edns_payload is None:
        edns_payload = 1232
    if pad:
        if edns_payload is None:
            edns_payload = 1232
        edns_options = tuple(option for option in edns_options if option.code != 12)
    query = question.query_message(
        identifier,
        edns_payload=edns_payload,
        want_dnssec=want_dnssec,
        edns_options=edns_options,
    )
    if edns := query.edns:
        version = 0 if use_edns is True or use_edns is None else use_edns
        options_record = opt_record(
            edns.payload,
            version=version,
            flags=edns.flags | ednsflags,
            options=edns.options,
        )
        query = replace(query, additional=(options_record,))
    return replace(query, flags=flags, _pad=pad, request_payload=request_payload)


def make_response(
    query: Message,
    *,
    rcode: int = 0,
    authoritative: bool = False,
    recursion_available: bool = False,
    edns_payload: int = 1232,
    copy_mode: CopyMode | None = None,
    pad: int | None = None,
) -> Message:
    if query.flags & 0x8000 or not 0 <= rcode <= 4095:
        raise ValueError("expected a DNS query and a valid response code")
    flags = 0x8000 | (query.flags & 0x7910) | (rcode & 15)
    if authoritative:
        flags |= 0x0400
    if recursion_available:
        flags |= 0x0080
    received_edns = query.edns
    if pad is None:
        pad = 468 if query._pad or query.get_options(12) else 0
    if not 0 <= pad <= 65535:
        raise ValueError("DNS padding block size is outside the wire range")
    extra = ()
    if received_edns is not None or rcode > 15 or pad:
        edns_flags = 0 if received_edns is None else received_edns.flags & 0x8000
        extra = (opt_record(edns_payload, flags=edns_flags, rcode=rcode >> 4),)
    mode = CopyMode.QUESTION if copy_mode is None else CopyMode(copy_mode)
    auth = {}
    if query.had_tsig and query.tsig_key is not None:
        auth = {
            "tsig_key": query.tsig_key,
            "request_mac": query.mac or b"",
            "_sign_on_wire": True,
        }
    if mode == CopyMode.EVERYTHING:
        copied = tuple(
            rr
            for rr in query.additional
            if rr.type not in (RecordType.OPT, RecordType.TSIG)
        )
        return Message(
            query.id,
            flags,
            query.questions,
            query.answers,
            query.authority,
            (*copied, *extra),
            _pad=pad,
            **auth,
        )
    questions = query.questions if mode == CopyMode.QUESTION else ()
    return Message(query.id, flags, questions, additional=extra, _pad=pad, **auth)


def response_flags(
    packet: bytes,
    identifier: int,
    question: Question,
    *,
    opcode: int = 0,
    allow_empty_question: bool = False,
) -> int:
    if len(packet) < _HEADER.size:
        raise WireError("truncated DNS header")
    actual, flags, count, *_ = _HEADER.unpack_from(packet)
    matching = (
        count == 0
        and allow_empty_question
        or count == 1
        and Question._read(packet, _HEADER.size)[0] == question
    )
    if (
        actual != identifier
        or flags & 0xF800 != (0x8000 | (opcode << 11))
        or not matching
    ):
        raise WireError("DNS response does not match the query")
    return flags
