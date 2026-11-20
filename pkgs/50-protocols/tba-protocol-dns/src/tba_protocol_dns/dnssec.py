"""DNSSEC canonicalization, DS records, and signature operations."""

import base64
import hashlib
import time
from collections.abc import Iterable
from dataclasses import dataclass, replace
from enum import IntEnum, IntFlag
from struct import Struct

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import (
    dsa,
    ec,
    ed448,
    ed25519,
    padding,
    rsa,
    utils,
)
from tba_codec_dns.rdata import decoded, type_bitmap
from tba_codec_dns.rdataset import Rdataset
from tba_codec_dns.rdataset import from_records as dataset_from_records
from tba_codec_dns.wire import RecordClass, RecordType, ResourceRecord, _name_wire
from tba_concrete_dns_zone.zone import Zone
from tba_primitives_dns_name.names import (
    Name,
    canonical_order,
    is_subdomain,
    parse_name,
)

_SIG = Struct("!HBBIIIH")
_KEY = Struct("!HBB")
_DS = Struct("!HBB")
_RSA = {
    1: hashes.MD5,
    5: hashes.SHA1,
    7: hashes.SHA1,
    8: hashes.SHA256,
    10: hashes.SHA512,
}
_DSA = frozenset({3, 6})
_EC = {13: (ec.SECP256R1, hashes.SHA256, 32), 14: (ec.SECP384R1, hashes.SHA384, 48)}
_ED = {
    15: (ed25519.Ed25519PrivateKey, ed25519.Ed25519PublicKey),
    16: (ed448.Ed448PrivateKey, ed448.Ed448PublicKey),
}
_DIGESTS = {1: "sha1", 2: "sha256", 4: "sha384"}


class Algorithm(IntEnum):
    RSAMD5 = 1
    DH = 2
    DSA = 3
    RSASHA1 = 5
    DSANSEC3SHA1 = 6
    RSASHA1NSEC3SHA1 = 7
    RSASHA256 = 8
    RSASHA512 = 10
    ECCGOST = 12
    ECDSAP256SHA256 = 13
    ECDSAP384SHA384 = 14
    ED25519 = 15
    ED448 = 16
    SM2SM3 = 17
    ECCGOST12 = 23
    INDIRECT = 252
    PRIVATEDNS = 253
    PRIVATEOID = 254


class DSDigest(IntEnum):
    SHA1 = 1
    SHA256 = 2
    GOST = 3
    SHA384 = 4


class Flag(IntFlag):
    SEP = 1
    REVOKE = 128
    ZONE = 256


def algorithm_from_text(text: str | int) -> int:
    if isinstance(text, str):
        if text.startswith("-") and text[1:].isdecimal():
            raise ValueError("DNSSEC algorithm outside 0..255")
        name = text.upper().replace("-", "")
        if not name.isdecimal():
            try:
                return Algorithm[name]
            except KeyError as exc:
                raise ValueError(f"unknown DNSSEC algorithm {text!r}") from exc
        text = int(name)
    if not 0 <= text <= 255:
        raise ValueError("DNSSEC algorithm outside 0..255")
    return text


def algorithm_to_text(value: int) -> str:
    value = algorithm_from_text(value)
    try:
        return Algorithm(value).name
    except ValueError:
        return str(value)


class ValidationError(ValueError):
    """DNSSEC data did not pass validation."""


@dataclass(frozen=True)
class Policy:
    sign_algorithms: frozenset[int] = frozenset({8, 10, 13, 14, 15, 16})
    validate_algorithms: frozenset[int] = frozenset({5, 7, 8, 10, 13, 14, 15, 16})
    create_ds_digests: frozenset[int] = frozenset({2, 4})
    validate_ds_digests: frozenset[int] = frozenset({1, 2, 4})


DEFAULT_POLICY = Policy()


def _canonical(name: Name) -> Name:
    return tuple(label.lower() for label in name)


def key_tag(key: ResourceRecord) -> int:
    if (
        key.type not in (RecordType.DNSKEY, RecordType.CDNSKEY, RecordType.KEY)
        or len(key.data) < 4
    ):
        raise ValidationError("invalid DNSKEY data")
    if key.data[3] == 1:
        if len(key.data) < 7:
            raise ValidationError("truncated RSAMD5 DNSKEY")
        return int.from_bytes(key.data[-3:-1], "big")
    total = sum(
        byte << 8 if index % 2 == 0 else byte for index, byte in enumerate(key.data)
    )
    return (total + (total >> 16)) & 65535


