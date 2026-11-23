"""Compute and verify SIMPLE zone digests (RFC 8976)."""

import hashlib
import hmac
from collections import Counter
from enum import IntEnum
from struct import Struct

from tba_codec_dns.rdata import Rdata
from tba_codec_dns.wire import RecordType, ResourceRecord
from tba_primitives_dns_name.names import canonical_order

_HEADER = Struct("!IBB")


class DigestScheme(IntEnum):
    SIMPLE = 1


class DigestHashAlgorithm(IntEnum):
    SHA384 = 1
    SHA512 = 2


class UnsupportedDigestScheme(ValueError):
    """The ZONEMD scheme is unsupported."""


class UnsupportedDigestHashAlgorithm(ValueError):
    """The ZONEMD hash algorithm is unsupported."""


class NoDigest(ValueError):
    """The zone has no apex ZONEMD data."""


class DigestVerificationFailure(ValueError):
    """No eligible ZONEMD verified the zone."""


_HASHES = {DigestHashAlgorithm.SHA384: "sha384", DigestHashAlgorithm.SHA512: "sha512"}


def _digest(zone, txn, algorithm, scheme) -> bytes:
    if scheme != DigestScheme.SIMPLE:
        raise UnsupportedDigestScheme(scheme)
    try:
        hasher = hashlib.new(_HASHES[algorithm])
    except KeyError as exc:
        raise UnsupportedDigestHashAlgorithm(algorithm) from exc
    origin, _, apex = zone.origin_information()
    datasets = []
    for owner, dataset in txn.iterate_rdatasets():
        if owner == apex and RecordType.ZONEMD in (dataset.rdtype, dataset.covers):
            continue
        labels = owner.derelativize(origin).labels[:-1]
        datasets.append(
            (canonical_order(labels), dataset.rdtype, dataset.covers, labels, dataset)
        )
    for _, _, _, labels, dataset in sorted(datasets, key=lambda entry: entry[:3]):
        records = sorted(
            dataset.records(labels), key=lambda rr: rr.uncompressed_data(canonical=True)
        )
        for record in records:
            hasher.update(record.to_wire(canonical=True))
    return hasher.digest()


def digest(zone, algorithm: int = DigestHashAlgorithm.SHA384) -> bytes:
    with zone.reader() as txn:
        return _digest(zone, txn, algorithm, DigestScheme.SIMPLE)


def make_zonemd(
    zone, algorithm: int = DigestHashAlgorithm.SHA384, scheme: int = DigestScheme.SIMPLE
) -> ResourceRecord:
    with zone.reader() as txn:
        soa = txn.get(zone.origin, RecordType.SOA)
        if not soa or len(soa) != 1:
            raise ValueError("ZONEMD requires one apex SOA")
        data = _digest(zone, txn, algorithm, scheme)
        return ResourceRecord(
            zone.origin,
            RecordType.ZONEMD,
            zone.rdclass,
            soa.ttl,
            _HEADER.pack(soa[0].serial, scheme, algorithm) + data,
        )


def verify_zonemd(zone, zonemd: Rdata | None = None) -> ResourceRecord:
    with zone.reader() as txn:
        candidates = (
            txn.get(zone.origin, RecordType.ZONEMD) if zonemd is None else (zonemd,)
        )
        if not candidates:
            raise NoDigest("zone has no apex ZONEMD records")
        soa = txn.get(zone.origin, RecordType.SOA)
        if not soa or len(soa) != 1:
            raise DigestVerificationFailure("ZONEMD requires one apex SOA")
        occurrences = Counter(
            (value.scheme, value.hash_algorithm) for value in candidates
        )
        for value in candidates:
            scheme, algorithm = value.scheme, value.hash_algorithm
            if occurrences[(scheme, algorithm)] != 1 or value.serial != soa[0].serial:
                continue
            if scheme != DigestScheme.SIMPLE or algorithm not in _HASHES:
                continue
            expected = _digest(zone, txn, algorithm, scheme)
            if hmac.compare_digest(value.digest, expected):
                ttl = 0 if zonemd is not None else candidates.ttl
                return value.record(zone.origin, ttl)
    raise DigestVerificationFailure("no eligible ZONEMD verified the zone")
