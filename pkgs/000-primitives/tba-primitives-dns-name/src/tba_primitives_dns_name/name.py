"""Case-insensitive DNS names with explicit root and relative-name semantics."""

from collections.abc import Iterable, Iterator, MutableMapping
from dataclasses import dataclass
from enum import IntEnum
from functools import total_ordering
from typing import BinaryIO, Protocol, TypeVar

from ._wire import WireError, _name_wire, _read_name
from .names import (
    canonical_order,
    check_name,
    encode_idna2003,
    is_absolute_text,
    name_text,
    parse_name,
)


class NameRelation(IntEnum):
    NONE = 0
    SUPERDOMAIN = 1
    SUBDOMAIN = 2
    EQUAL = 3
    COMMONANCESTOR = 4


class IDNACodec(Protocol):
    def encode(self, label: str) -> bytes: ...
    def decode(self, label: bytes) -> str: ...


def _decode_practical(label: bytes) -> str:
    return (
        label[4:].decode("punycode")
        if label.lower().startswith(b"xn--")
        else label.decode("ascii")
    )


@dataclass(frozen=True)
class IDNA2003Codec:
    strict_decode: bool = False

    def encode(self, label: str) -> bytes:
        return encode_idna2003(label)

    def decode(self, label: bytes) -> str:
        if self.strict_decode and label.lower().startswith(b"xn--"):
            return label.lower().decode("idna")
        return _decode_practical(label)


@dataclass(frozen=True)
class IDNA2008Codec:
    uts_46: bool = False
    transitional: bool = False
    allow_pure_ascii: bool = False
    strict_decode: bool = False

    def encode(self, label: str) -> bytes:
        import idna

        if self.allow_pure_ascii and label.isascii():
            return label.encode("ascii")
        if self.uts_46 and self.transitional:
            label = label.translate(
                {
                    ord("ß"): "ss",
                    ord("ẞ"): "ss",
                    ord("ς"): "σ",
                    0x200C: None,
                    0x200D: None,
                }
            )
        return idna.encode(label, strict=True, uts46=self.uts_46)

    def decode(self, label: bytes) -> str:
        if self.strict_decode and label.lower().startswith(b"xn--"):
            import idna

            return idna.decode(label, strict=True, uts46=self.uts_46)
        return _decode_practical(label)


IDNA_2003_Practical = IDNA_2003 = IDNA2003Codec()
IDNA_2003_Strict = IDNA2003Codec(strict_decode=True)
IDNA_2008_Practical = IDNA_2008 = IDNA2008Codec(uts_46=True, allow_pure_ascii=True)
IDNA_2008_Strict = IDNA2008Codec(strict_decode=True)
IDNA_2008_UTS_46 = IDNA2008Codec(uts_46=True)
IDNA_2008_Transitional = IDNA2008Codec(uts_46=True, transitional=True)


@dataclass(frozen=True)
class NameStyle:
    omit_final_dot: bool = False
    idna_codec: IDNACodec | None = None
    origin: "Name | None" = None
    relativize: bool = False