def make_ds(
    key: ResourceRecord,
    digest: int | str = 2,
    *,
    policy: Policy = DEFAULT_POLICY,
    validating: bool = False,
    cds: bool = False,
) -> ResourceRecord:
    if isinstance(digest, str):
        try:
            digest = DSDigest[digest.upper().replace("-", "")]
        except KeyError as exc:
            raise ValidationError(f"unsupported DS digest {digest!r}") from exc
    allowed = policy.validate_ds_digests if validating else policy.create_ds_digests
    if (
        key.type not in (RecordType.DNSKEY, RecordType.CDNSKEY)
        or digest not in allowed
        or digest not in _DIGESTS
    ):
        raise ValidationError("DS digest denied or DNSKEY type is invalid")
    _, protocol, algorithm, _ = decoded(key)
    if protocol != 3:
        raise ValidationError("DNSKEY protocol must be 3")
    value = hashlib.new(
        _DIGESTS[digest], _name_wire(_canonical(key.name)) + key.data
    ).digest()
    return ResourceRecord(
        key.name,
        RecordType.CDS if cds else RecordType.DS,
        key.rdclass,
        key.ttl,
        _DS.pack(key_tag(key), algorithm, digest) + value,
    )


def _integer(value: int) -> bytes:
    return value.to_bytes(max(1, (value.bit_length() + 7) // 8), "big")


def make_dnskey(
    owner: str | Name,
    public_key,
    algorithm: int | str,
    *,
    flags: int = 256,
    ttl: int = 3600,
    rdclass: int = RecordClass.IN,
    cdnskey: bool = False,
) -> ResourceRecord:
    algorithm = algorithm_from_text(algorithm)
    name = (
        parse_name(owner, canonical=True)
        if isinstance(owner, str)
        else _canonical(owner)
    )
    if algorithm in _RSA and isinstance(public_key, rsa.RSAPublicKey):
        numbers = public_key.public_numbers()
        exponent = _integer(numbers.e)
        size = len(exponent)
        data = bytes((size,)) if size < 256 else b"\x00" + size.to_bytes(2, "big")
        data += exponent + _integer(numbers.n)
    elif algorithm in _DSA and isinstance(public_key, dsa.DSAPublicKey):
        numbers = public_key.public_numbers()
        params = numbers.parameter_numbers
        width = len(_integer(params.p))
        if not 64 <= width <= 128 or (width - 64) % 8 or params.q.bit_length() != 160:
            raise ValidationError("DSA parameters cannot be encoded as DNSKEY")
        t = (width - 64) // 8
        data = (
            bytes((t,))
            + params.q.to_bytes(20, "big")
            + b"".join(
                number.to_bytes(width, "big")
                for number in (params.p, params.g, numbers.y)
            )
        )
    elif algorithm in _EC and isinstance(public_key, ec.EllipticCurvePublicKey):
        curve, _, size = _EC[algorithm]
        if not isinstance(public_key.curve, curve):
            raise ValidationError("DNSKEY curve does not match its algorithm")
        numbers = public_key.public_numbers()
        data = numbers.x.to_bytes(size, "big") + numbers.y.to_bytes(size, "big")
    elif algorithm in _ED and isinstance(public_key, _ED[algorithm][1]):
        data = public_key.public_bytes(
            serialization.Encoding.Raw, serialization.PublicFormat.Raw
        )
    else:
        raise ValidationError("public key does not match its DNSSEC algorithm")
    return ResourceRecord(
        name,
        RecordType.CDNSKEY if cdnskey else RecordType.DNSKEY,
        rdclass,
        ttl,
        _KEY.pack(flags, 3, algorithm) + data,
    )


def make_cdnskey(
    owner: str | Name, public_key, algorithm: int | str, **kwargs
) -> ResourceRecord:
    return make_dnskey(owner, public_key, algorithm, cdnskey=True, **kwargs)


def make_cds(key: ResourceRecord, digest: int | str = 2, **kwargs) -> ResourceRecord:
    return make_ds(key, digest, cds=True, **kwargs)


def make_ds_rdataset(
    owner: str | Name,
    keys: Rdataset,
    digests: Iterable[int | str] = (DSDigest.SHA256,),
    *,
    policy: Policy = DEFAULT_POLICY,
    cds: bool = False,
) -> Rdataset:
    name = (
        parse_name(owner, canonical=True)
        if isinstance(owner, str)
        else _canonical(owner)
    )
    algorithms = tuple(digests)
    if not algorithms:
        raise ValueError("a DS dataset requires at least one digest algorithm")
    return dataset_from_records(
        make_ds(key, digest, policy=policy, cds=cds)
        for key in keys.records(name)
        for digest in algorithms
    )


def _public_key(algorithm: int, data: bytes):
    try:
        if algorithm in _RSA:
            if not data:
                raise ValueError("missing RSA exponent")
            offset, size = (
                (1, data[0]) if data[0] else (3, int.from_bytes(data[1:3], "big"))
            )
            if not size or offset + size >= len(data):
                raise ValueError("bad RSA exponent length")
            exponent = int.from_bytes(data[offset : offset + size], "big")
            modulus = int.from_bytes(data[offset + size :], "big")
            return rsa.RSAPublicNumbers(exponent, modulus).public_key()
        if algorithm in _DSA:
            if not data or data[0] > 8:
                raise ValueError("bad DSA parameter size")
            width = 64 + 8 * data[0]
            if len(data) != 21 + 3 * width:
                raise ValueError("bad DSA public key length")
            q = int.from_bytes(data[1:21], "big")
            p, g, y = (
                int.from_bytes(data[start : start + width], "big")
                for start in range(21, len(data), width)
            )
            return dsa.DSAPublicNumbers(
                y, dsa.DSAParameterNumbers(p, q, g)
            ).public_key()
        if algorithm in _EC:
            curve, _, size = _EC[algorithm]
            if len(data) != 2 * size:
                raise ValueError("bad ECDSA point length")
            return ec.EllipticCurvePublicKey.from_encoded_point(curve(), b"\x04" + data)
        if algorithm in _ED:
            return _ED[algorithm][1].from_public_bytes(data)
    except ValueError as exc:
        raise ValidationError("invalid DNSKEY public-key encoding") from exc
    raise ValidationError("unsupported DNSSEC algorithm")


def _rrset(records: Iterable[ResourceRecord]) -> tuple[ResourceRecord, ...]:
    items = tuple(records)
    if not items:
        raise ValidationError("DNSSEC requires a nonempty RRset")
    first = items[0]
    if any(
        (_canonical(rr.name), rr.type, rr.rdclass)
        != (_canonical(first.name), first.type, first.rdclass)
        for rr in items
    ):
        raise ValidationError("inconsistent DNSSEC RRset")
    return items


def _signature_data(
    records: tuple[ResourceRecord, ...], signature: ResourceRecord
) -> bytes:
    covered, _, labels, ttl, _, _, _, signer, _ = decoded(signature)
    first = records[0]
    owner = _canonical(first.name)
    if (
        signature.type != RecordType.RRSIG
        or _canonical(signature.name) != owner
        or signature.rdclass != first.rdclass
        or covered != first.type
        or labels > len(owner)
        or not is_subdomain(owner, signer)
    ):
        raise ValidationError("signature does not cover this DNS RRset")
    if owner[:1] == (b"*",) and labels != len(owner) - 1:
        raise ValidationError("wrong labels count for wildcard RRset")
    if labels < len(owner):
        owner = (b"*",) + owner[len(owner) - labels :]
    ordered = sorted({rr.uncompressed_data(canonical=True) for rr in records})
    return (
        signature.data[: _SIG.size]
        + _name_wire(_canonical(signer))
        + b"".join(
            ResourceRecord(owner, first.type, first.rdclass, ttl, item).to_wire()
            for item in ordered
        )
    )


def _seconds(start: int, end: int) -> int:
    return (end - start) % 2**32


def sign_rrset(
    records: Iterable[ResourceRecord],
    key: ResourceRecord,
    private_key,
    *,
    inception: int,
    expiration: int,
    policy: Policy = DEFAULT_POLICY,
) -> ResourceRecord:
    items = _rrset(records)
    first = items[0]
    if key.type != RecordType.DNSKEY or key.rdclass != first.rdclass:
        raise ValidationError("signing requires a matching DNSKEY")
    flags, protocol, algorithm, _ = decoded(key)
    if protocol != 3 or not flags & 256 or algorithm not in policy.sign_algorithms:
        raise ValidationError("DNSKEY is not permitted for signing")
    if not 0 < expiration - inception < 2**31:
        raise ValidationError("invalid DNSSEC signature validity period")
    if (
        make_dnskey(key.name, private_key.public_key(), algorithm, flags=flags).data
        != key.data
    ):
        raise ValidationError("private key does not match the DNSKEY")
    labels = len(first.name) - int(first.name[:1] == (b"*",))
    ttl = min(rr.ttl for rr in items)
    unsigned = _SIG.pack(
        first.type,
        algorithm,
        labels,
        ttl,
        expiration % 2**32,
        inception % 2**32,
        key_tag(key),
    ) + _name_wire(_canonical(key.name))
    signature = ResourceRecord(
        first.name, RecordType.RRSIG, first.rdclass, ttl, unsigned
    )
    payload = _signature_data(items, signature)
    if algorithm in _RSA:
        raw = private_key.sign(payload, padding.PKCS1v15(), _RSA[algorithm]())
    elif algorithm in _DSA:
        r, s = utils.decode_dss_signature(private_key.sign(payload, hashes.SHA1()))
        raw = key.data[4:5] + r.to_bytes(20, "big") + s.to_bytes(20, "big")
    elif algorithm in _EC:
        _, digest, size = _EC[algorithm]
        r, s = utils.decode_dss_signature(private_key.sign(payload, ec.ECDSA(digest())))
        raw = r.to_bytes(size, "big") + s.to_bytes(size, "big")
    else:
        raw = private_key.sign(payload)
    return replace(signature, data=unsigned + raw)


def validate_rrsig(
    records: Iterable[ResourceRecord],
    signature: ResourceRecord,
    keys: Iterable[ResourceRecord],
    *,
    now: int | None = None,
    policy: Policy = DEFAULT_POLICY,
) -> None:
    items = _rrset(records)
    if signature.type != RecordType.RRSIG:
        raise ValidationError("expected a DNS RRSIG record")
    _, algorithm, _, _, expiration, inception, tag, signer, raw = decoded(signature)
    current = int(time.time()) if now is None else now
    if not 0 < _seconds(inception, expiration) < 2**31 or _seconds(
        inception, current
    ) > _seconds(inception, expiration):
        raise ValidationError("DNSSEC signature outside its validity period")
    if algorithm not in policy.validate_algorithms:
        raise ValidationError("DNSSEC signature algorithm denied")
    payload = _signature_data(items, signature)
    for key in keys:
        if (
            key.type != RecordType.DNSKEY
            or key.rdclass != signature.rdclass
            or _canonical(key.name) != _canonical(signer)
        ):
            continue
        flags, protocol, key_algorithm, data = decoded(key)
        if (
            protocol != 3
            or not flags & Flag.ZONE
            or (flags & Flag.REVOKE and items[0].type != RecordType.DNSKEY)
            or key_algorithm != algorithm
            or key_tag(key) != tag
        ):
            continue
        try:
            public_key = _public_key(algorithm, data)
            if algorithm in _RSA:
                public_key.verify(raw, payload, padding.PKCS1v15(), _RSA[algorithm]())
            elif algorithm in _DSA:
                if len(raw) != 41 or raw[0] != data[0]:
                    raise ValidationError("invalid DNSSEC DSA signature length")
                signature_der = utils.encode_dss_signature(
                    int.from_bytes(raw[1:21], "big"), int.from_bytes(raw[21:41], "big")
                )
                public_key.verify(signature_der, payload, hashes.SHA1())
            elif algorithm in _EC:
                _, digest, size = _EC[algorithm]
                if len(raw) != 2 * size:
                    raise ValidationError("invalid DNSSEC ECDSA signature length")
                signature_der = utils.encode_dss_signature(
                    int.from_bytes(raw[:size], "big"), int.from_bytes(raw[size:], "big")
                )
                public_key.verify(signature_der, payload, ec.ECDSA(digest()))
            else:
                public_key.verify(raw, payload)
            return
        except (InvalidSignature, ValidationError):
            continue
    raise ValidationError("no DNSKEY validated the RRSIG")


def validate(
    records: Iterable[ResourceRecord],
    signatures: Iterable[ResourceRecord],
    keys: Iterable[ResourceRecord],
    *,
    now: int | None = None,
    policy: Policy = DEFAULT_POLICY,
) -> None:
    items, candidates = tuple(records), tuple(keys)
    for signature in signatures:
        try:
            validate_rrsig(items, signature, candidates, now=now, policy=policy)
            return
        except ValueError:
            continue
    raise ValidationError("no valid DNSSEC RRSIG for RRset")


def nsec3_hash(
    name: str | Name, salt: str | bytes, iterations: int, algorithm: int = 1
) -> str:
    if algorithm != 1 or not 0 <= iterations <= 65535:
        raise ValueError("unsupported NSEC3 hash algorithm or iteration count")
    owner = (
        parse_name(name, canonical=True) if isinstance(name, str) else _canonical(name)
    )
    if isinstance(salt, str):
        salt = b"" if salt == "-" else bytes.fromhex(salt)
    if len(salt) > 255:
        raise ValueError("NSEC3 salt is longer than 255 octets")
    digest = hashlib.sha1(_name_wire(owner) + salt).digest()
    for _ in range(iterations):
        digest = hashlib.sha1(digest + salt).digest()
    return base64.b32hexencode(digest).decode().rstrip("=")


def sign_zone(
    zone: Zone,
    keys: Iterable[tuple[ResourceRecord, object]],
    *,
    inception: int,
    expiration: int,
    policy: Policy = DEFAULT_POLICY,
) -> Zone:
    """Return a signed snapshot with an NSEC chain and delegation-aware signatures."""
    keys = tuple(keys)
    if not keys or any(
        _canonical(key.name) != zone.origin or key.rdclass != zone.rdclass
        for key, _ in keys
    ):
        raise ValidationError("zone signing requires apex DNSKEYs from the same class")
    snapshot = Zone(
        zone.origin,
        (
            rr
            for rr in zone.records()
            if rr.type
            not in (
                RecordType.NSEC,
                RecordType.NSEC3,
                RecordType.NSEC3PARAM,
                RecordType.RRSIG,
            )
        ),
        rdclass=zone.rdclass,
    )
    snapshot.check_origin()
    with snapshot.transaction() as change:
        for key, _ in keys:
            change.add(key)
    rrsets = snapshot.rrsets()
    cuts = {
        rrset.owner
        for rrset in rrsets
        if rrset.type == RecordType.NS and rrset.owner != snapshot.origin
    }
    cuts = {
        owner
        for owner in cuts
        if not any(is_subdomain(owner[1:], other) for other in cuts)
    }
    authoritative = [
        rrset
        for rrset in rrsets
        if not any(is_subdomain(rrset.owner[1:], cut) for cut in cuts)
        and (rrset.owner not in cuts or rrset.type in (RecordType.NS, RecordType.DS))
    ]
    names: dict[Name, set[int]] = {}
    for rrset in authoritative:
        names.setdefault(rrset.owner, {RecordType.NSEC, RecordType.RRSIG}).add(
            rrset.type
        )
    ordered = sorted(names, key=canonical_order)
    soa = snapshot.get(snapshot.origin, RecordType.SOA).records[0]
    nsec_ttl = min(soa.ttl, decoded(soa)[-1])
    ksk = [(key, private) for key, private in keys if decoded(key)[0] & 1] or keys
    zsk = [(key, private) for key, private in keys if not decoded(key)[0] & 1] or keys

    def signatures(records, signers):
        for key, private in signers:
            yield sign_rrset(
                records,
                key,
                private,
                inception=inception,
                expiration=expiration,
                policy=policy,
            )

    with snapshot.transaction() as change:
        for rrset in authoritative:
            if rrset.owner in cuts and rrset.type == RecordType.NS:
                continue
            for signature in signatures(
                rrset.records, ksk if rrset.type == RecordType.DNSKEY else zsk
            ):
                change.add(signature)
        for owner, successor in zip(ordered, ordered[1:] + ordered[:1]):
            bitmap = type_bitmap(tuple(names[owner]))
            nsec = ResourceRecord(
                owner,
                RecordType.NSEC,
                zone.rdclass,
                nsec_ttl,
                _name_wire(successor) + bitmap,
            )
            change.add(nsec)
            for signature in signatures((nsec,), zsk):
                change.add(signature)
    return snapshot
