"""B-tree-backed zones with copy-on-write snapshots and DNS name bounds."""

from collections.abc import Callable, Iterator, MutableSet
from dataclasses import dataclass
from enum import IntFlag
from itertools import groupby
from types import MappingProxyType

from tba_codec_dns.node import Node as RecordNode
from tba_codec_dns.rrset import RRset
from tba_codec_dns.wire import RecordClass, RecordType, ResourceRecord
from tba_primitives_dns_name.name import Name, from_text
from tba_primitives_dns_name.names import Name as Labels
from tba_primitives_dns_name.names import common_ancestor, is_subdomain

from ._btree import ZoneIndex
from ._immutable import ImmutableVersionedNode
from .zone import VersionedZone
from .zone import WritableVersion as BaseWritableVersion


class NodeFlags(IntFlag):
    ORIGIN = 1
    DELEGATION = 2
    GLUE = 4


class Node(RecordNode):
    """An owner and its role in the selected version of the zone."""

    def __init__(self, rdatasets=(), *, flags: NodeFlags = NodeFlags(0)) -> None:
        super().__init__(rdatasets)
        self.flags = flags

    def is_origin(self) -> bool:
        return bool(self.flags & NodeFlags.ORIGIN)

    def is_delegation(self) -> bool:
        return bool(self.flags & NodeFlags.DELEGATION)

    def is_glue(self) -> bool:
        return bool(self.flags & NodeFlags.GLUE)

    def is_origin_or_glue(self) -> bool:
        return self.is_origin() or self.is_glue()


class ImmutableNode(ImmutableVersionedNode, Node):
    def __init__(self, rdatasets=(), *, flags=NodeFlags(0)):
        super().__init__(rdatasets)
        object.__setattr__(self, "flags", flags)


class Delegations(MutableSet):
    """Canonical set of visible delegation points in a DNS zone."""

    def __init__(self, names=()):
        self._names = set(names)

    def __contains__(self, name):
        return name in self._names

    def __iter__(self):
        return iter(sorted(self._names))

    def __len__(self):
        return len(self._names)

    def add(self, name):
        self._names.add(name)

    def discard(self, name):
        self._names.discard(name)

    def get_delegation(self, name):
        if isinstance(name, str):
            name = from_text(name)
        ancestor = next((entry for entry in self if name.is_subdomain(entry)), None)
        return ancestor, ancestor is not None and name != ancestor

    def is_glue(self, name):
        return self.get_delegation(name)[1]


@dataclass(frozen=True)
class Bounds:
    name: Name
    left: Name
    right: Name | None
    closest_encloser: Name
    is_equal: bool
    is_delegation: bool


def _delegation(index: ZoneIndex, owner: Labels, origin: Labels) -> Labels | None:
    # An ancestor delegation obscures all nested NS records.
    if owner != origin and index.glue_boundaries.get(origin):
        return origin
    for offset in range(len(owner) - len(origin) - 1, -1, -1):
        candidate = owner[offset:]
        boundary = (candidate, RecordType.NS, None) in index
        if candidate != owner:
            boundary = index.glue_boundaries.get(candidate, boundary)
        if boundary:
            return candidate
    return None


@dataclass(frozen=True)
class ImmutableVersion:
    zone: "Zone"
    revision: int
    _index: ZoneIndex

    @property
    def id(self) -> int:
        return self.revision

    @property
    def origin(self) -> Labels:
        return self.zone.origin

    @property
    def rdclass(self) -> int:
        return self.zone.rdclass

    @property
    def rrsets(self) -> tuple[RRset, ...]:
        return tuple(self.zone._rrset(key, self._index[key]) for key in self._index)

    def records(self) -> Iterator[ResourceRecord]:
        for rrset in self.rrsets:
            yield from rrset.records

    def iterate_names(self) -> Iterator[Name]:
        for owner, _ in groupby(self._index, key=lambda key: key[0]):
            yield self.zone._display(owner)

    @property
    def nodes(self):
        return MappingProxyType(
            {name: self.get_node(name) for name in self.iterate_names()}
        )

    def get_node(self, name: str | Name | Labels) -> Node | None:
        node = self.zone._node_at(self._index, self.zone._owner(name))
        return None if node is None else self.zone._immutable_node(node)

    @property
    def delegations(self):
        return self.zone._delegations(self._index)

    def get_delegation(self, name: str | Name | Labels) -> tuple[Name | None, bool]:
        owner = self.zone._owner(name)
        if not is_subdomain(owner, self.origin):
            return None, False
        delegation = _delegation(self._index, owner, self.origin)
        if delegation is None:
            return None, False
        return self.zone._display(delegation), delegation != owner

    def bounds(self, name: str | Name | Labels) -> Bounds:
        owner = self.zone._owner(name)
        if not is_subdomain(owner, self.origin):
            raise KeyError(name)
        edge = (owner, 65536, None)
        before = self._index.floor(edge)
        after = next(self._index.from_key(edge), None)
        left = self.origin if before is None else before[0]
        right = None if after is None else after[0]
        closest = common_ancestor(owner, left)
        if right is not None:
            closest = max(closest, common_ancestor(owner, right), key=len)
        return Bounds(
            self.zone._display(owner),
            self.zone._display(left),
            None if right is None else self.zone._display(right),
            self.zone._display(closest),
            before is not None and left == owner,
            _delegation(self._index, left, self.origin) == left,
        )


