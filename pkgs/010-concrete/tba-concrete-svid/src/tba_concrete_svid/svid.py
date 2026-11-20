from dataclasses import dataclass

from tba_contracts_workload_identity import SpiffeId, SvidFormat

from .spiffe_ids import normalize_spiffe_id


@dataclass(frozen=True, slots=True)
class SvidIdentity:
    spiffe_id: SpiffeId
    format: SvidFormat

    def __post_init__(self):
        object.__setattr__(self, "spiffe_id", normalize_spiffe_id(self.spiffe_id))
        object.__setattr__(self, "format", SvidFormat(self.format))
