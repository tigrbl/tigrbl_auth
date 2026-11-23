"""Secret-key DNS transaction authentication (RFC 8945)."""

import base64
import hmac
import time
from collections.abc import Mapping
from dataclasses import dataclass, replace
from struct import Struct
from typing import ClassVar, Protocol

from tba_primitives_dns_name.name import Name as DomainName
from tba_primitives_dns_name.names import Name, parse_name

from .wire import (
    Message,
    RecordClass,
    RecordType,
    ResourceRecord,
    UnknownTSIGKey,
    WireError,
    _name_wire,
    _read_name,
)

_H = Struct("!H")
_VARIABLES = Struct("!HI")
_ALGORITHMS = {
    "hmac-md5.sig-alg.reg.int.": "md5",
    "hmac-sha1.": "sha1",
    "hmac-sha224.": "sha224",
    "hmac-sha256.": "sha256",
    "hmac-sha384.": "sha384",
    "hmac-sha512.": "sha512",
    "hmac-sha256-128.": "sha256",
    "hmac-sha384-192.": "sha384",
    "hmac-sha512-256.": "sha512",
}


class TsigError(WireError):
    """The DNS message failed TSIG authentication."""


@dataclass(frozen=True, repr=False)
class TsigKey:
    name: Name
    secret: bytes
    algorithm: Name = (b"hmac-sha256",)

    @classmethod
    def from_text(
        cls, name: str, secret: str, algorithm: str = "hmac-sha256."
    ) -> "TsigKey":
        return cls(
            parse_name(name, canonical=True),
            base64.b64decode(secret, validate=True),
            parse_name(algorithm, canonical=True),
        )

    def __post_init__(self) -> None:
        if not self.name or not self.secret or self.algorithm not in _DIGESTS:
            raise ValueError("invalid TSIG key name, secret, or algorithm")
        object.__setattr__(self, "name", tuple(label.lower() for label in self.name))


_DIGESTS = {parse_name(name): digest for name, digest in _ALGORITHMS.items()}
_FIXED_SIZES = {
    (b"hmac-sha256-128",): 16,
    (b"hmac-sha384-192",): 24,
    (b"hmac-sha512-256",): 32,
}


class GssContext(Protocol):
    def get_signature(self, message: bytes) -> bytes: ...
    def verify_signature(self, message: bytes, signature: bytes) -> int: ...


@dataclass(frozen=True, repr=False)
class GssTsigKey:
    """RFC 3645 TSIG using an established caller-supplied GSS context."""

    name: Name
    context: GssContext
    algorithm: ClassVar[Name] = (b"gss-tsig",)

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("invalid GSS-TSIG key name")
        object.__setattr__(self, "name", tuple(label.lower() for label in self.name))


AuthKey = TsigKey | GssTsigKey


@dataclass(frozen=True)
class TsigRecord:
    algorithm: Name
    time_signed: int
    fudge: int
    mac: bytes
    original_id: int
    error: int = 0
    other: bytes = b""

    def timers(self) -> bytes:
        return self.time_signed.to_bytes(6, "big") + _H.pack(self.fudge)

    def trailer(self) -> bytes:
        return _H.pack(self.error) + _H.pack(len(self.other)) + self.other

    def data(self) -> bytes:
        return (
            _name_wire(self.algorithm)
            + self.timers()
            + _H.pack(len(self.mac))
            + self.mac
            + _H.pack(self.original_id)
            + self.trailer()
        )

    @classmethod
    def from_data(cls, data: bytes) -> "TsigRecord":
        algorithm, offset = _read_name(data, 0, compress=False)
        if offset + 16 > len(data):
            raise TsigError("truncated TSIG record")
        now = int.from_bytes(data[offset : offset + 6], "big")
        fudge = _H.unpack_from(data, offset + 6)[0]
        size = _H.unpack_from(data, offset + 8)[0]
        start, end = offset + 10, offset + 10 + size
        if end + 6 > len(data):
            raise TsigError("truncated TSIG MAC")
        ident, error, other_size = Struct("!3H").unpack_from(data, end)
        if end + 6 + other_size != len(data):
            raise TsigError("invalid TSIG other-data length")
        return cls(
            algorithm, now, fudge, data[start:end], ident, error, data[end + 6 :]
        )


def _prior(mac: bytes | None) -> bytes:
    return b"" if mac is None else _H.pack(len(mac)) + mac


def _variables(key: AuthKey, signature: TsigRecord) -> bytes:
    return (
        _name_wire(key.name)
        + _VARIABLES.pack(RecordClass.ANY, 0)
        + _name_wire(signature.algorithm)
        + signature.timers()
        + signature.trailer()
    )


def _signed_bytes(unsigned: bytes, original_id: int) -> bytes:
    return _H.pack(original_id) + unsigned[2:]