class WritableVersion(BaseWritableVersion):
    """A B-tree zone writer with a view of its current delegations."""

    def update_glue_flag(self, name, is_glue):
        """Obscure or expose proper descendants of a delegation point."""
        self._ensure_open(write=True)
        owner = self._zone._owner(name)
        if not is_subdomain(owner, self._zone.origin):
            raise KeyError(name)
        natural = (
            owner != self._zone.origin and (owner, RecordType.NS, None) in self._data
        )
        boundaries = self._data.glue_boundaries
        if boundaries.get(owner, natural) == is_glue:
            return
        if is_glue == natural:
            boundaries.pop(owner, None)
        else:
            boundaries[owner] = is_glue
        self._changed = True

    def _set_records(self, key, records):
        was_present = key in self._data
        super()._set_records(key, records)
        if key[1] == RecordType.NS and was_present != bool(records):
            self._data.glue_boundaries.pop(key[0], None)

    @property
    def delegations(self):
        self._ensure_open()
        return self._zone._delegations(self._data)


class Zone(VersionedZone):
    """A versioned zone that shares B-tree pages across revisions."""

    map_factory = ZoneIndex
    node_factory = Node
    writable_version_factory = WritableVersion
    immutable_version_factory = ImmutableVersion

    def __init__(
        self,
        origin: str | Name | Labels,
        records=(),
        *,
        rdclass: int | str = RecordClass.IN,
        versions: int | None = 1,
        relativize: bool = True,
        pruning_policy: Callable | None = None,
    ) -> None:
        super().__init__(
            origin,
            records,
            rdclass=rdclass,
            versions=versions,
            pruning_policy=pruning_policy,
            relativize=relativize,
        )

    def _new_index(self) -> ZoneIndex:
        return self.map_factory()

    def _snapshot(self, revision: int, data: ZoneIndex) -> ImmutableVersion:
        return self.immutable_version_factory(self, revision, data)

    def version(self, revision: int | None = None) -> ImmutableVersion:
        return super().version(revision)

    def _node_at(self, data: ZoneIndex, owner: Labels) -> Node | None:
        datasets = self._datasets_at(data, owner)
        if not datasets:
            return None
        flags = NodeFlags(0)
        if owner == self.origin:
            flags = NodeFlags.ORIGIN
        else:
            delegated = _delegation(data, owner, self.origin)
            if delegated is not None:
                flags = NodeFlags.DELEGATION if delegated == owner else NodeFlags.GLUE
        return self.node_factory(datasets, flags=flags)

    def _immutable_node(self, node):
        return ImmutableNode(node.rdatasets, flags=node.flags)

    def _delegations(self, data):
        names = {
            owner
            for owner, kind, _ in data
            if kind == RecordType.NS and owner != self.origin
        }
        for owner, hidden in data.glue_boundaries.items():
            if hidden:
                names.add(owner)
            else:
                names.discard(owner)
        visible = {
            owner
            for owner in names
            if _delegation(data, owner, self.origin) in (None, owner)
        }
        return Delegations(self._display(owner) for owner in visible)

    def __iter__(self) -> Iterator[Name]:
        return self.version().iterate_names()

    def rrsets(self) -> tuple[RRset, ...]:
        return self.version().rrsets

    def bounds(self, name: str | Name | Labels) -> Bounds:
        return self.version().bounds(name)