@total_ordering
class Name:
    """An immutable sequence of DNS labels, optionally terminated by the root."""

    __slots__ = ("_labels", "_order")

    def __init__(self, labels: Iterable[bytes | str]):
        normalized = tuple(
            label.encode("ascii") if isinstance(label, str) else bytes(label)
            for label in labels
        )
        absolute = bool(normalized) and normalized[-1] == b""
        values = normalized[:-1] if absolute else normalized
        check_name(values)
        object.__setattr__(self, "_labels", normalized)
        object.__setattr__(self, "_order", (absolute, canonical_order(values)))

    def __setattr__(self, name, value):
        raise AttributeError("DNS names are immutable")

    def __delattr__(self, name):
        raise AttributeError("DNS names are immutable")

    @property
    def labels(self) -> tuple[bytes, ...]:
        return self._labels

    def __iter__(self) -> Iterator[bytes]:
        return iter(self.labels)

    def __len__(self) -> int:
        return len(self.labels)

    def __getitem__(self, position):
        return self.labels[position]

    def __hash__(self) -> int:
        return hash(self._order)

    def __eq__(self, other):
        return (
            self._order == other._order if isinstance(other, Name) else NotImplemented
        )

    def __lt__(self, other):
        return self._order < other._order if isinstance(other, Name) else NotImplemented

    def __str__(self) -> str:
        return self.to_text()

    def __repr__(self) -> str:
        return f"Name({self.to_text()!r})"

    def is_absolute(self) -> bool:
        return self._order[0]

    def is_wild(self) -> bool:
        return self.labels[:1] == (b"*",)

    def canonicalize(self) -> "Name":
        return Name(label.lower() for label in self.labels)

    def to_text(
        self, omit_final_dot: bool = False, style: NameStyle | None = None
    ) -> str:
        if style is not None:
            return self.to_styled_text(style)
        if not self.labels:
            return "@"
        if self.labels == (b"",):
            return "."
        text = name_text(self.labels[:-1] if self.is_absolute() else self.labels)
        return text if self.is_absolute() and not omit_final_dot else text[:-1]

    def to_styled_text(self, style: NameStyle) -> str:
        name = self.choose_relativity(style.origin, style.relativize)
        if style.idna_codec is None:
            return name.to_text(style.omit_final_dot)
        return name.to_unicode(style.omit_final_dot, style.idna_codec)

    def to_unicode(
        self,
        omit_final_dot: bool = False,
        idna_codec: IDNACodec | None = None,
        style: NameStyle | None = None,
        *,
        idna2008: bool = False,
    ) -> str:
        if style is not None:
            return self.to_styled_text(style)
        if len(self.labels) <= 1 and self.labels in ((), (b"",)):
            return self.to_text()
        labels = self.labels[:-1] if self.is_absolute() else self.labels
        codec = idna_codec or (IDNA_2008 if idna2008 else IDNA_2003)
        converted = [
            codec.decode(label)
            if label.lower().startswith(b"xn--")
            else name_text((label,))[:-1]
            for label in labels
        ]
        text = ".".join(converted)
        return text + "." if self.is_absolute() and not omit_final_dot else text

    def fullcompare(self, other: "Name") -> tuple[NameRelation, int, int]:
        order = (self > other) - (self < other)
        if self.is_absolute() != other.is_absolute():
            return NameRelation.NONE, order, 0
        count = 0
        for left, right in zip(reversed(self.labels), reversed(other.labels)):
            if left.lower() != right.lower():
                break
            count += 1
        if count == len(self) == len(other):
            relation = NameRelation.EQUAL
        elif count == len(self):
            relation = NameRelation.SUPERDOMAIN
        elif count == len(other):
            relation = NameRelation.SUBDOMAIN
        else:
            relation = NameRelation.COMMONANCESTOR if count else NameRelation.NONE
        return relation, order, count

    def is_subdomain(self, other: "Name") -> bool:
        return self.fullcompare(other)[0] in (
            NameRelation.EQUAL,
            NameRelation.SUBDOMAIN,
        )

    def is_superdomain(self, other: "Name") -> bool:
        return other.is_subdomain(self)

    def concatenate(self, other: "Name") -> "Name":
        if self.is_absolute() and other.labels:
            raise ValueError("a DNS absolute name cannot be concatenated")
        return Name(self.labels + other.labels)

    def relativize(self, origin: "Name") -> "Name":
        if not self.is_subdomain(origin):
            return self
        return Name(self.labels[: len(self) - len(origin)])

    def derelativize(self, origin: "Name") -> "Name":
        return self if self.is_absolute() else self.concatenate(origin)

    def choose_relativity(
        self, origin: "Name | None" = None, relativize: bool = True
    ) -> "Name":
        if origin is None:
            return self
        return self.relativize(origin) if relativize else self.derelativize(origin)

    def split(self, depth: int) -> tuple["Name", "Name"]:
        if not 0 <= depth <= len(self):
            raise ValueError("invalid DNS name split depth")
        left = len(self) - depth
        return Name(self.labels[:left]), Name(self.labels[left:])

    def parent(self) -> "Name":
        if self in (root, empty):
            raise ValueError("the DNS root and empty name have no parent")
        return Name(self.labels[1:])

    def _adjacent(self, origin: "Name", *, successor: bool, prefix_ok: bool) -> "Name":
        if not origin.is_absolute():
            raise ValueError("DNSSEC ordering requires an absolute zone origin")
        owner = self.derelativize(origin).canonicalize()
        if not owner.is_subdomain(origin):
            raise ValueError("DNS name is outside the ordering zone")
        origin = origin.canonicalize()
        labels = list(owner.labels)

        def available() -> int:
            return 255 - sum(len(label) + 1 for label in labels)

        if successor:
            if prefix_ok and available() >= 2:
                labels.insert(0, b"\x00")
            else:
                while len(labels) > len(origin):
                    label = labels[0]
                    if len(label) < 63 and available() >= 1:
                        labels[0] += b"\x00"
                        break
                    position = next(
                        (i for i in range(len(label) - 1, -1, -1) if label[i] < 255),
                        None,
                    )
                    if position is not None:
                        value = label[position] + 1
                        labels[0] = label[:position] + bytes(
                            (91 if 65 <= value <= 90 else value,)
                        )
                        break
                    del labels[0]
        elif owner != origin and labels[0] == b"\x00":
            del labels[0]
        else:
            if owner != origin:
                last = labels[0][-1]
                if not last:
                    labels[0] = labels[0][:-1]
                else:
                    value = last - 1
                    extension = b"\xff" * min(63 - len(labels[0]), available())
                    labels[0] = (
                        labels[0][:-1]
                        + bytes((64 if 65 <= value <= 90 else value,))
                        + extension
                    )
            if prefix_ok:
                while (space := available()) >= 2:
                    labels.insert(0, b"\xff" * min(63, space - 1))
        result = Name(labels)
        return result if self.is_absolute() else result.relativize(origin)

    def successor(self, origin: "Name", prefix_ok: bool = True) -> "Name":
        """Return the next possible name in canonical zone order (RFC 4471)."""
        return self._adjacent(origin, successor=True, prefix_ok=prefix_ok)

    def predecessor(self, origin: "Name", prefix_ok: bool = True) -> "Name":
        """Return the previous possible name in canonical zone order (RFC 4471)."""
        return self._adjacent(origin, successor=False, prefix_ok=prefix_ok)

    def to_wire(
        self,
        file: BinaryIO | None = None,
        compress: dict["Name", int] | None = None,
        origin: "Name | None" = None,
        canonicalize: bool = False,
    ) -> bytes | None:
        name = self.choose_relativity(origin, False)
        if not name.is_absolute():
            raise ValueError("a DNS name requires an origin for wire encoding")
        labels = name.labels[:-1]
        if canonicalize:
            labels = tuple(label.lower() for label in labels)
        if file is None:
            return _name_wire(labels)
        if compress is None or canonicalize:
            file.write(_name_wire(labels))
            return None
        for offset, label in enumerate(labels):
            suffix = Name(name.labels[offset:])
            pointer = compress.get(suffix)
            if pointer is not None and 0 <= pointer < min(file.tell(), 0x4000):
                file.write((0xC000 | pointer).to_bytes(2, "big"))
                return None
            if file.tell() < 0x4000:
                compress[suffix] = file.tell()
            file.write(bytes((len(label),)) + label)
        file.write(b"\0")
        return None

    def to_digestable(self, origin: "Name | None" = None) -> bytes:
        return self.to_wire(origin=origin, canonicalize=True)