def _strip(packet: bytes, key: AuthKey) -> tuple[bytes, TsigRecord]:
    message = Message.from_wire(packet)
    signatures = tuple(rr for rr in message.additional if rr.type == RecordType.TSIG)
    if len(signatures) != 1 or message.additional[-1] is not signatures[0]:
        raise TsigError("DNS message requires a single final TSIG record")
    record = signatures[0]
    if record.name != key.name or record.rdclass != RecordClass.ANY or record.ttl != 0:
        raise TsigError("unexpected TSIG owner, class, or TTL")
    offset = record._start
    if (
        offset < 12
        or _read_name(packet, offset, compress=False)[1] != record._offset - 10
    ):
        raise TsigError("invalid TSIG owner encoding")
    unsigned = packet[:10] + _H.pack(len(message.additional) - 1) + packet[12:offset]
    return unsigned, TsigRecord.from_data(record.data)


def _check_hmac(key: TsigKey, signed: TsigRecord, digest: bytes) -> None:
    size = _FIXED_SIZES.get(key.algorithm)
    if (size is not None and len(signed.mac) != size) or not max(
        10, len(digest) // 2
    ) <= len(signed.mac) <= len(digest):
        raise TsigError("invalid TSIG digest length")
    if not hmac.compare_digest(signed.mac, digest[: len(signed.mac)]):
        raise TsigError("TSIG digest verification failed")


def _check_metadata(key: AuthKey, signed: TsigRecord, now: int) -> None:
    if signed.algorithm != key.algorithm:
        raise TsigError("unexpected TSIG algorithm")
    if abs(now - signed.time_signed) > signed.fudge:
        raise TsigError("TSIG time outside the signing window")
    if signed.error:
        raise TsigError(f"server returned TSIG error {signed.error}")


def _check_gss(key: GssTsigKey, signature: TsigRecord, payload: bytes) -> None:
    try:
        key.context.verify_signature(payload, signature.mac)
    except Exception as exc:
        raise TsigError("GSS-TSIG signature verification failed") from exc


def sign(
    packet: bytes,
    key: AuthKey,
    *,
    request_mac: bytes | None = None,
    now: int | None = None,
    fudge: int = 300,
    original_id: int | None = None,
    error: int = 0,
    other: bytes = b"",
    context=None,
) -> tuple[bytes, bytes]:
    message = Message.from_wire(packet)
    if any(rr.type == RecordType.TSIG for rr in message.additional):
        raise ValueError("DNS message is already TSIG signed")
    now = int(time.time()) if now is None else now
    identifier = message.id if original_id is None else original_id
    if not 0 <= now < 2**48 or not all(
        0 <= value <= 65535 for value in (fudge, identifier, error, len(other))
    ):
        raise ValueError("TSIG metadata outside its wire range")
    unsigned = TsigRecord(key.algorithm, now, fudge, b"", identifier, error, other)
    payload = (
        _prior(request_mac)
        + _signed_bytes(packet, identifier)
        + _variables(key, unsigned)
    )
    if context is not None:
        if not isinstance(context, StreamSigner) or context.key != key:
            raise ValueError("TSIG signing context belongs to a different key")
        mac = context.mac(packet, unsigned, payload)
    elif isinstance(key, GssTsigKey):
        mac = key.context.get_signature(payload)
    else:
        mac = hmac.digest(key.secret, payload, _DIGESTS[key.algorithm])
        mac = mac[: _FIXED_SIZES.get(key.algorithm)]
    signature = replace(unsigned, mac=mac)
    rr = ResourceRecord(key.name, RecordType.TSIG, RecordClass.ANY, 0, signature.data())
    signed = (
        packet[:10] + _H.pack(len(message.additional) + 1) + packet[12:] + rr.to_wire()
    )
    if len(signed) > 65535:
        raise ValueError("TSIG signed message exceeds DNS size limit")
    if context is not None:
        context.previous_mac = mac
    return signed, mac


def verify(
    packet: bytes,
    key: AuthKey,
    *,
    request_mac: bytes | None = None,
    now: int | None = None,
) -> TsigRecord:
    unsigned, signature = _strip(packet, key)
    payload = (
        _prior(request_mac)
        + _signed_bytes(unsigned, signature.original_id)
        + _variables(key, signature)
    )
    _check_metadata(key, signature, int(time.time()) if now is None else now)
    if isinstance(key, GssTsigKey):
        _check_gss(key, signature, payload)
    else:
        _check_hmac(
            key, signature, hmac.digest(key.secret, payload, _DIGESTS[key.algorithm])
        )
    return signature


class StreamSigner:
    """Carry the previous signature across consecutively signed DNS messages."""

    def __init__(self, key: AuthKey):
        self.key = key
        self.previous_mac: bytes | None = None

    def mac(self, packet: bytes, record: TsigRecord, first_payload: bytes) -> bytes:
        payload = first_payload
        if self.previous_mac is not None:
            payload = (
                _prior(self.previous_mac)
                + _signed_bytes(packet, record.original_id)
                + record.timers()
            )
        if isinstance(self.key, GssTsigKey):
            return self.key.context.get_signature(payload)
        digest = hmac.digest(self.key.secret, payload, _DIGESTS[self.key.algorithm])
        return digest[: _FIXED_SIZES.get(self.key.algorithm)]


