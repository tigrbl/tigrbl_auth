"""TTL-aware set operations for collections of homogeneous DNS RDATA."""

from collections.abc import Iterable, Iterator, MutableSet

from .rdata import Rdata, from_record, is_registered_singleton
from .rdata import from_text as parse_rdata
from .wire import ResourceRecord, class_text, record_class, record_type, type_text


class Rdataset(MutableSet[Rdata]):
    """An ordered DNS record set with a shared TTL and covered type."""

    def __init__(
        self,
        rdclass: int | str,
        rdtype: int | str,
        covers: int | str = 0,
        ttl: int = 0,
        values: Iterable[Rdata] = (),
    ) -> None:
        self.rdclass = record_class(rdclass)
        self.rdtype = record_type(rdtype)
        self.covers = record_type(covers)
        self.ttl = self._ttl(ttl)
        self._values: dict[Rdata, None] = {}
        for item in values:
            self.add(item)

    @staticmethod
    def _ttl(value: int) -> int:
        if not isinstance(value, int) or not 0 <= value <= 0xFFFFFFFF:
            raise ValueError("DNS TTL is outside its wire range")
        return value

    def __iter__(self) -> Iterator[Rdata]:
        return iter(self._values)

    def __contains__(self, value) -> bool:
        return value in self._values

    def __len__(self) -> int:
        return len(self._values)

    def __getitem__(self, index):
        return tuple(self._values)[index]

    def add(self, value: Rdata, ttl: int | None = None) -> None:
        if (value.rdclass, value.rdtype, value.covers()) != (
            self.rdclass,
            self.rdtype,
            self.covers,
        ):
            raise ValueError(
                "RDATA class, type, or covered type does not match the DNS dataset"
            )
        if ttl is not None:
            ttl = self._ttl(ttl)
            self.ttl = min(self.ttl, ttl) if self._values else ttl
        if (
            self._values
            and value not in self._values
            and is_registered_singleton(self.rdtype)
        ):
            self._values.clear()
        self._values[value] = None

    def discard(self, value: Rdata) -> None:
        self._values.pop(value, None)

    def update_ttl(self, ttl: int) -> None:
        ttl = self._ttl(ttl)
        self.ttl = min(self.ttl, ttl) if self._values else ttl

    def copy(self) -> "Rdataset":
        return Rdataset(self.rdclass, self.rdtype, self.covers, self.ttl, self)

    def _from_iterable(self, values):
        return Rdataset(self.rdclass, self.rdtype, self.covers, self.ttl, values)

    def update(self, other: Iterable[Rdata]) -> None:
        if isinstance(other, Rdataset):
            if not self.match(other.rdclass, other.rdtype, other.covers):
                raise ValueError(
                    "DNS datasets have different class, type, or covered type"
                )
            for item in other:
                self.add(item, ttl=other.ttl)
            return
        for item in other:
            self.add(item)

    def union(self, other: Iterable[Rdata]) -> "Rdataset":
        merged = self.copy()
        merged.update(other)
        return merged

    __or__ = union

    def __ior__(self, other: Iterable[Rdata]) -> "Rdataset":
        self.update(other)
        return self

    def intersection(self, other: Iterable[Rdata]) -> "Rdataset":
        return self & other

    def difference(self, other: Iterable[Rdata]) -> "Rdataset":
        return self - other

    def match(
        self, rdclass: int | str, rdtype: int | str, covers: int | str = 0
    ) -> bool:
        return (self.rdclass, self.rdtype, self.covers) == (
            record_class(rdclass),
            record_type(rdtype),
            record_type(covers),
        )

    def records(self, owner: tuple[bytes, ...]) -> tuple[ResourceRecord, ...]:
        return tuple(value.record(owner, self.ttl) for value in self)

    def to_text(self) -> str:
        stem = f"{self.ttl} {class_text(self.rdclass)} {type_text(self.rdtype)}"
        return "\n".join(f"{stem} {value.to_text()}".rstrip() for value in self)


def from_rdata(ttl: int, *values: Rdata) -> Rdataset:
    if not values:
        raise ValueError("at least one DNS RDATA value is required")
    first = values[0]
    return Rdataset(first.rdclass, first.rdtype, first.covers(), ttl, values)


def from_text(
    rdclass: int | str, rdtype: int | str, ttl: int, *text: str, origin=None
) -> Rdataset:
    if not text:
        return Rdataset(rdclass, rdtype, ttl=ttl)
    return from_rdata(
        ttl, *(parse_rdata(rdclass, rdtype, value, origin) for value in text)
    )


def from_records(records: Iterable[ResourceRecord]) -> Rdataset:
    items = tuple(records)
    if not items:
        raise ValueError("at least one DNS resource record is required")
    return from_rdata(min(rr.ttl for rr in items), *(from_record(rr) for rr in items))
