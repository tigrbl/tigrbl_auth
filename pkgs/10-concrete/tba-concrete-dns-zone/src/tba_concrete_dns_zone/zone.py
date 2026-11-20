"""DNS master files, RRsets, and atomic zone transactions."""

import re
from collections.abc import Callable, Iterable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from threading import RLock
from types import MappingProxyType

from tba_codec_dns.node import Node
from tba_codec_dns.rdata import (
    Rdata,
    decoded,
    from_tokens,
    parse_ttl,
    record_text,
)
from tba_codec_dns.rdata import (
    from_record as from_record,
)
from tba_codec_dns.rdataset import Rdataset
from tba_codec_dns.rdataset import from_records as from_records
from tba_codec_dns.rrset import RRset
from tba_codec_dns.tokenizer import master_tokens
from tba_codec_dns.wire import (
    RecordClass,
    RecordType,
    ResourceRecord,
    record_class,
    record_type,
)
from tba_primitives_dns_name.name import Name as DomainName
from tba_primitives_dns_name.name import empty
from tba_primitives_dns_name.names import (
    Name,
    canonical_order,
    is_subdomain,
    parse_name,
)

from ._btree import ZoneIndex
from ._immutable import ImmutableRdataset
from ._immutable import ImmutableVersionedNode as ImmutableVersionedNode
from ._immutable import VersionedNode as VersionedNode

_Key = tuple[Name, int, int | None]
_Index = dict[_Key, dict[bytes, ResourceRecord]] | ZoneIndex


class AlreadyEnded(RuntimeError):
    """A completed DNS zone transaction was used again."""


class UseTransaction(RuntimeError):
    """The versioned zone can only be edited through a writer."""


class ReadOnly(RuntimeError):
    """A write was attempted through a DNS zone reader."""


class DeleteNotExact(ValueError):
    """Some of the requested records are absent from the DNS zone."""


class NoSOA(ValueError):
    """The zone does not have exactly one apex SOA."""


class NoNS(ValueError):
    """The zone does not have an apex NS set."""


def _owner_keys(data: _Index, owner: Name) -> Iterator[_Key]:
    if isinstance(data, ZoneIndex):
        for key in data.from_key((owner, 0, None)):
            if key[0] != owner:
                return
            yield key
    else:
        yield from (key for key in data if key[0] == owner)


def _key(record: ResourceRecord) -> _Key:
    covered = (
        decoded(record)[0]
        if record.type in (RecordType.RRSIG, RecordType.SIG)
        else None
    )
    return tuple(label.lower() for label in record.name), record.type, covered