class StreamVerifier:
    """Validate response TSIG chaining across a DNS zone-transfer stream."""

    def __init__(self, key: AuthKey, request_mac: bytes | None) -> None:
        self._key = key
        self._request_mac = request_mac
        self._mac: hmac.HMAC | None = None
        self._gss: bytearray | None = None
        self._unsigned = 0

    def verify(self, packet: bytes, *, last: bool = False) -> None:
        message = Message.from_wire(packet)
        signed = any(rr.type == RecordType.TSIG for rr in message.additional)
        if self._mac is None and self._gss is None:
            signature = verify(packet, self._key, request_mac=self._request_mac)
        elif isinstance(self._key, GssTsigKey):
            if signed:
                unsigned, signature = _strip(packet, self._key)
                self._gss.extend(
                    _signed_bytes(unsigned, signature.original_id) + signature.timers()
                )
                _check_metadata(self._key, signature, int(time.time()))
                _check_gss(self._key, signature, bytes(self._gss))
            else:
                self._require_signature(last)
                self._gss.extend(packet)
                return
        elif signed:
            unsigned, signature = _strip(packet, self._key)
            self._mac.update(_signed_bytes(unsigned, signature.original_id))
            self._mac.update(signature.timers())
            _check_metadata(self._key, signature, int(time.time()))
            _check_hmac(self._key, signature, self._mac.digest())
        else:
            self._require_signature(last)
            self._mac.update(packet)
            return
        if isinstance(self._key, GssTsigKey):
            self._gss = bytearray(_prior(signature.mac))
        else:
            self._mac = hmac.new(
                self._key.secret, _prior(signature.mac), _DIGESTS[self._key.algorithm]
            )
        self._unsigned = 0

    def _require_signature(self, last: bool) -> None:
        self._unsigned += 1
        if last or self._unsigned >= 100:
            raise TsigError("missing required TSIG on DNS transfer response")


def _key_labels(name) -> Name:
    if isinstance(name, DomainName):
        if not name.is_absolute():
            raise ValueError("TSIG key name must be absolute")
        return tuple(label.lower() for label in name.labels[:-1])
    if isinstance(name, str):
        return parse_name(name, canonical=True)
    return tuple(label.lower() for label in name)


def _lookup_key(keyring: Mapping, labels: Name):
    name = DomainName((*labels, b""))
    return keyring.get(name) or keyring.get(labels) or keyring.get(name.to_text())


def signing_key(keyring, keyname, algorithm) -> AuthKey:
    if isinstance(keyring, (TsigKey, GssTsigKey)):
        if keyname is not None and _key_labels(keyname) != keyring.name:
            raise UnknownTSIGKey("TSIG key name does not match the supplied key")
        return keyring
    if not isinstance(keyring, Mapping):
        raise TypeError("expected a DNS TSIG key or keyring")
    if keyname is None:
        if len(keyring) != 1:
            raise UnknownTSIGKey("select a TSIG key name for signing")
        name, value = next(iter(keyring.items()))
        labels = _key_labels(name)
    else:
        labels = _key_labels(keyname)
        value = _lookup_key(keyring, labels)
    if isinstance(value, bytes):
        return TsigKey(labels, value, _key_labels(algorithm))
    if isinstance(value, (TsigKey, GssTsigKey)) and value.name == labels:
        return value
    raise UnknownTSIGKey("no matching TSIG key for signing")


def authenticate_message(message: Message, keyring, *, multi: bool, context) -> Message:
    if context is not None:
        if not multi or not isinstance(context, StreamVerifier):
            raise TypeError(
                "TSIG context requires multi-message parsing and a StreamVerifier"
            )
        context.verify(message.wire)
        return replace(message, tsig_ctx=context, tsig_key=context._key)
    if not message.had_tsig:
        if message.request_mac and not multi:
            raise TsigError("missing response TSIG for the signed request")
        if multi and isinstance(keyring, (TsigKey, GssTsigKey)):
            raise TsigError("the first DNS stream message requires TSIG")
        return message
    record = message.additional[-1]
    key = keyring
    if isinstance(keyring, Mapping):
        key = _lookup_key(keyring, record.name)
        if isinstance(key, bytes):
            try:
                key = TsigKey(
                    record.name, key, TsigRecord.from_data(record.data).algorithm
                )
            except ValueError as exc:
                raise UnknownTSIGKey("invalid TSIG key for the DNS message") from exc
    elif callable(keyring):
        key = keyring(message, DomainName((*record.name, b"")))
    if not isinstance(key, (TsigKey, GssTsigKey)):
        raise UnknownTSIGKey("no TSIG key for the DNS message")
    if multi:
        context = StreamVerifier(key, message.request_mac or None)
        context.verify(message.wire)
    else:
        verify(message.wire, key, request_mac=message.request_mac or None)
    return replace(message, tsig_key=key, tsig_ctx=context)