root = Name((b"",))
empty = Name(())


def from_text(
    text: str | bytes,
    origin: Name | None = root,
    idna_codec: IDNACodec | None = None,
    *,
    idna2008: bool = False,
) -> Name:
    if isinstance(text, bytes):
        text = text.decode("ascii")
    if text in ("@", ""):
        return empty if origin is None else origin
    codec = idna_codec or (IDNA_2008 if idna2008 else IDNA_2003)
    values = parse_name(text, encode_label=codec.encode)
    if is_absolute_text(text):
        return Name((*values, b""))
    return Name(values) if origin is None else Name(values).concatenate(origin)


def from_wire(packet: bytes, current: int = 0) -> tuple[Name, int]:
    if not 0 <= current < len(packet):
        raise WireError("DNS name offset outside message")
    labels, end = _read_name(packet, current, canonical=False, pointer_floor=0)
    return Name((*labels, b"")), end - current


class _NameReader(Protocol):
    def get_name(self) -> Name: ...


def from_wire_parser(parser: _NameReader) -> Name:
    return parser.get_name()


def from_unicode(
    text: str, origin: Name | None = root, idna_codec: IDNACodec | None = None
) -> Name:
    return from_text(text, origin, idna_codec or IDNA_2008)


_Value = TypeVar("_Value")


class NameDict(MutableMapping[Name, _Value]):
    """Map case-insensitive DNS names with longest-ancestor lookup."""

    def __init__(self, values=(), /):
        self._data: dict[Name, _Value] = {}
        self.update(values)

    def __getitem__(self, name: Name) -> _Value:
        return self._data[name]

    def __setitem__(self, name: Name, value: _Value) -> None:
        if not isinstance(name, Name):
            raise TypeError("NameDict keys must be DNS names")
        self._data[name] = value

    def __delitem__(self, name: Name) -> None:
        del self._data[name]

    def __iter__(self) -> Iterator[Name]:
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    @property
    def max_depth(self) -> int:
        return max(map(len, self._data), default=0)

    @property
    def max_depth_items(self) -> int:
        depth = self.max_depth
        return sum(len(name) == depth for name in self._data)

    def get_deepest_match(self, name: Name) -> tuple[Name, _Value]:
        last = len(name) if name.is_absolute() else len(name) + 1
        for offset in range(last):
            candidate = Name(name.labels[offset:])
            if candidate in self._data:
                return candidate, self._data[candidate]
        if empty in self._data:
            return empty, self._data[empty]
        raise KeyError(name)