class ZoneTransaction:
    def __init__(
        self, zone: "Zone", data: _Index, revision: int, *, read_only: bool = False
    ) -> None:
        self._zone = zone
        self._data = data
        self._revision = revision
        self._read_only = read_only
        self._closed = False
        self._changed = False
        self._put_checks = []
        self._delete_dataset_checks = []
        self._delete_name_checks = []
        self._checking = False

    def _ensure_open(self, *, write: bool = False) -> None:
        if self._closed:
            raise AlreadyEnded("DNS zone transaction is closed")
        if write and self._read_only:
            raise ReadOnly("DNS zone transaction is read-only")
        if write and self._checking:
            raise RuntimeError("DNS transaction checks may only read")

    def check_put_rdataset(self, check) -> None:
        self._ensure_open(write=True)
        self._put_checks.append(check)

    def check_delete_rdataset(self, check) -> None:
        self._ensure_open(write=True)
        self._delete_dataset_checks.append(check)

    def check_delete_name(self, check) -> None:
        self._ensure_open(write=True)
        self._delete_name_checks.append(check)

    def _check(self, callbacks, owner, *args) -> None:
        if callbacks:
            self._checking = True
            try:
                name = self._zone._display(owner)
                for check in callbacks:
                    check(self, name, *args)
            finally:
                self._checking = False

    @contextmanager
    def _checked_edit(self):
        if not (
            self._put_checks or self._delete_dataset_checks or self._delete_name_checks
        ):
            yield
            return
        before, changed = self._data.copy(), self._changed
        try:
            yield
        except BaseException:
            self._data, self._changed = before, changed
            raise

    def commit(self) -> None:
        self._ensure_open()
        if self._checking:
            raise RuntimeError("DNS transaction checks may only read")
        try:
            if not self._read_only:
                with self._zone._lock:
                    if self._zone._revision != self._revision:
                        raise RuntimeError("DNS zone changed during transaction")
                    previous = self._zone._data
                    self._zone._data = self._data
                    self._zone._revision += 1
                    try:
                        self._zone._committed()
                    except BaseException:
                        self._zone._data = previous
                        self._zone._revision -= 1
                        raise
        finally:
            self._closed = True

    def rollback(self) -> None:
        self._ensure_open()
        if self._checking:
            raise RuntimeError("DNS transaction checks may only read")
        self._closed = True

    def changed(self) -> bool:
        self._ensure_open()
        return self._changed

    def get(
        self, name: str | Name | DomainName, rdtype: int | str, covers: int | str = 0
    ) -> Rdataset | None:
        self._ensure_open()
        key = (
            self._zone._owner(name),
            record_type(rdtype),
            record_type(covers) or None,
        )
        records = self._data.get(key)
        if records is None:
            return None
        dataset = self._zone._rrset(key, records).to_rdataset()
        return ImmutableRdataset(dataset) if self._read_only else dataset

    def name_exists(self, name: str | Name | DomainName) -> bool:
        self._ensure_open()
        owner = self._zone._owner(name)
        return next(_owner_keys(self._data, owner), None) is not None

    def get_node(self, name: str | Name | DomainName) -> Node | None:
        self._ensure_open()
        node = self._zone._node_at(self._data, self._zone._owner(name))
        if not self._read_only or node is None:
            return node
        return self._zone._immutable_node(node)

    def check_origin(self) -> None:
        soa = self.get(self._zone.origin, RecordType.SOA)
        if soa is None or len(soa) != 1:
            raise NoSOA("DNS zone requires exactly one apex SOA")
        if self.get(self._zone.origin, RecordType.NS) is None:
            raise NoNS("DNS zone requires an apex NS RRset")

    def iterate_names(self) -> Iterator[DomainName]:
        self._ensure_open()
        return iter(
            self._zone._display(owner)
            for owner in sorted({key[0] for key in self._data}, key=canonical_order)
        )

    def iterate_rdatasets(self) -> Iterator[tuple[DomainName, Rdataset]]:
        self._ensure_open()
        for key, records in self._data.items():
            rrset = self._zone._rrset(key, records)
            yield self._zone._display(key[0]), rrset.to_rdataset()

    def _datasets(self, name, arguments: tuple) -> tuple[Name, tuple[Rdataset, ...]]:
        if isinstance(name, RRset):
            if arguments:
                raise TypeError("an RRset supplies its own owner and dataset")
            return self._zone._owner(name.owner), (name.to_rdataset(),)
        owner = self._zone._owner(name)
        if not arguments:
            raise TypeError("DNS transaction needs a dataset or TTL and RDATA")
        if isinstance(arguments[0], int):
            ttl, *records = arguments
            datasets: dict[tuple[int, int, int], Rdataset] = {}
            if not records or not all(isinstance(rr, Rdata) for rr in records):
                raise TypeError("DNS TTL must be followed by RDATA values")
            for rr in records:
                key = rr.rdclass, rr.rdtype, rr.covers()
                if key not in datasets:
                    datasets[key] = Rdataset(*key, ttl=ttl)
                datasets[key].add(rr)
            return owner, tuple(datasets.values())
        if not all(isinstance(dataset, Rdataset) for dataset in arguments):
            raise TypeError("DNS transaction arguments must be datasets")
        return owner, arguments

    def _put(self, name, arguments: tuple, *, replace: bool) -> None:
        self._ensure_open(write=True)
        owner, datasets = self._datasets(name, arguments)
        if not is_subdomain(owner, self._zone.origin) or any(
            dataset.rdclass != self._zone.rdclass for dataset in datasets
        ):
            raise ValueError("DNS dataset is outside zone name or class")
        prepared = tuple(
            (dataset, tuple(self._record_entry(rr) for rr in dataset.records(owner)))
            for dataset in datasets
        )
        with self._checked_edit():
            for dataset, entries in prepared:
                key = (owner, dataset.rdtype, dataset.covers or None)
                records = {} if replace else self._data.get(key, {}).copy()
                records.update((value, rr) for _, value, rr in entries)
                self._set_records(key, records)

    def replace(self, name, dataset=None, *values) -> None:
        arguments = () if dataset is None and not values else (dataset, *values)
        self._put(name, arguments, replace=True)

    def add(self, record, *values) -> None:
        if isinstance(record, ResourceRecord) and not values:
            self._ensure_open(write=True)
            self._add_record(record)
        else:
            self._put(record, values, replace=False)

    def _add_record(self, record: ResourceRecord) -> None:
        if record.rdclass != self._zone.rdclass or not is_subdomain(
            record.name, self._zone.origin
        ):
            raise ValueError("DNS record is outside zone name or class")
        self._store_record(*self._record_entry(record))

    @staticmethod
    def _record_entry(record: ResourceRecord) -> tuple[_Key, bytes, ResourceRecord]:
        normalized = ResourceRecord(
            record.name,
            record.type,
            record.rdclass,
            record.ttl,
            record.uncompressed_data(),
        )
        return _key(record), record.uncompressed_data(canonical=True), normalized

    def _store_record(
        self, key: _Key, value: bytes, normalized: ResourceRecord
    ) -> None:
        records = self._data.get(key, {})
        self._set_records(key, {**records, value: normalized})

    def _set_records(self, key: _Key, records: dict[bytes, ResourceRecord]) -> None:
        if records == self._data.get(key, {}):
            return
        if records:
            if self._put_checks:
                self._check(
                    self._put_checks,
                    key[0],
                    self._zone._rrset(key, records).to_rdataset(),
                )
            self._data[key] = records
        else:
            self._check(self._delete_dataset_checks, key[0], key[1], key[2] or 0)
            del self._data[key]
        self._changed = True

    def delete(
        self,
        owner: str | Name | DomainName,
        rdtype=None,
        *values,
        covers=None,
    ) -> None:
        self._delete(owner, rdtype, values, covers, exact=False)

    def delete_exact(self, name, rdtype=None, *values, covers=None) -> None:
        """Delete an entire owner, dataset, or the exact requested RDATA subset."""
        self._delete(name, rdtype, values, covers, exact=True)

    def _delete(self, name, rdtype, values, covers, *, exact: bool):
        self._ensure_open(write=True)
        if isinstance(name, RRset) or isinstance(rdtype, (Rdata, Rdataset)):
            if isinstance(name, RRset):
                if rdtype is not None or covers is not None or values:
                    raise TypeError("an RRset supplies its own owner and data")
                records = name.records
            else:
                owner = self._zone._owner(name)
                if covers is not None:
                    raise TypeError("covered type is implicit when deleting RDATA")
                records = []
                for value in (rdtype, *values):
                    if isinstance(value, Rdata):
                        records.append(value.record(owner, 0))
                    elif isinstance(value, Rdataset):
                        records.extend(value.records(owner))
                    else:
                        raise TypeError("DNS deletion values must be RDATA or datasets")
            if exact and any(
                record.rdclass != self._zone.rdclass
                or record.uncompressed_data(canonical=True)
                not in self._data.get(_key(record), {})
                for record in records
            ):
                raise DeleteNotExact("DNS zone does not contain every requested record")
            replacements = {}
            for record in records:
                if record.rdclass == self._zone.rdclass:
                    key = _key(record)
                    if key not in replacements:
                        replacements[key] = self._data.get(key, {}).copy()
                    replacements[key].pop(
                        record.uncompressed_data(canonical=True), None
                    )
            with self._checked_edit():
                for key, dataset in replacements.items():
                    self._set_records(key, dataset)
            return
        if values:
            if len(values) != 1 or covers is not None:
                raise TypeError("DNS dataset deletion accepts one covered type")
            covers = values[0]
        selected = self._zone._owner(name)
        kind = None if rdtype is None else record_type(rdtype)
        covered = None if covers is None else record_type(covers)
        keys = tuple(
            key
            for key in _owner_keys(self._data, selected)
            if (kind is None or key[1] == kind)
            and (covered is None or (key[2] or 0) == covered)
        )
        if exact and not keys:
            raise DeleteNotExact("DNS zone owner or dataset is absent")
        if not keys:
            return
        if kind is None:
            self._check(self._delete_name_checks, selected)
            for key in keys:
                del self._data[key]
            self._changed = True
        else:
            with self._checked_edit():
                for key in keys:
                    self._set_records(key, {})

    def update_serial(
        self, value: int = 1, relative: bool = True, name: str | Name | DomainName = "@"
    ) -> None:
        self._ensure_open(write=True)
        if not isinstance(value, int) or not 0 <= value <= 0xFFFFFFFF:
            raise ValueError("DNS serial is outside its wire range")
        origin = self._zone._owner(name)
        soa = self.get(origin, RecordType.SOA)
        if soa is None or len(soa) != 1:
            raise NoSOA("DNS zone requires exactly one apex SOA")
        serial = (soa[0].serial + value) & 0xFFFFFFFF if relative else value
        if serial != soa[0].serial:
            self.replace(
                origin,
                Rdataset(
                    soa.rdclass,
                    soa.rdtype,
                    ttl=soa.ttl,
                    values=(soa[0].replace(serial=serial),),
                ),
            )

    def delete_record(self, record: ResourceRecord) -> None:
        self._ensure_open(write=True)
        if record.rdclass != self._zone.rdclass:
            return
        key = _key(record)
        records = self._data.get(key)
        if not records:
            return
        value = record.uncompressed_data(canonical=True)
        if value not in records:
            return
        updated = records.copy()
        del updated[value]
        self._set_records(key, updated)


