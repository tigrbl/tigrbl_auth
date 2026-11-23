"""Construct immutable owner-qualified DNS RRsets."""

from dataclasses import dataclass, field

from tba_primitives_dns_name.name import Name
from tba_primitives_dns_name.name import from_text as parse_name
from tba_primitives_dns_name.names import Name as Labels

from .rdata import Rdata, decoded, from_record, record_text
from .rdataset import Rdataset, from_records
from .rdataset import from_rdata as make_dataset
from .rdataset import from_text as parse_dataset
from .wire import RecordType, ResourceRecord


@dataclass(frozen=True)
class RRset:
    owner: Labels
    rdclass: int
    type: int
    ttl: int
    records: tuple[ResourceRecord, ...]
    origin: Name | None = field(default=None, repr=False, compare=False)

    @property
    def name(self) -> Name:
        name = Name((*self.owner, b""))
        return name if self.origin is None else name.relativize(self.origin)

    @property
    def rdtype(self) -> int:
        return self.type

    @property
    def covers(self) -> int:
        if self.records and self.type in (RecordType.SIG, RecordType.RRSIG):
            return decoded(self.records[0])[0]
        return 0

    def to_rdataset(self) -> Rdataset:
        return (
            from_records(self.records)
            if self.records
            else Rdataset(self.rdclass, self.type, ttl=self.ttl)
        )

    def to_text(self) -> str:
        return "\n".join(record_text(record) for record in self.records)

    def __len__(self) -> int:
        return len(self.records)

    def __iter__(self):
        return iter(self.to_rdataset())

    def __getitem__(self, index):
        if isinstance(index, slice):
            return tuple(from_record(rr) for rr in self.records[index])
        return from_record(self.records[index])


def from_rdataset(name: Name | str, dataset: Rdataset) -> RRset:
    owner = parse_name(name) if isinstance(name, str) else name
    if not owner.is_absolute():
        raise ValueError("RRset owner needs an absolute DNS name")
    labels = owner.labels[:-1]
    return RRset(
        labels, dataset.rdclass, dataset.rdtype, dataset.ttl, dataset.records(labels)
    )


def from_rdata(name: Name | str, ttl: int, *values: Rdata) -> RRset:
    return from_rdataset(name, make_dataset(ttl, *values))


def from_text(
    name: Name | str,
    ttl: int,
    rdclass: int | str,
    rdtype: int | str,
    *text: str,
    origin=None,
) -> RRset:
    if isinstance(origin, str):
        origin = parse_name(origin)
    owner = (
        parse_name(name)
        if isinstance(name, str) and origin is None
        else (parse_name(name, origin=origin) if isinstance(name, str) else name)
    )
    return from_rdataset(
        owner, parse_dataset(rdclass, rdtype, ttl, *text, origin=origin)
    )
