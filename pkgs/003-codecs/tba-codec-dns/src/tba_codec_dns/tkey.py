"""Wire representation of DNS TKEY records (RFC 2930)."""

from dataclasses import dataclass
from struct import Struct

from tba_primitives_dns_name.names import Name

from .wire import (
    RecordClass,
    RecordType,
    ResourceRecord,
    WireError,
    _name_wire,
    _read_name,
)

_HEADER = Struct("!IIHHH")
_SIZE = Struct("!H")


@dataclass(frozen=True)
class Tkey:
    algorithm: Name
    inception: int
    expiration: int
    mode: int
    error: int = 0
    key: bytes = b""
    other: bytes = b""

    def to_wire(self) -> bytes:
        return (
            _name_wire(self.algorithm)
            + _HEADER.pack(
                self.inception, self.expiration, self.mode, self.error, len(self.key)
            )
            + self.key
            + _SIZE.pack(len(self.other))
            + self.other
        )

    @classmethod
    def from_wire(cls, data: bytes) -> "Tkey":
        algorithm, offset = _read_name(data, 0, canonical=False, compress=False)
        if offset + _HEADER.size > len(data):
            raise WireError("truncated TKEY record")
        inception, expiration, mode, error, size = _HEADER.unpack_from(data, offset)
        start = offset + _HEADER.size
        end = start + size
        if end + 2 > len(data) or end + 2 + _SIZE.unpack_from(data, end)[0] != len(
            data
        ):
            raise WireError("invalid TKEY key or other data length")
        return cls(
            algorithm,
            inception,
            expiration,
            mode,
            error,
            data[start:end],
            data[end + 2 :],
        )

    def record(self, owner: Name) -> ResourceRecord:
        return ResourceRecord(
            owner, RecordType.TKEY, RecordClass.ANY, 0, self.to_wire()
        )