class Zone:
    """An in-memory zone with immutable RRsets and optimistic transactions."""

    writable_version_factory = ZoneTransaction
    node_factory = Node

    def __init__(
        self,
        origin: str | Name | DomainName,
        records: Iterable[ResourceRecord] = (),
        *,
        rdclass: int | str = RecordClass.IN,
        relativize: bool = False,
    ) -> None:
        self.origin = _origin_labels(origin)
        self.rdclass = record_class(rdclass)
        self.relativize = relativize
        self._data = self._new_index()
        self._revision = 0
        self._lock = RLock()
        with self.transaction() as change:
            for record in records:
                change.add(record)

    @contextmanager
    def transaction(self, *, replacement: bool = False) -> Iterator[ZoneTransaction]:
        with self._lock:
            baseline = self._revision
            data = self._new_index() if replacement else self._data.copy()
            replacing_data = replacement and bool(self._data)
        change = self.writable_version_factory(self, data, baseline)
        change._changed = replacing_data
        try:
            yield change
            if not change._closed:
                change.commit()
        finally:
            if not change._closed:
                change.rollback()

    def writer(self, replacement: bool = False):
        return self.transaction(replacement=replacement)

    def _new_index(self) -> _Index:
        return {}

    @contextmanager
    def reader(self) -> Iterator[ZoneTransaction]:
        with self._lock:
            snapshot = ZoneTransaction(self, self._data, self._revision, read_only=True)
        with self._read_transaction(snapshot) as reader:
            yield reader

    @staticmethod
    @contextmanager
    def _read_transaction(snapshot: ZoneTransaction) -> Iterator[ZoneTransaction]:
        try:
            yield snapshot
        finally:
            if not snapshot._closed:
                snapshot.rollback()

    def _immutable_node(self, node: Node) -> ImmutableVersionedNode:
        return ImmutableVersionedNode(node.rdatasets)

    def _committed(self) -> None:
        """Observe changes while holding the zone lock."""

    @staticmethod
    def _rrset(key: _Key, records: dict[bytes, ResourceRecord]) -> RRset:
        first = next(iter(records.values()))
        ttl = min(record.ttl for record in records.values())
        normalized = tuple(
            ResourceRecord(record.name, record.type, record.rdclass, ttl, record.data)
            for record in records.values()
        )
        return RRset(key[0], first.rdclass, key[1], ttl, normalized)

    def get(
        self,
        name: str | Name | DomainName,
        rdtype: int | str,
        *,
        covers: int | None = None,
    ) -> RRset | None:
        owner = self._owner(name)
        key = (owner, record_type(rdtype), covers)
        with self._lock:
            records = self._data.get(key)
            return None if records is None else self._rrset(key, records)

    def _owner(self, name: str | Name | DomainName) -> Name:
        if isinstance(name, str):
            return parse_name(name, self.origin, canonical=True)
        if isinstance(name, DomainName):
            labels = name.derelativize(DomainName((*self.origin, b""))).labels[:-1]
        else:
            labels = name
        return tuple(label.lower() for label in labels)

    def _display(self, owner: Name) -> DomainName:
        absolute = DomainName((*owner, b""))
        return (
            absolute.relativize(DomainName((*self.origin, b"")))
            if self.relativize
            else absolute
        )

    def find_node(self, name: str | Name | DomainName) -> Node:
        owner = self._owner(name)
        with self._lock:
            node = self._node_at(self._data, owner)
        if node is None:
            raise KeyError(name)
        return node

    def _node_at(self, data: _Index, owner: Name) -> Node | None:
        datasets = self._datasets_at(data, owner)
        return self.node_factory(datasets) if datasets else None

    def _datasets_at(self, data: _Index, owner: Name) -> tuple[Rdataset, ...]:
        return tuple(
            self._rrset(key, data[key]).to_rdataset()
            for key in _owner_keys(data, owner)
        )

    def get_node(self, name: str | Name | DomainName) -> Node | None:
        try:
            return self.find_node(name)
        except KeyError:
            return None

    def __getitem__(self, name: str | Name | DomainName) -> Node:
        return self.find_node(name)

    def __iter__(self) -> Iterator[DomainName]:
        with self._lock:
            names = sorted({key[0] for key in self._data}, key=canonical_order)
            return iter(self._display(name) for name in names)

    def __len__(self) -> int:
        with self._lock:
            return len({key[0] for key in self._data})

    def get_rdataset(
        self, name: str | Name | DomainName, rdtype: int | str, covers: int | str = 0
    ) -> Rdataset | None:
        owner = self._owner(name)
        rrset = self.get(owner, rdtype, covers=record_type(covers) or None)
        return None if rrset is None else rrset.to_rdataset()

    def get_rrset(
        self, name: str | Name | DomainName, rdtype: int | str, covers: int | str = 0
    ) -> RRset | None:
        return self.get(name, rdtype, covers=record_type(covers) or None)

    def find_rrset(
        self, name: str | Name | DomainName, rdtype: int | str, covers: int | str = 0
    ) -> RRset:
        rrset = self.get_rrset(name, rdtype, covers)
        if rrset is None:
            raise KeyError((name, rdtype, covers))
        return rrset

    def get_soa(self):
        soa = self.get_rdataset(self.origin, RecordType.SOA)
        if soa is None or len(soa) != 1:
            raise NoSOA("DNS zone requires exactly one apex SOA")
        return soa[0]

    def get_class(self) -> int:
        return self.rdclass

    def origin_information(self) -> tuple[DomainName, bool, DomainName]:
        absolute = DomainName((*self.origin, b""))
        return absolute, self.relativize, empty if self.relativize else absolute

    def from_wire_origin(self) -> DomainName | None:
        absolute, relativize, _ = self.origin_information()
        return absolute if relativize else None

    def delete_node(self, name: str | Name | DomainName) -> None:
        with self.writer() as change:
            change.delete(name)

    def find_rdataset(
        self, name: str | Name | DomainName, rdtype: int | str, covers: int | str = 0
    ) -> Rdataset:
        dataset = self.get_rdataset(name, rdtype, covers)
        if dataset is None:
            raise KeyError((name, rdtype, covers))
        return dataset

    def replace_rdataset(
        self, name: str | Name | DomainName, dataset: Rdataset
    ) -> None:
        with self.transaction() as change:
            change.replace(name, dataset)

    def delete_rdataset(
        self, name: str | Name | DomainName, rdtype: int | str, covers: int | str = 0
    ) -> None:
        with self.transaction() as change:
            change.delete(self._owner(name), rdtype, covers=record_type(covers) or None)

    def iterate_rdatasets(
        self, rdtype: int | str = RecordType.ANY, covers: int | str = 0
    ):
        kind, covered = record_type(rdtype), record_type(covers)
        for rrset in self.rrsets():
            if kind in (RecordType.ANY, rrset.type) and (
                not covered or rrset.covers == covered
            ):
                yield self._display(rrset.owner), rrset.to_rdataset()

    def iterate_rdatas(self, rdtype: int | str = RecordType.ANY, covers: int | str = 0):
        for owner, dataset in self.iterate_rdatasets(rdtype, covers):
            for value in dataset:
                yield owner, dataset.ttl, value

    def rrsets(self) -> tuple[RRset, ...]:
        with self._lock:
            keys = sorted(
                self._data,
                key=lambda key: (canonical_order(key[0]), key[1], key[2] or 0),
            )
            return tuple(self._rrset(key, self._data[key]) for key in keys)

    def records(self) -> Iterator[ResourceRecord]:
        for rrset in self.rrsets():
            yield from rrset.records

    def check_origin(self) -> None:
        with self.reader() as snapshot:
            snapshot.check_origin()

    def to_text(self) -> str:
        return "".join(record_text(record) + "\n" for record in self.records())

    def to_file(self, path: str | Path) -> None:
        Path(path).write_text(self.to_text(), encoding="utf-8")

    @classmethod
    def from_file(
        cls,
        path: str | Path,
        origin: str | DomainName | None = None,
        *,
        rdclass: int | str = RecordClass.IN,
        allow_include: bool = False,
        check_origin: bool = True,
        rfc2308_ttl: bool = True,
        relativize: bool | None = None,
    ) -> "Zone":
        source = path if hasattr(path, "read") else None
        loader = None
        if allow_include:
            filename = getattr(source, "name", path)
            base = Path(filename).resolve().parent

            def load_include(name: str) -> str:
                include = (base / name).resolve()
                if not include.is_relative_to(base):
                    raise ValueError("$INCLUDE is outside the DNS zone directory")
                return include.read_text(encoding="utf-8")

            loader = load_include
        text = (
            source.read()
            if source is not None
            else Path(path).read_text(encoding="utf-8")
        )
        return cls.from_text(
            text.decode("utf-8") if isinstance(text, bytes) else text,
            origin,
            rdclass=rdclass,
            include=loader,
            check_origin=check_origin,
            rfc2308_ttl=rfc2308_ttl,
            relativize=relativize,
        )

    @classmethod
    def from_text(
        cls,
        text: str,
        origin: str | DomainName | None = None,
        *,
        rdclass: int | str = RecordClass.IN,
        include: Callable[[str], str] | None = None,
        check_origin: bool = True,
        rfc2308_ttl: bool = True,
        relativize: bool | None = None,
    ) -> "Zone":
        root = None if origin is None else _origin_labels(origin)
        reader = _MasterReader(root, record_class(rdclass), include, rfc2308_ttl)
        records = tuple(reader.read(text, root))
        if reader.root is None:
            raise ValueError("DNS zone origin was not provided")
        options = {} if relativize is None else {"relativize": relativize}
        zone = cls(
            reader.root,
            (record for record in records if is_subdomain(record.name, reader.root)),
            rdclass=rdclass,
            **options,
        )
        if check_origin:
            zone.check_origin()
        return zone


