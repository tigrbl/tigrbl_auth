"""DNS owner nodes containing one dataset per class, type, and covered type."""

from collections.abc import Iterable, Iterator

from .rdataset import Rdataset
from .wire import record_class, record_type


class Node:
    def __init__(self, rdatasets: Iterable[Rdataset] = ()) -> None:
        self._sets: dict[tuple[int, int, int], Rdataset] = {}
        for dataset in rdatasets:
            self.replace_rdataset(dataset)

    @property
    def rdatasets(self) -> tuple[Rdataset, ...]:
        return tuple(self._sets.values())

    def __iter__(self) -> Iterator[Rdataset]:
        return iter(self._sets.values())

    def __len__(self) -> int:
        return len(self._sets)

    def find_rdataset(
        self, rdclass, rdtype, covers=0, create: bool = False
    ) -> Rdataset:
        key = (record_class(rdclass), record_type(rdtype), record_type(covers))
        result = self._sets.get(key)
        if result is not None:
            return result
        if not create:
            raise KeyError(key)
        result = Rdataset(*key)
        self._sets[key] = result
        return result

    def get_rdataset(
        self, rdclass, rdtype, covers=0, create: bool = False
    ) -> Rdataset | None:
        try:
            return self.find_rdataset(rdclass, rdtype, covers, create)
        except KeyError:
            return None

    def delete_rdataset(self, rdclass, rdtype, covers=0) -> None:
        self._sets.pop(
            (record_class(rdclass), record_type(rdtype), record_type(covers)), None
        )

    def replace_rdataset(self, dataset: Rdataset) -> None:
        self._sets[(dataset.rdclass, dataset.rdtype, dataset.covers)] = dataset.copy()
