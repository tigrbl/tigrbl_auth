"""Compute and verify SIMPLE zone digests (RFC 8976)."""

import hashlib
import hmac
from struct import Struct

from tba_codec_dns.rdata import decoded
from tba_codec_dns.wire import RecordType, ResourceRecord
from tba_concrete_dns_zone.zone import Zone
from tba_primitives_dns_name.names import canonical_order

_HEADER = Struct("!IBB")
_HASHES = {1: "sha384", 2: "sha512"}


def digest(zone: Zone, algorithm: int = 1) -> bytes:
    if algorithm not in _HASHES:
        raise ValueError("unsupported ZONEMD hash algorithm")
    records = []
    for record in zone.records():
        if tuple(label.lower() for label in record.name) == zone.origin:
            if record.type == RecordType.ZONEMD:
                continue
            if (
                record.type == RecordType.RRSIG
                and decoded(record)[0] == RecordType.ZONEMD
            ):
                continue
        records.append(
            (
                canonical_order(record.name),
                record.type,
                record.uncompressed_data(canonical=True),
                record,
            )
        )
    records.sort(key=lambda item: item[:3])
    hasher = hashlib.new(_HASHES[algorithm])
    for _, _, _, record in records:
        hasher.update(record.to_wire(canonical=True))
    return hasher.digest()


def make_zonemd(zone: Zone, algorithm: int = 1) -> ResourceRecord:
    apex = zone.get(zone.origin, RecordType.SOA)
    if apex is None or len(apex.records) != 1:
        raise ValueError("ZONEMD requires an apex SOA")
    soa = apex.records[0]
    serial = decoded(soa)[2]
    return ResourceRecord(
        zone.origin,
        RecordType.ZONEMD,
        zone.rdclass,
        soa.ttl,
        _HEADER.pack(serial, 1, algorithm) + digest(zone, algorithm),
    )


def verify_zonemd(zone: Zone) -> ResourceRecord:
    candidates = zone.get(zone.origin, RecordType.ZONEMD)
    if candidates is None:
        raise ValueError("zone has no apex ZONEMD records")
    for record in candidates.records:
        _, scheme, algorithm, _ = decoded(record)
        if scheme != 1 or algorithm not in _HASHES:
            continue
        expected = make_zonemd(zone, algorithm)
        if hmac.compare_digest(record.data, expected.data):
            return record
    raise ValueError("no supported ZONEMD verified the zone")