def _origin_labels(origin: str | Name | DomainName) -> Name:
    if isinstance(origin, str):
        return parse_name(origin, canonical=True)
    if isinstance(origin, DomainName):
        if not origin.is_absolute():
            raise ValueError("zone origin must be absolute")
        origin = origin.labels[:-1]
    return tuple(label.lower() for label in origin)


def from_text(text: str, origin=None, *, zone_factory=Zone, **kwargs) -> Zone:
    return zone_factory.from_text(text, origin, **kwargs)


def from_file(source, origin=None, *, zone_factory=Zone, **kwargs) -> Zone:
    return zone_factory.from_file(source, origin, **kwargs)


_GENERATE_RANGE = re.compile(r"([0-9]+)-([0-9]+)(?:/([0-9]+))?")
_GENERATE_TOKEN = re.compile(r"\\.|\$(?:\{([^{}]+)\})?")


def _expand(template: str, number: int) -> str:
    def substitute(match: re.Match[str]) -> str:
        if match[0].startswith("\\"):
            return match[0]
        if match[1] is None:
            return str(number)
        fields = match[1].split(",")
        if len(fields) > 3:
            raise ValueError("invalid $GENERATE substitution")
        offset, width, radix = (fields + ["", "", ""])[:3]
        value = number + int(offset or "0")
        digits = int(width or "0")
        if (
            value < 0
            or not 0 <= digits <= 255
            or radix not in ("", "d", "o", "x", "X", "n", "N")
        ):
            raise ValueError("invalid $GENERATE offset, width, or base")
        if radix in ("n", "N"):
            formatted = format(value, radix.lower().replace("n", "x")).zfill(digits)
            return ".".join(reversed(formatted.upper() if radix == "N" else formatted))
        return format(value, radix or "d").zfill(digits)

    return _GENERATE_TOKEN.sub(substitute, template)


