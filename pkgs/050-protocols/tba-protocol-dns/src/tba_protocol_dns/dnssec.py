"""DNSSEC canonicalization, DS records, and signature operations."""

import base64
import hashlib
import time
from collections.abc import Iterable, Mapping
from contextlib import nullcontext
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from enum import IntEnum, IntFlag
from functools import partial
from struct import Struct

from cryptography.exceptions import InvalidSignature
from cryptography.exceptions import UnsupportedAlgorithm as UnsupportedCryptoAlgorithm
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

try:
    from cryptography.hazmat.primitives.asymmetric.mldsa import MLDSA44PublicKey
except ImportError:
    MLDSA44PublicKey = None

from tba_codec_dns.message import RRset as EditableRRset
from tba_codec_dns.rdata import Rdata, decoded, from_record, type_bitmap
from tba_codec_dns.rdataset import Rdataset
from tba_codec_dns.rdataset import from_records as dataset_from_records
from tba_codec_dns.rrset import RRset, from_rdataset
from tba_codec_dns.wire import RecordClass, RecordType, ResourceRecord, _name_wire
from tba_concrete_dns_zone.zone import Zone
from tba_primitives_dns_name.name import Name as DomainName
from tba_primitives_dns_name.name import from_text as parse_domain
from tba_primitives_dns_name.name import root
from tba_primitives_dns_name.names import (
    Name,
    is_subdomain,
    parse_name,
)

from .dnssecalgs import (
    GenericPrivateKey as GenericPrivateKey,
    GenericPublicKey as GenericPublicKey,
    get_algorithm_cls as get_algorithm_cls,
    get_algorithm_cls_from_dnskey as get_algorithm_cls_from_dnskey,
    register_algorithm_cls as register_algorithm_cls,
)
from .dnssecalgs._native import NativePublicKey

_SIG = Struct("!HBBIIIH")
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
    MLDSA44 = 18
    ECCGOST12 = 23
    INDIRECT = 252
    PRIVATEDNS = 253
    PRIVATEOID = 254


class DSDigest(IntEnum):
    NULL = 0
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
    sign_algorithms: frozenset[int] = frozenset({8, 10, 13, 14, 15, 16, 18})
    validate_algorithms: frozenset[int] = frozenset({5, 7, 8, 10, 13, 14, 15, 16, 18})
    create_ds_digests: frozenset[int] = frozenset({2, 4})
    validate_ds_digests: frozenset[int] = frozenset({1, 2, 4})

    def ok_to_sign(self, key: Rdata) -> bool:
        return key.algorithm in self.sign_algorithms

    def ok_to_validate(self, key: Rdata) -> bool:
        return key.algorithm in self.validate_algorithms

    def ok_to_create_ds(self, algorithm: int) -> bool:
        return algorithm in self.create_ds_digests

    def ok_to_validate_ds(self, algorithm: int) -> bool:
        return algorithm in self.validate_ds_digests


@dataclass(frozen=True, init=False)
class SimpleDeny(Policy):
    _denied_sign: frozenset
    _denied_validate: frozenset
    _denied_create_ds: frozenset
    _denied_validate_ds: frozenset

    def __init__(self, deny_sign, deny_validate, deny_create_ds, deny_validate_ds):
        object.__setattr__(self, "_denied_sign", frozenset(deny_sign))
        object.__setattr__(self, "_denied_validate", frozenset(deny_validate))
        object.__setattr__(self, "_denied_create_ds", frozenset(deny_create_ds))
        object.__setattr__(self, "_denied_validate_ds", frozenset(deny_validate_ds))

    def ok_to_sign(self, key: Rdata) -> bool:
        return key.algorithm not in self._denied_sign

    def ok_to_validate(self, key: Rdata) -> bool:
        return key.algorithm not in self._denied_validate

    def ok_to_create_ds(self, algorithm: int) -> bool:
        return algorithm not in self._denied_create_ds

    def ok_to_validate_ds(self, algorithm: int) -> bool:
        return algorithm not in self._denied_validate_ds


