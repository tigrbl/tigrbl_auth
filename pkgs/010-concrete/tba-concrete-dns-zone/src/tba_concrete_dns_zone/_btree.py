"""Persistent B+ tree index for DNS RRsets in canonical owner order."""

from bisect import bisect_left
from collections.abc import Iterator, MutableMapping
from dataclasses import dataclass

from tba_codec_dns.wire import ResourceRecord
from tba_primitives_dns_name.names import Name, canonical_order

Key = tuple[Name, int, int | None]
Records = dict[bytes, ResourceRecord]
Order = tuple[Name, int, int]
_WIDTH = 16
_MIN = _WIDTH // 2


def _order(key: Key) -> Order:
    owner, kind, covered = key
    return canonical_order(owner), kind, -1 if covered is None else covered


@dataclass(frozen=True, slots=True)
class _Page:
    keys: tuple[Order, ...]
    entries: tuple[tuple[Key, Records], ...] = ()
    children: tuple["_Page", ...] = ()


def _leaf(entries: tuple[tuple[Key, Records], ...]) -> _Page:
    return _Page(tuple(_order(key) for key, _ in entries), entries)


def _branch(children: tuple[_Page, ...]) -> _Page:
    return _Page(tuple(child.keys[-1] for child in children), children=children)


def _insert(
    page: _Page, order: Order, key: Key, value: Records
) -> tuple[tuple[_Page, ...], bool]:
    position = bisect_left(page.keys, order)
    if page.children:
        position = min(position, len(page.children) - 1)
        parts, added = _insert(page.children[position], order, key, value)
        children = page.children[:position] + parts + page.children[position + 1 :]
        if len(children) > _WIDTH:
            return (_branch(children[:_MIN]), _branch(children[_MIN:])), added
        return (_branch(children),), added
    added = position == len(page.keys) or page.keys[position] != order
    entries = (
        page.entries[:position]
        + ((key, value),)
        + page.entries[position + int(not added) :]
    )
    if len(entries) > _WIDTH:
        return (_leaf(entries[:_MIN]), _leaf(entries[_MIN:])), added
    return (_leaf(entries),), added


def _rebalance(left: _Page, right: _Page) -> tuple[_Page, ...]:
    if left.children:
        children = left.children + right.children
        midpoint = len(children) // 2
        if len(children) <= _WIDTH:
            return (_branch(children),)
        return _branch(children[:midpoint]), _branch(children[midpoint:])
    entries = left.entries + right.entries
    midpoint = len(entries) // 2
    if len(entries) <= _WIDTH:
        return (_leaf(entries),)
    return _leaf(entries[:midpoint]), _leaf(entries[midpoint:])


def _remove(page: _Page, order: Order, key: Key) -> _Page:
    position = bisect_left(page.keys, order)
    if position == len(page.keys):
        raise KeyError(key)
    if not page.children:
        if page.keys[position] != order:
            raise KeyError(key)
        return _leaf(page.entries[:position] + page.entries[position + 1 :])
    changed = _remove(page.children[position], order, key)
    children = page.children[:position] + (changed,) + page.children[position + 1 :]
    if len(changed.keys) < _MIN and len(children) > 1:
        left = max(0, position - 1)
        children = (
            children[:left]
            + _rebalance(*children[left : left + 2])
            + children[left + 2 :]
        )
    return _branch(children)


def _entries(page: _Page, start: Order | None = None) -> Iterator[tuple[Key, Records]]:
    position = 0 if start is None else bisect_left(page.keys, start)
    if page.children:
        for child in page.children[position:]:
            yield from _entries(child, start)
            start = None
    else:
        yield from page.entries[position:]


class ZoneIndex(MutableMapping[Key, Records]):
    """A mutable root pointer with immutable pages shared by snapshots."""

    def __init__(self, root: _Page | None = None, size: int = 0) -> None:
        self._root = _leaf(()) if root is None else root
        self._size = size
        self.glue_boundaries: dict[tuple[bytes, ...], bool] = {}

    def copy(self) -> "ZoneIndex":
        duplicate = ZoneIndex(self._root, self._size)
        duplicate.glue_boundaries = self.glue_boundaries.copy()
        return duplicate

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[Key]:
        return (key for key, _ in _entries(self._root))

    def __getitem__(self, key: Key) -> Records:
        match = next(_entries(self._root, _order(key)), None)
        if match is None or match[0] != key:
            raise KeyError(key)
        return match[1]

    def __setitem__(self, key: Key, value: Records) -> None:
        pages, added = _insert(self._root, _order(key), key, value)
        self._root = pages[0] if len(pages) == 1 else _branch(pages)
        self._size += added

    def __delitem__(self, key: Key) -> None:
        root = _remove(self._root, _order(key), key)
        self._root = root.children[0] if len(root.children) == 1 else root
        self._size -= 1

    def from_key(self, key: Key) -> Iterator[Key]:
        return (found for found, _ in _entries(self._root, _order(key)))

    def floor(self, key: Key) -> Key | None:
        order = _order(key)
        page = self._root
        previous = None
        while page.children:
            position = min(bisect_left(page.keys, order), len(page.children) - 1)
            if position:
                previous = page.children[position - 1]
            page = page.children[position]
        position = bisect_left(page.keys, order)
        if position < len(page.keys) and page.keys[position] == order:
            return page.entries[position][0]
        if position:
            return page.entries[position - 1][0]
        if previous is None:
            return None
        while previous.children:
            previous = previous.children[-1]
        return previous.entries[-1][0]