class _MasterReader:
    def __init__(
        self,
        root: Name | None,
        rdclass: int,
        include: Callable[[str], str] | None,
        rfc2308_ttl: bool,
    ):
        self.root = root
        self.rdclass = rdclass
        self.include = include
        self.default_ttl: int | None = None
        self.last_ttl: int | None = None
        self.soa_minimum: int | None = None
        self.rfc2308_ttl = rfc2308_ttl

    def read(
        self, text: str, origin: Name | None, depth: int = 0, owner: Name | None = None
    ) -> Iterator[ResourceRecord]:
        for lineno, omitted, tokens in master_tokens(text):
            try:
                directive, args = tokens[0].upper(), tokens[1:]
                if directive == "$ORIGIN" and len(args) == 1:
                    origin = parse_name(args[0], origin or (), canonical=True)
                    if self.root is None:
                        self.root = origin
                    continue
                if directive == "$TTL" and len(args) == 1:
                    self.default_ttl = parse_ttl(args[0])
                    continue
                if origin is None:
                    raise ValueError("DNS zone origin is unknown")
                if directive == "$INCLUDE" and len(args) in (1, 2):
                    if self.include is None or depth >= 16:
                        raise ValueError(
                            "$INCLUDE is disabled or exceeds nesting limit"
                        )
                    include_name = args[0].strip('"')
                    subtree = origin if len(args) == 1 else parse_name(args[1], origin)
                    previous = self.default_ttl, self.last_ttl, self.soa_minimum
                    try:
                        yield from self.read(
                            self.include(include_name), subtree, depth + 1, owner
                        )
                    finally:
                        self.default_ttl, self.last_ttl, self.soa_minimum = previous
                    continue
                if directive == "$GENERATE" and len(args) >= 3:
                    span = _GENERATE_RANGE.fullmatch(args[0])
                    if span is None:
                        raise ValueError("invalid $GENERATE range")
                    first, last, step = int(span[1]), int(span[2]), int(span[3] or "1")
                    if first > last or step <= 0 or (last - first) // step >= 100000:
                        raise ValueError("invalid or excessive $GENERATE range")
                    for number in range(first, last + 1, step):
                        expanded = tuple(_expand(token, number) for token in args[1:])
                        owner = parse_name(expanded[0], origin)
                        yield self._record(owner, expanded[1:], origin)
                    continue
                if directive.startswith("$"):
                    raise ValueError(f"invalid DNS directive {tokens[0]}")
                if not omitted:
                    owner = parse_name(tokens[0], origin)
                    tokens = tokens[1:]
                if owner is None:
                    raise ValueError("DNS record omits its first owner")
                yield self._record(owner, tokens, origin)
            except (ValueError, IndexError) as exc:
                raise ValueError(f"DNS master-file line {lineno}: {exc}") from exc

    def _record(
        self, owner: Name, tokens: tuple[str, ...], origin: Name
    ) -> ResourceRecord:
        ttl = rdclass = None
        offset = 0
        for token in tokens:
            if ttl is None and token[:1].isascii() and token[:1].isdigit():
                ttl = parse_ttl(token)
            elif rdclass is None and (
                token.upper() in ("IN", "CH", "HS") or token.upper().startswith("CLASS")
            ):
                rdclass = record_class(token)
            else:
                break
            offset += 1
        kind = record_type(tokens[offset])
        effective_class = self.rdclass if rdclass is None else rdclass
        fields = tokens[offset + 1 :]
        if kind == RecordType.SOA and self.default_ttl is None:
            if fields and fields[0] == r"\#":
                self.soa_minimum = decoded(
                    from_tokens(owner, 0, effective_class, kind, fields, origin=origin)
                )[-1]
            else:
                self.soa_minimum = parse_ttl(tokens[-1])
            if not self.rfc2308_ttl:
                self.default_ttl = self.soa_minimum
        if ttl is not None:
            self.last_ttl = ttl
        if ttl is None:
            ttl = self.default_ttl
        if ttl is None:
            ttl = self.last_ttl if self.last_ttl is not None else self.soa_minimum
        if ttl is None:
            raise ValueError("DNS record needs a TTL or $TTL directive")
        return from_tokens(owner, ttl, effective_class, kind, fields, origin=origin)