rfc_8624_policy = SimpleDeny(
    {Algorithm.RSAMD5, Algorithm.DSA, Algorithm.DSANSEC3SHA1, Algorithm.ECCGOST},
    {Algorithm.RSAMD5, Algorithm.DSA, Algorithm.DSANSEC3SHA1},
    {DSDigest.NULL, DSDigest.SHA1, DSDigest.GOST},
    {DSDigest.NULL},
)
rfc_9904_policy = rfc_8624_policy
allow_all_policy = SimpleDeny((), (), (), ())
default_policy = rfc_9904_policy
DEFAULT_POLICY = Policy()


def _canonical(name: Name) -> Name:
    return tuple(label.lower() for label in name)


def _absolute_owner(name, origin=None) -> Name:
    if isinstance(origin, str):
        origin = parse_domain(origin)
    if isinstance(name, str):
        name = parse_domain(name, origin=origin or root)
    if isinstance(name, DomainName):
        if not name.is_absolute() and origin is None:
            raise ValueError("relative DNSSEC name requires an origin")
        return name.derelativize(origin).labels[:-1]
    return name


def key_tag(key: ResourceRecord | Rdata) -> int:
    if isinstance(key, Rdata):
        key = key.record((), 0)
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


key_id = key_tag


class DeniedByPolicy(ValidationError):
    """The DNSSEC policy rejected the requested operation."""


def _digest_number(algorithm):
    if isinstance(algorithm, str):
        try:
            return DSDigest[algorithm.upper().replace("-", "")]
        except KeyError as exc:
            raise UnsupportedAlgorithm(f"unsupported DS digest {algorithm!r}") from exc
    return algorithm


def _ds_data(owner, key: Rdata, digest, policy, validating):
    digest = _digest_number(digest)
    if key.rdtype not in (RecordType.DNSKEY, RecordType.CDNSKEY):
        raise ValidationError("DS requires a DNSKEY or CDNSKEY")
    allowed = policy.ok_to_validate_ds if validating else policy.ok_to_create_ds
    if not allowed(digest):
        raise DeniedByPolicy(f"DS digest {digest} denied by policy")
    if digest not in _DIGESTS:
        raise UnsupportedAlgorithm(f"unsupported DS digest {digest}")
    value = hashlib.new(
        _DIGESTS[digest], _name_wire(_canonical(owner)) + key.to_wire()
    ).digest()
    return _DS.pack(key_tag(key), key.algorithm, digest) + value


def _make_ds_record(
    key: ResourceRecord,
    digest: int | str = 2,
    *,
    policy: Policy = DEFAULT_POLICY,
    validating: bool = False,
    cds: bool = False,
) -> ResourceRecord:
    value = from_record(key)
    if value.rdtype in (RecordType.DNSKEY, RecordType.CDNSKEY) and value.protocol != 3:
        raise ValidationError("DNSKEY protocol must be 3")
    data = _ds_data(key.name, value, digest, policy, validating)
    return ResourceRecord(
        key.name, RecordType.CDS if cds else RecordType.DS, key.rdclass, key.ttl, data
    )


def _make_ds_rdata(name, key, algorithm, origin=None, policy=None, validating=False):
    if not isinstance(key, Rdata):
        raise ValueError("DS requires detached DNSKEY or CDNSKEY RDATA")
    owner = _absolute_owner(name, origin)
    data = _ds_data(
        owner, key, algorithm, default_policy if policy is None else policy, validating
    )
    return from_record(ResourceRecord(owner, RecordType.DS, RecordClass.IN, 0, data))


def make_ds(*args, **kwargs) -> Rdata | ResourceRecord:
    """Construct DS RDATA from a DNS name, DNSKEY RDATA, and digest algorithm.

    The legacy form accepts a DNSKEY wire record and preserves its owner and TTL.
    """
    if (
        isinstance(args[0] if args else kwargs.get("key"), ResourceRecord)
        and "name" not in kwargs
    ):
        return _make_ds_record(*args, **kwargs)
    return _make_ds_rdata(*args, **kwargs)