class WritableVersion(ZoneTransaction):
    @property
    def id(self):
        return self._revision + 1

    @property
    def origin(self):
        return self._zone.origin_information()[0]

    @property
    def nodes(self):
        return MappingProxyType(
            {name: self.get_node(name) for name in self.iterate_names()}
        )

    def put_rdataset(self, name, dataset):
        self.replace(name, dataset)

    def delete_rdataset(self, name, rdtype, covers=0):
        self.delete(name, rdtype, covers=covers)

    def delete_node(self, name):
        self.delete(name)


@dataclass(frozen=True)
class Version:
    revision: int
    origin: Name
    rdclass: int
    rrsets: tuple[RRset, ...]

    @property
    def id(self) -> int:
        return self.revision

    def records(self) -> Iterator[ResourceRecord]:
        for rrset in self.rrsets:
            yield from rrset.records

    def iterate_names(self):
        for owner in dict.fromkeys(rrset.owner for rrset in self.rrsets):
            yield DomainName((*owner, b""))

    @property
    def nodes(self):
        return MappingProxyType(
            {name: self.get_node(name) for name in self.iterate_names()}
        )

    def get_node(self, name):
        if isinstance(name, str):
            labels = parse_name(name, self.origin, canonical=True)
        elif isinstance(name, DomainName):
            absolute = name.derelativize(DomainName((*self.origin, b"")))
            labels = _origin_labels(absolute)
        else:
            labels = _origin_labels(name)
        datasets = [
            rrset.to_rdataset() for rrset in self.rrsets if rrset.owner == labels
        ]
        return ImmutableVersionedNode(datasets) if datasets else None


@dataclass(frozen=True)
class ImmutableVersion(Version):
    pass


ZoneSnapshot = ImmutableVersion


class VersionedZone(Zone):
    """A zone retaining a configurable number of immutable committed snapshots."""

    immutable_version_factory = ImmutableVersion
    writable_version_factory = WritableVersion
    node_factory = VersionedNode

    def __init__(
        self,
        origin: str | Name,
        records: Iterable[ResourceRecord] = (),
        *,
        rdclass: int | str = RecordClass.IN,
        versions: int | None = 8,
        pruning_policy: Callable | None = None,
        relativize: bool = False,
    ) -> None:
        if versions is not None and versions <= 0:
            raise ValueError("versioned zone must retain at least one snapshot")
        self._versions = versions
        self._pruning_policy = pruning_policy
        self._history: dict[int, _Index] = {}
        self._writer_lock = RLock()
        self._writer_active = False
        self._readers: dict[int, int] = {}
        super().__init__(origin, records, rdclass=rdclass, relativize=relativize)

    @contextmanager
    def writer(self, replacement: bool = False) -> Iterator[ZoneTransaction]:
        with self._writer_lock:
            if self._writer_active:
                raise RuntimeError("a versioned DNS zone already has an active writer")
            self._writer_active = True
            try:
                with self.transaction(replacement=replacement) as change:
                    yield change
            finally:
                self._writer_active = False

    def find_node(self, name, create=False):
        if create:
            raise UseTransaction("use a DNS zone writer to create nodes")
        return self._immutable_node(super().find_node(name))

    def get_node(self, name, create=False):
        if create:
            raise UseTransaction("use a DNS zone writer to create nodes")
        return super().get_node(name)

    def get_rdataset(self, name, rdtype, covers=0, create=False):
        if create:
            raise UseTransaction("use a DNS zone writer to create datasets")
        dataset = super().get_rdataset(name, rdtype, covers)
        return ImmutableRdataset(dataset) if dataset is not None else None

    def find_rdataset(self, name, rdtype, covers=0, create=False):
        if create:
            raise UseTransaction("use a DNS zone writer to create datasets")
        return super().find_rdataset(name, rdtype, covers)

    def _require_writer(self, *args, **kwargs):
        raise UseTransaction("use a DNS zone writer to edit versioned data")

    delete_node = delete_rdataset = replace_rdataset = _require_writer

    def _committed(self) -> None:
        history = {**self._history, self._revision: self._data}
        self._history = self._prune(history)

    def _prune(self, history: dict[int, _Index]) -> dict[int, _Index]:
        for revision in tuple(history)[:-1]:
            if revision in self._readers:
                break
            if self._pruning_policy is None:
                remove = self._versions is not None and len(history) > self._versions
            else:
                remove = self._pruning_policy(
                    self, self._snapshot(revision, history[revision])
                )
            if not remove:
                break
            del history[revision]
        return history

    def set_max_versions(self, max_versions: int | None) -> None:
        if max_versions is not None and max_versions < 1:
            raise ValueError("versioned zone must retain at least one snapshot")
        with self._lock:
            self._versions = max_versions
            self._pruning_policy = None
            self._history = self._prune(self._history.copy())

    def set_pruning_policy(self, policy: Callable | None) -> None:
        with self._lock:
            previous = self._pruning_policy, self._versions
            self._pruning_policy = policy
            if policy is None:
                self._versions = 1
            try:
                self._history = self._prune(self._history.copy())
            except BaseException:
                self._pruning_policy, self._versions = previous
                raise

    @contextmanager
    def reader(
        self, id: int | None = None, serial: int | None = None
    ) -> Iterator[ZoneTransaction]:
        with self._lock:
            if id is not None and serial is not None:
                raise ValueError("select a DNS zone revision by ID or serial")
            revision = self._revision if id is None else id
            if serial is not None:
                for candidate, data in reversed(self._history.items()):
                    records = data.get((self.origin, RecordType.SOA, None), {})
                    if any(decoded(rr)[2] == serial for rr in records.values()):
                        revision = candidate
                        break
                else:
                    raise KeyError(serial)
            snapshot = ZoneTransaction(
                self, self._history[revision], revision, read_only=True
            )
            self._readers[revision] = self._readers.get(revision, 0) + 1
        try:
            with self._read_transaction(snapshot) as reader:
                yield reader
        finally:
            with self._lock:
                count = self._readers[revision] - 1
                if count:
                    self._readers[revision] = count
                else:
                    del self._readers[revision]
                    self._history = self._prune(self._history.copy())

    def version(self, revision: int | None = None) -> ZoneSnapshot:
        with self._lock:
            revision = self._revision if revision is None else revision
            return self._snapshot(revision, self._history[revision])

    def _snapshot(self, revision: int, data: _Index) -> ZoneSnapshot:
        rrsets = tuple(
            self._rrset(key, data[key])
            for key in sorted(
                data, key=lambda key: (canonical_order(key[0]), key[1], key[2] or 0)
            )
        )
        return self.immutable_version_factory(
            revision, self.origin, self.rdclass, rrsets
        )


def read_rrsets(
    text: str, origin: str, *, rdclass: int | str = RecordClass.IN
) -> tuple[RRset, ...]:
    return Zone.from_text(text, origin, rdclass=rdclass, check_origin=False).rrsets()