def _integer(value: int) -> bytes:
    return value.to_bytes(max(1, (value.bit_length() + 7) // 8), "big")


class UnsupportedAlgorithm(ValidationError):
    """The DNSSEC key algorithm is unavailable."""


class AlgorithmKeyMismatch(UnsupportedAlgorithm):
    """The public key is incompatible with the requested DNSSEC algorithm."""


def _check_native_public_key(public_key):
    if not isinstance(
        public_key,
        (
            rsa.RSAPublicKey,
            dsa.DSAPublicKey,
            ec.EllipticCurvePublicKey,
            ed25519.Ed25519PublicKey,
            ed448.Ed448PublicKey,
        ),
    ) and not (
        MLDSA44PublicKey is not None and isinstance(public_key, MLDSA44PublicKey)
    ):
        raise TypeError("expected a DNSSEC public key")


def _native_dnskey_data(public_key, algorithm: int) -> bytes:
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
            raise AlgorithmKeyMismatch("DNSKEY curve does not match its algorithm")
        numbers = public_key.public_numbers()
        data = numbers.x.to_bytes(size, "big") + numbers.y.to_bytes(size, "big")
    elif algorithm in _ED and isinstance(public_key, _ED[algorithm][1]):
        data = public_key.public_bytes(
            serialization.Encoding.Raw, serialization.PublicFormat.Raw
        )
    elif (
        algorithm == Algorithm.MLDSA44
        and MLDSA44PublicKey is not None
        and isinstance(public_key, MLDSA44PublicKey)
    ):
        data = public_key.public_bytes_raw()
    else:
        raise AlgorithmKeyMismatch("public key does not match its DNSSEC algorithm")
    return data


def _make_key_rdata(
    public_key, algorithm: int | str, flags=Flag.ZONE, protocol=3
) -> Rdata:
    algorithm = algorithm_from_text(algorithm)
    if not isinstance(public_key, GenericPublicKey):
        cls = get_algorithm_cls(algorithm).public_cls
        if issubclass(cls, NativePublicKey):
            _check_native_public_key(public_key)
        public_key = cls(key=public_key)
    return public_key.to_dnskey(flags=flags, protocol=protocol)


def _make_key_record(
    owner: str | Name | DomainName,
    public_key,
    algorithm: int | str,
    *,
    flags=Flag.ZONE,
    ttl=3600,
    rdclass=RecordClass.IN,
    cdnskey=False,
) -> ResourceRecord:
    return ResourceRecord(
        _canonical(_absolute_owner(owner)),
        RecordType.CDNSKEY if cdnskey else RecordType.DNSKEY,
        rdclass,
        ttl,
        _make_key_rdata(public_key, algorithm, flags).to_wire(),
    )


def make_dnskey(*args, **kwargs) -> Rdata | ResourceRecord:
    """Convert (public_key, algorithm, flags=ZONE, protocol=3) to DNSKEY RDATA.

    The legacy (owner, public_key, algorithm) form returns a wire record.
    """
    if "owner" in kwargs or (args and isinstance(args[0], (str, tuple, DomainName))):
        return _make_key_record(*args, **kwargs)
    return _make_key_rdata(*args, **kwargs)


def make_cdnskey(*args, **kwargs) -> Rdata | ResourceRecord:
    """Convert public key material to CDNSKEY using the DNSKEY call forms."""
    key = make_dnskey(*args, **kwargs)
    if isinstance(key, ResourceRecord):
        return replace(key, type=RecordType.CDNSKEY)
    return from_record(replace(key.record(()), type=RecordType.CDNSKEY))


def make_cds(*args, **kwargs) -> Rdata | ResourceRecord:
    """Construct CDS using the same owner and digest conversion as DS."""
    value = make_ds(*args, **kwargs)
    if isinstance(value, ResourceRecord):
        return replace(value, type=RecordType.CDS)
    return from_record(replace(value.record(()), type=RecordType.CDS))


def _make_ds_rdataset_from_keys(
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


def _make_ds_rdataset_from_rrset(rrset, algorithms, origin=None) -> Rdataset:
    if isinstance(rrset, RRset):
        owner, dataset = rrset.name, rrset.to_rdataset()
        if origin is None and rrset.origin is not None:
            origin = rrset.origin
    elif isinstance(rrset, EditableRRset):
        owner, dataset = rrset.name, rrset
    else:
        owner, dataset = rrset
    if dataset.rdtype not in (RecordType.DNSKEY, RecordType.CDNSKEY, RecordType.CDS):
        raise ValueError("expected a DNSKEY, CDNSKEY, or CDS dataset")
    digests = dict.fromkeys(_digest_number(digest) for digest in algorithms)
    if dataset.rdtype == RecordType.CDS:
        result = Rdataset(dataset.rdclass, RecordType.DS, ttl=dataset.ttl)
        for value in cds_rdataset_to_ds_rdataset(dataset):
            if value.digest_type in digests:
                result.add(value)
        if not result:
            raise ValueError("no CDS records matched the requested digest algorithms")
        return result

    # The 2.9.2 RRset form yields CDS for DNSKEY and CDNSKEY inputs.
    result = Rdataset(RecordClass.IN, RecordType.CDS, ttl=dataset.ttl)
    for digest in digests:
        for key in dataset:
            result.add(make_cds(owner, key, digest, origin))
    if not result:
        raise ValueError("no DNSKEY records or digest algorithms")
    return result


def make_ds_rdataset(*args, **kwargs) -> Rdataset:
    """Build a delegation dataset from an RRset or the legacy owner/key form."""
    if "rrset" in kwargs or (
        args
        and (
            isinstance(args[0], (RRset, EditableRRset))
            or (
                isinstance(args[0], tuple)
                and len(args[0]) == 2
                and isinstance(args[0][1], Rdataset)
            )
        )
    ):
        return _make_ds_rdataset_from_rrset(*args, **kwargs)
    return _make_ds_rdataset_from_keys(*args, **kwargs)


def dnskey_rdataset_to_cds_rdataset(
    name: str | DomainName,
    rdataset: Rdataset,
    algorithm: DSDigest | str,
    origin: DomainName | None = None,
) -> Rdataset:
    """Derive a CDS dataset from a DNSKEY or CDNSKEY dataset."""
    if rdataset.rdtype not in (RecordType.DNSKEY, RecordType.CDNSKEY):
        raise ValueError("expected a DNSKEY or CDNSKEY dataset")
    return make_ds_rdataset(
        _absolute_owner(name, origin), rdataset, (algorithm,), cds=True
    )


def cds_rdataset_to_ds_rdataset(rdataset: Rdataset) -> Rdataset:
    if rdataset.rdtype != RecordType.CDS:
        raise ValueError("expected a CDS dataset")
    return _convert_dataset(rdataset, RecordType.DS)


def dnskey_rdataset_to_cdnskey_rdataset(rdataset: Rdataset) -> Rdataset:
    if rdataset.rdtype != RecordType.DNSKEY:
        raise ValueError("expected a DNSKEY dataset")
    return _convert_dataset(rdataset, RecordType.CDNSKEY)


def _convert_dataset(rdataset, rdtype):
    return Rdataset(
        rdataset.rdclass,
        rdtype,
        ttl=rdataset.ttl,
        values=(
            from_record(replace(value.record((), rdataset.ttl), type=rdtype))
            for value in rdataset
        ),
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
        if algorithm == Algorithm.MLDSA44 and MLDSA44PublicKey is not None:
            return MLDSA44PublicKey.from_public_bytes(data)
    except (ValueError, UnsupportedCryptoAlgorithm) as exc:
        raise ValidationError(
            "invalid or unsupported DNSKEY public-key encoding"
        ) from exc
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
    deterministic: bool = False,
    verify: bool = False,
) -> ResourceRecord:
    items = _rrset(records)
    first = items[0]
    if key.type != RecordType.DNSKEY or key.rdclass != first.rdclass:
        raise ValidationError("signing requires a matching DNSKEY")
    dnskey = from_record(key)
    flags, protocol, algorithm, _ = decoded(key)
    if protocol != 3 or not flags & Flag.ZONE or not policy.ok_to_sign(dnskey):
        raise DeniedByPolicy("DNSKEY is not permitted for signing")
    if not 0 < expiration - inception < 2**31:
        raise ValidationError("invalid DNSSEC signature validity period")
    if not isinstance(private_key, GenericPrivateKey):
        private_key = get_algorithm_cls_from_dnskey(dnskey)(key=private_key)
    if private_key.public_key().to_dnskey(flags, protocol).to_wire() != key.data:
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
    return replace(
        signature, data=unsigned + private_key.sign(payload, verify, deterministic)
    )


def _native_sign(private_key, payload, algorithm, data, deterministic):
    if algorithm in _RSA:
        raw = private_key.sign(payload, padding.PKCS1v15(), _RSA[algorithm]())
    elif algorithm in _DSA:
        r, s = utils.decode_dss_signature(private_key.sign(payload, hashes.SHA1()))
        raw = data[:1] + r.to_bytes(20, "big") + s.to_bytes(20, "big")
    elif algorithm in _EC:
        _, digest, size = _EC[algorithm]
        r, s = utils.decode_dss_signature(
            private_key.sign(
                payload, ec.ECDSA(digest(), deterministic_signing=deterministic)
            )
        )
        raw = r.to_bytes(size, "big") + s.to_bytes(size, "big")
    else:
        raw = private_key.sign(payload)
    return raw


def _native_verify(public_key, raw, payload, algorithm, data):
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


def _resource_records(rrset, origin):
    if isinstance(rrset, RRset):
        return rrset.records
    if isinstance(rrset, EditableRRset):
        return rrset.to_records(
            parse_domain(origin) if isinstance(origin, str) else origin
        )
    if isinstance(rrset, tuple) and len(rrset) == 2 and isinstance(rrset[1], Rdataset):
        return rrset[1].records(_absolute_owner(rrset[0], origin))
    return tuple(rrset)


def _signature_time(value):
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return int(value.timestamp())
    if isinstance(value, str) and len(value) == 14:
        parsed = datetime.strptime(value, "%Y%m%d%H%M%S")
        return int(parsed.replace(tzinfo=timezone.utc).timestamp())
    return int(value)


def sign(
    rrset,
    private_key,
    signer,
    dnskey,
    inception=None,
    expiration=None,
    lifetime=None,
    verify=False,
    policy=None,
    origin=None,
    deterministic=True,
):
    """Sign an owner-qualified RRset and return its typed RRSIG."""
    owner = _absolute_owner(signer, origin)
    key = dnskey.record(owner, 0) if isinstance(dnskey, Rdata) else dnskey
    if _canonical(key.name) != _canonical(owner):
        raise ValidationError("DNSKEY owner does not match the signer")
    start = int(time.time()) if inception is None else _signature_time(inception)
    if expiration is not None:
        end = _signature_time(expiration)
    elif lifetime is not None:
        end = start + lifetime
    else:
        raise ValueError("DNSSEC signing requires an expiration or lifetime")
    records = _resource_records(rrset, origin)
    policy = default_policy if policy is None else policy
    signature = sign_rrset(
        records,
        key,
        private_key,
        inception=start,
        expiration=end,
        policy=policy,
        deterministic=deterministic,
        verify=verify,
    )
    if verify:
        validate_rrsig(records, signature, (key,), now=start, policy=policy)
    return from_record(signature)


def _validation_keys(keys, signer, rdclass, origin):
    if not isinstance(keys, Mapping):
        return keys
    signer = _canonical(signer)
    for owner, node in keys.items():
        labels = _absolute_owner(owner, origin)
        if _canonical(labels) != signer:
            continue
        dataset = (
            node
            if isinstance(node, Rdataset)
            else node.get_rdataset(rdclass, RecordType.DNSKEY)
        )
        if dataset is not None:
            return dataset.records(labels)
    return ()


def validate_rrsig(
    rrset,
    rrsig,
    keys,
    origin=None,
    now: int | float | None = None,
    policy: Policy | None = None,
) -> None:
    items = _rrset(_resource_records(rrset, origin))
    signature = (
        rrsig.record(items[0].name, items[0].ttl) if isinstance(rrsig, Rdata) else rrsig
    )
    policy = default_policy if policy is None else policy
    if signature.type != RecordType.RRSIG:
        raise ValidationError("expected a DNS RRSIG record")
    _, algorithm, _, _, expiration, inception, tag, signer, raw = decoded(signature)
    current = int(time.time() if now is None else now)
    if not 0 < _seconds(inception, expiration) < 2**31 or _seconds(
        inception, current
    ) > _seconds(inception, expiration):
        raise ValidationError("DNSSEC signature outside its validity period")
    payload = _signature_data(items, signature)
    for key in _validation_keys(keys, signer, signature.rdclass, origin):
        if (
            key.type != RecordType.DNSKEY
            or key.rdclass != signature.rdclass
            or _canonical(key.name) != _canonical(signer)
        ):
            continue
        dnskey = from_record(key)
        flags, protocol, key_algorithm, _ = decoded(key)
        if (
            protocol != 3
            or not flags & Flag.ZONE
            or (flags & Flag.REVOKE and items[0].type != RecordType.DNSKEY)
            or key_algorithm != algorithm
            or key_tag(key) != tag
            or not policy.ok_to_validate(dnskey)
        ):
            continue
        try:
            public_cls = get_algorithm_cls_from_dnskey(dnskey).public_cls
            public_cls.from_dnskey(dnskey).verify(raw, payload)
            return
        except (InvalidSignature, ValueError):
            continue
    raise ValidationError("no DNSKEY validated the RRSIG")


def validate(
    rrset,
    rrsigset,
    keys,
    origin=None,
    now: int | float | None = None,
    policy: Policy | None = None,
) -> None:
    items = _resource_records(rrset, origin)
    candidates = keys if isinstance(keys, Mapping) else tuple(keys)
    for signature in _resource_records(rrsigset, origin):
        try:
            validate_rrsig(items, signature, candidates, origin, now, policy)
            return
        except ValueError:
            continue
    raise ValidationError("no valid DNSSEC RRSIG for RRset")


def nsec3_hash(
    name: str | Name | DomainName,
    salt: str | bytes | None,
    iterations: int,
    algorithm: int | str = 1,
) -> str:
    if isinstance(algorithm, str) and algorithm.upper() == "SHA1":
        algorithm = 1
    if algorithm != 1 or not 0 <= iterations <= 65535:
        raise ValueError("unsupported NSEC3 hash algorithm or iteration count")
    owner = _canonical(_absolute_owner(name))
    if salt is None:
        salt = b""
    elif isinstance(salt, str):
        salt = b"" if salt == "-" else bytes.fromhex(salt)
    if len(salt) > 255:
        raise ValueError("NSEC3 salt is longer than 255 octets")
    digest = hashlib.sha1(_name_wire(owner) + salt).digest()
    for _ in range(iterations):
        digest = hashlib.sha1(digest + salt).digest()
    return base64.b32hexencode(digest).decode().rstrip("=")


def default_rrset_signer(
    txn,
    rrset,
    signer,
    ksks,
    zsks,
    inception=None,
    expiration=None,
    lifetime=None,
    policy=None,
    origin=None,
    deterministic=True,
):
    """Add signatures for an RRset using the keys assigned to its record type."""
    keys = (
        ksks
        if rrset.rdtype in (RecordType.DNSKEY, RecordType.CDS, RecordType.CDNSKEY)
        else zsks
    )
    for private_key, dnskey in keys:
        signature = sign(
            rrset,
            private_key,
            signer,
            dnskey,
            inception=inception,
            expiration=expiration,
            lifetime=lifetime,
            policy=policy,
            origin=origin,
            deterministic=deterministic,
        )
        txn.add(rrset.name, rrset.ttl, signature)


def sign_zone(
    zone: Zone,
    txn=None,
    keys=None,
    add_dnskey=True,
    dnskey_ttl=None,
    inception=None,
    expiration=None,
    lifetime=None,
    nsec3=None,
    rrset_signer=None,
    policy=None,
    deterministic=True,
) -> None:
    """Sign the zone in place or stage signatures in a caller-owned writer."""
    if nsec3 is not None:
        raise NotImplementedError("zone signing with NSEC3 is unsupported")
    origin, relativize, apex = zone.origin_information()
    if origin is None:
        raise ValueError("zone signing requires an origin")
    keypairs = []
    for private_key, dnskey in keys or ():
        if isinstance(dnskey, ResourceRecord):
            if _canonical(dnskey.name) != _canonical(origin.labels[:-1]):
                raise ValidationError("zone signing requires apex DNSKEYs")
            dnskey = from_record(dnskey)
        if (dnskey.rdclass, dnskey.rdtype) != (zone.get_class(), RecordType.DNSKEY):
            raise ValidationError("zone signing requires DNSKEYs of the zone class")
        keypairs.append((private_key, dnskey))

    if rrset_signer is None:
        ksks = [pair for pair in keypairs if pair[1].flags & Flag.SEP]
        zsks = [pair for pair in keypairs if not pair[1].flags & Flag.SEP]
        rrset_signer = partial(
            default_rrset_signer,
            signer=origin,
            ksks=ksks or keypairs,
            zsks=zsks or keypairs,
            inception=inception,
            expiration=expiration,
            lifetime=lifetime,
            policy=policy,
            origin=origin,
            deterministic=deterministic,
        )

    with zone.writer() if txn is None else nullcontext(txn) as change:
        soa = change.get(apex, RecordType.SOA)
        if soa is None or len(soa) != 1:
            raise ValueError("zone signing requires one apex SOA")
        if add_dnskey and keypairs:
            if dnskey_ttl is None:
                existing_keys = change.get(apex, RecordType.DNSKEY)
                dnskey_ttl = existing_keys.ttl if existing_keys else soa.ttl
            change.add(apex, dnskey_ttl, *(key for _, key in keypairs))
        _sign_nsec_chain(
            change,
            origin,
            origin if relativize else None,
            soa[0].minimum,
            zone.get_class(),
            rrset_signer,
        )


def _sign_nsec_chain(txn, origin, display_origin, ttl, rdclass, signer):
    """Sign authoritative data and emit an NSEC chain in canonical name order."""

    def add_nsec(owner, successor):
        node = txn.get_node(owner)
        types = {dataset.rdtype for dataset in node}
        types.update((RecordType.NSEC, RecordType.RRSIG))
        record = ResourceRecord(
            owner.labels[:-1],
            RecordType.NSEC,
            rdclass,
            ttl,
            _name_wire(successor.labels[:-1]) + type_bitmap(tuple(types)),
        )
        value = from_record(record)
        txn.replace(owner, ttl, value)
        signer(
            txn,
            RRset(record.name, rdclass, record.type, ttl, (record,), display_origin),
        )

    previous = delegation = None
    for owner in tuple(txn.iterate_names()):
        owner = owner.derelativize(origin)
        if delegation is not None and owner.is_subdomain(delegation):
            continue
        delegation = (
            owner if owner != origin and txn.get(owner, RecordType.NS) else None
        )
        for dataset in txn.get_node(owner):
            if dataset.rdtype in (RecordType.RRSIG, RecordType.NSEC, RecordType.NSEC3):
                continue
            if delegation is None or dataset.rdtype == RecordType.DS:
                rrset = from_rdataset(owner, dataset)
                signer(txn, replace(rrset, origin=display_origin))
        if previous is not None:
            add_nsec(previous, owner)
        previous = owner
    if previous is not None:
        add_nsec(previous, origin)
