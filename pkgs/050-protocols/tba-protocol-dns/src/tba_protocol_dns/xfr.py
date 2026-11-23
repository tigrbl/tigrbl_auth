"""AXFR and IXFR zone transfers (RFC 5936 and RFC 1995)."""

import secrets
import socket
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass, replace
from time import monotonic, time

from tba_codec_dns import message as editable_message
from tba_codec_dns.rdata import decoded, from_record, from_text as parse_rdata
from tba_codec_dns.tsig import AuthKey, StreamVerifier, sign
from tba_codec_dns.wire import (
    Message,
    Question,
    RecordClass,
    RecordType,
    ResourceRecord,
    Truncated,
    WireError,
    record_class,
    record_type,
)
from tba_concrete_dns_zone.zone import Zone
from tba_primitives_dns_name.name import Name as DomainName
from tba_primitives_dns_name.name import from_text as domain_from_text
from tba_primitives_dns_name.names import Name, is_subdomain, parse_name
from tba_provider_dns_resolver import asyncquery, query as syncquery
from tba_provider_dns_resolver.async_transport import run_blocking
from tba_provider_dns_resolver.asyncbackend import get_default_backend
from tba_provider_dns_resolver.transport import (
    check_response,
    deadline_after,
    exchange_udp_packet,
    remaining,
    stream,
)


def _serial(record: ResourceRecord) -> int:
    return decoded(record)[2]


def _same_soa(left: ResourceRecord, right: ResourceRecord) -> bool:
    return (
        right.type == RecordType.SOA
        and left.name == right.name
        and left.rdclass == right.rdclass
        and left.uncompressed_data(canonical=True)
        == right.uncompressed_data(canonical=True)
    )


def _newer(candidate: int, baseline: int) -> bool:
    return 0 < (candidate - baseline) % 2**32 < 2**31


@dataclass(frozen=True)
class Delta:
    previous: ResourceRecord
    deleted: tuple[ResourceRecord, ...]
    current: ResourceRecord
    added: tuple[ResourceRecord, ...]


@dataclass(frozen=True)
class Transfer:
    origin: Name
    rdclass: int
    soa: ResourceRecord
    snapshot: tuple[ResourceRecord, ...] | None = None
    deltas: tuple[Delta, ...] = ()

    def apply(self, base: Zone | None = None) -> Zone:
        if self.snapshot is not None:
            zone = Zone(self.origin, rdclass=self.rdclass)
        else:
            if base is None:
                raise ValueError("IXFR requires the matching local zone")
            zone = Zone(base.origin, base.records(), rdclass=base.rdclass)
        self.apply_to(zone)
        return zone

    def apply_to(self, zone: Zone, *, transaction_setup=None) -> None:
        """Commit a complete transfer atomically to an existing zone."""
        origin, _, _ = zone.origin_information()
        if (origin.labels[:-1], zone.get_class()) != (self.origin, self.rdclass):
            raise ValueError("DNS transfer requires the matching local zone")
        with zone.writer(replacement=self.snapshot is not None) as txn:
            if transaction_setup is not None:
                transaction_setup(txn)
            if self.snapshot is not None:
                for rr in self.snapshot:
                    txn.add(rr.name, rr.ttl, from_record(rr))
                txn.check_origin()
                return
            apex = txn.get(self.origin, RecordType.SOA)
            expected = self.deltas[0].previous if self.deltas else self.soa
            if (
                apex is None
                or len(apex) != 1
                or not _same_soa(apex[0].record(self.origin, apex.ttl), expected)
            ):
                raise ValueError("local zone SOA does not match the IXFR baseline")
            for delta in self.deltas:
                txn.delete(self.origin, RecordType.SOA)
                for rr in delta.deleted:
                    txn.delete_exact(rr.name, from_record(rr))
                txn.add(
                    delta.current.name, delta.current.ttl, from_record(delta.current)
                )
                for rr in delta.added:
                    txn.add(rr.name, rr.ttl, from_record(rr))
            txn.check_origin()
            if not txn.changed():
                txn.rollback()


def _deltas(records: list[ResourceRecord], serial: int) -> tuple[Delta, ...]:
    opening, closing = records[0], records[-1]
    milestones = [
        i for i in range(1, len(records) - 1) if records[i].type == RecordType.SOA
    ]
    if not milestones or len(milestones) % 2 or not _same_soa(opening, closing):
        raise WireError("invalid IXFR delta structure")
    milestones.append(len(records) - 1)
    output = []
    for old_index, new_index, next_index in zip(
        milestones[::2], milestones[1::2], milestones[2::2]
    ):
        previous, current = records[old_index], records[new_index]
        if _serial(previous) != serial or not _newer(_serial(current), serial):
            raise WireError("IXFR serial sequence is invalid")
        if output and not _same_soa(output[-1].current, previous):
            raise WireError("IXFR delta SOAs disagree")
        output.append(
            Delta(
                previous,
                tuple(records[old_index + 1 : new_index]),
                current,
                tuple(records[new_index + 1 : next_index]),
            )
        )
        serial = _serial(current)
    if not _same_soa(output[-1].current, opening):
        raise WireError("IXFR did not reach the advertised serial")
    return tuple(output)


@contextmanager
def _frames(
    query: Message,
    packet: bytes,
    server: str,
    port: int,
    deadline: float,
    udp_serial: int | None,
) -> Iterator[Iterator[bytes]]:
    if udp_serial is not None:
        try:
            udp_deadline = monotonic() + min(2, remaining(deadline) / 2)
            answer = exchange_udp_packet(
                query, packet, server, port, udp_deadline, None
            )
        except OSError:
            answer = None
        if answer is not None and not answer[2] & 2:
            response = Message.from_wire(answer)
            if (
                len(response.answers) != 1
                or response.answers[0].type != RecordType.SOA
                or _serial(response.answers[0]) == udp_serial
            ):
                yield iter((answer,))
                return
    with stream(server, port, deadline) as connection:
        connection.send(packet)

        def frames():
            while True:
                yield connection.receive()

        yield frames()


def transfer(
    origin: str,
    server: str,
    *,
    port: int = 53,
    timeout: float = 10,
    rdclass: int | str = RecordClass.IN,
    base_soa: ResourceRecord | None = None,
    key: AuthKey | None = None,
    max_records: int = 1000000,
    try_udp: bool = False,
) -> Transfer:
    if max_records <= 0:
        raise ValueError("DNS transfer requires a positive record limit")
    if try_udp and base_soa is None:
        raise ValueError("UDP transfer requires an IXFR baseline")
    owner = parse_name(origin, canonical=True)
    class_number = record_class(rdclass)
    serial = None
    if base_soa is not None:
        if (base_soa.name, base_soa.rdclass, base_soa.type) != (
            owner,
            class_number,
            RecordType.SOA,
        ):
            raise ValueError("IXFR baseline must be the matching apex SOA")
        serial = _serial(base_soa)
    query = Message(
        secrets.randbits(16),
        0,
        (
            Question(
                owner,
                RecordType.AXFR if serial is None else RecordType.IXFR,
                class_number,
            ),
        ),
        authority=() if base_soa is None else (base_soa,),
    )
    packet = query.to_wire()
    verifier = None
    if key is not None:
        packet, mac = sign(packet, key)
        verifier = StreamVerifier(key, mac)
    decoder = _transfer_decoder(query, serial, verifier, max_records)
    next(decoder)
    with _frames(
        query,
        packet,
        server,
        port,
        deadline_after(timeout),
        serial if try_udp else None,
    ) as packets:
        for response_packet in packets:
            try:
                decoder.send(response_packet)
            except StopIteration as finished:
                return finished.value
    raise WireError("DNS transfer ended before its closing SOA")


class TransferError(WireError):
    """The primary returned an unsuccessful DNS response code."""

    def __init__(self, rcode):
        super().__init__(f"DNS transfer failed with rcode {rcode}")
        self.rcode = rcode


class SerialWentBackwards(WireError):
    """A primary advertised a serial older than the local zone."""


class UseTCP(WireError):
    """A UDP response cannot complete this IXFR."""


def _transfer_decoder(
    query,
    serial,
    verifier,
    max_records,
    raise_on_serial_went_backwards=True,
    *,
    parsed=False,
):
    owner, class_number = query.questions[0].name, query.questions[0].rdclass
    records = []
    opening = None
    incremental = signed = False
    soa_count = 0
    while True:
        response_packet = yield
        response = response_packet if parsed else Message.from_wire(response_packet)
        if parsed:
            if response.questions and response.questions != query.questions:
                raise WireError("unexpected DNS transfer question")
        else:
            check_response(query, response, allow_empty_question=bool(records))
        if response.rcode:
            raise TransferError(response.rcode)
        if not response.answers or (not parsed and not response.flags & 0x0400):
            raise WireError("invalid DNS transfer response")
        if parsed and not records:
            signed = bool(response.request_mac)
            if signed and not response.had_tsig:
                raise WireError("missing TSIG on first transfer response")
        completed = False
        for rr in response.answers:
            if completed or len(records) >= max_records:
                raise WireError("excess records in DNS transfer")
            if not is_subdomain(rr.name, owner) and parsed and records:
                continue
            if rr.rdclass != class_number or not is_subdomain(rr.name, owner):
                raise WireError("record is outside the transferred zone")
            if rr.type == RecordType.SOA:
                if rr.name != owner:
                    raise WireError("transfer SOA is outside the apex")
                soa_count += 1
            if not records:
                if rr.type != RecordType.SOA:
                    raise WireError("DNS transfer requires an opening SOA")
                opening = rr
            elif len(records) == 1 and serial is not None:
                incremental = rr.type == RecordType.SOA and not _same_soa(opening, rr)
            if len(records) and _same_soa(opening, rr):
                completed = not incremental or (soa_count >= 4 and soa_count % 2 == 0)
            records.append(rr)
        same_serial = serial is not None and _serial(opening) == serial
        older_serial = serial is not None and _newer(serial, _serial(opening))
        if parsed and (completed or same_serial or older_serial):
            if (signed or response.request_mac) and not response.had_tsig:
                raise WireError("missing TSIG on last transfer response")
            if (same_serial or older_serial) and len(records) != 1:
                raise WireError("unexpected records after the current SOA")
        if older_serial:
            if verifier is not None:
                verifier.verify(response_packet, last=True)
            if raise_on_serial_went_backwards:
                raise SerialWentBackwards(
                    "primary zone serial is older than the local serial"
                )
            return Transfer(owner, class_number, opening)
        unchanged = len(records) == 1 and same_serial
        if verifier is not None:
            verifier.verify(response_packet, last=completed or unchanged)
        if unchanged:
            return Transfer(owner, class_number, opening)
        if completed:
            if incremental:
                return Transfer(
                    owner, class_number, opening, deltas=_deltas(records, serial)
                )
            if soa_count != 2:
                raise WireError("full DNS transfer contains interior SOA records")
            return Transfer(owner, class_number, opening, snapshot=tuple(records[:-1]))


class Inbound:
    """Apply one complete AXFR or IXFR to a transaction manager."""

    def __init__(
        self,
        txn_manager,
        rdtype=RecordType.AXFR,
        serial=None,
        is_udp=False,
        raise_on_serial_went_backwards=True,
        transaction_setup=None,
    ):
        if rdtype not in (RecordType.AXFR, RecordType.IXFR):
            raise ValueError("expected AXFR or IXFR")
        if rdtype == RecordType.IXFR and serial is None:
            raise ValueError("IXFR requires an initial serial")
        if rdtype == RecordType.AXFR and (serial is not None or is_udp):
            raise ValueError("AXFR requires TCP and no initial serial")
        origin, _, _ = txn_manager.origin_information()
        if origin is None:
            raise ValueError("transfer requires a zone origin")
        self.txn_manager = txn_manager
        self.transaction_setup = transaction_setup
        self.is_udp = is_udp
        self.done = False
        self._serial = serial
        self._closed = False
        query = Message(
            0, 0, (Question(origin.labels[:-1], rdtype, txn_manager.get_class()),)
        )
        self._decoder = _transfer_decoder(
            query,
            serial,
            None,
            1000000,
            raise_on_serial_went_backwards,
            parsed=True,
        )
        next(self._decoder)

    def process_message(self, message):
        """Consume a parsed frame and commit once its closing SOA arrives."""
        if self._closed:
            raise WireError("DNS transfer is already closed")
        if isinstance(message, editable_message.Message):
            message = message._wire_message()
        try:
            self._decoder.send(message)
        except StopIteration as finished:
            self._closed = True
            result = finished.value
            if self._serial is None or _newer(_serial(result.soa), self._serial):
                result.apply_to(
                    self.txn_manager, transaction_setup=self.transaction_setup
                )
            self.done = True
        except BaseException:
            self._closed = True
            raise
        if self.is_udp and not self.done:
            self.__exit__(None, None, None)
            if len(message.answers) == 1:
                raise UseTCP("IXFR requires TCP")
            raise WireError("incomplete UDP IXFR")
        return self.done

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._closed = True
        self._decoder.close()


def make_query(
    txn_manager,
    serial=0,
    use_edns=None,
    ednsflags=None,
    payload=None,
    request_payload=None,
    options=None,
    keyring=None,
    keyname=None,
    keyalgorithm="hmac-sha256.",
):
    """Build a zone transfer request and return its requested serial."""
    origin, _, effective_origin = txn_manager.origin_information()
    if origin is None:
        raise ValueError("transfer requires a zone origin")
    if serial is not None and (not isinstance(serial, int) or not 0 <= serial < 2**32):
        raise ValueError("invalid IXFR serial")
    if serial == 0:
        with txn_manager.reader() as reader:
            soa = reader.get(effective_origin, RecordType.SOA)
            serial = soa[0].serial if soa else None
    rdclass = txn_manager.get_class()
    query = editable_message.make_query(
        origin,
        RecordType.AXFR if serial is None else RecordType.IXFR,
        rdclass,
        use_edns=use_edns,
        ednsflags=ednsflags or 0,
        payload=payload,
        request_payload=request_payload or 0,
        options=options,
    )
    if serial is not None:
        soa = query.find_rrset(
            query.authority, origin, rdclass, RecordType.SOA, create=True
        )
        soa.add(parse_rdata(rdclass, RecordType.SOA, f". . {serial} 0 0 0 0"), 0)
    if keyring is not None:
        query.use_tsig(keyring, keyname, algorithm=keyalgorithm)
    return query, serial


def extract_serial_from_query(query):
    """Return the IXFR baseline or None for AXFR."""
    if isinstance(query, editable_message.QueryMessage):
        query = query._wire_message()
    if not isinstance(query, Message) or query.opcode != 0 or len(query.questions) != 1:
        raise ValueError("expected an AXFR or IXFR query")
    question = query.questions[0]
    if question.type == RecordType.AXFR:
        return None
    if question.type != RecordType.IXFR:
        raise ValueError("expected an AXFR or IXFR query")
    for record in query.authority:
        if (record.name, record.rdclass, record.type) == (
            question.name,
            question.rdclass,
            RecordType.SOA,
        ):
            return _serial(record)
    raise ValueError("IXFR requires an apex SOA")


async def transfer_async(origin: str, server: str, **kwargs) -> Transfer:
    return await run_blocking(transfer, origin, server, **kwargs)


def _request(query):
    key = (
        query.keyring if isinstance(query, editable_message.Message) else query.tsig_key
    )
    packet = query.to_wire()
    query = Message.from_wire(packet)
    if query.had_tsig and key is None:
        raise ValueError("a signed DNS transfer query requires its TSIG key")
    serial = extract_serial_from_query(query)
    return query, packet, key, serial


def _manager_request(txn_manager, query):
    origin, relativize, _ = txn_manager.origin_information()
    if origin is None:
        raise ValueError("transfer requires a zone origin")
    if query is None:
        query, _ = make_query(txn_manager)
    request = _request(query)
    question = request[0].questions[0]
    if (question.name, question.rdclass) != (
        origin.labels[:-1],
        txn_manager.get_class(),
    ):
        raise ValueError("DNS transfer query does not match the transaction manager")
    return request, origin if relativize else None


def _sync_frames(
    where,
    port,
    source,
    source_port,
    timeout,
    expiration,
    request,
    origin,
    udp,
    raise_on_serial_went_backwards,
):
    query, packet, key, serial = request
    verifier = None if key is None else StreamVerifier(key, query.mac or None)
    keyring = None if verifier is None else False
    state = _transfer_decoder(
        query, serial, verifier, 1000000, raise_on_serial_went_backwards
    )
    kind = socket.SOCK_DGRAM if udp else socket.SOCK_STREAM
    family, _, _, _, peer = socket.getaddrinfo(
        where, port, type=kind, flags=socket.AI_NUMERICHOST
    )[0]

    def frame_expiration():
        if timeout is None:
            return expiration
        per_frame = time() + timeout
        return per_frame if expiration is None else min(per_frame, expiration)

    try:
        next(state)
        with syncquery.make_socket(
            family, kind, syncquery._source(family, source, source_port)
        ) as sock:
            sock.settimeout(None if expiration is None else max(expiration - time(), 0))
            sock.connect(peer)
            if udp:
                syncquery.send_udp(sock, packet, None, expiration)
            else:
                syncquery.send_tcp(sock, packet, expiration)
            while True:
                if udp:
                    try:
                        reply, _ = syncquery.receive_udp(
                            sock,
                            peer,
                            frame_expiration(),
                            keyring=keyring,
                            raise_on_truncation=True,
                        )
                    except Truncated as exc:
                        raise UseTCP("IXFR requires TCP") from exc
                else:
                    reply, _ = syncquery.receive_tcp(
                        sock, frame_expiration(), keyring=keyring
                    )
                try:
                    state.send(reply.wire)
                except StopIteration as finished:
                    result = finished.value
                else:
                    result = None
                if udp and result is None:
                    raise UseTCP("IXFR requires more than one UDP response")
                response = Message.from_wire(
                    reply.wire,
                    origin=origin,
                    xfr=True,
                    one_rr_per_rrset=serial is not None,
                )
                yield editable_message.Message._from_wire_message(
                    replace(response, tsig_key=key, request_mac=query.mac or b"")
                )
                if result is not None:
                    return result
    finally:
        state.close()


def xfr(
    where,
    zone,
    rdtype,
    rdclass,
    timeout,
    port,
    keyring,
    keyname,
    relativize,
    lifetime,
    source,
    source_port,
    serial,
    use_udp,
    keyalgorithm,
    raise_on_serial_went_backwards,
):
    origin = zone if isinstance(zone, DomainName) else domain_from_text(zone)
    rdtype, rdclass = record_type(rdtype), record_class(rdclass)
    if use_udp and rdtype != RecordType.IXFR:
        raise ValueError("cannot do a UDP AXFR")
    question = editable_message.make_query(origin, rdtype, rdclass)
    if rdtype == RecordType.IXFR:
        if not isinstance(serial, int) or not 0 <= serial < 2**32:
            raise ValueError("invalid IXFR serial")
        soa = question.find_rrset(
            question.authority, origin, rdclass, RecordType.SOA, create=True
        )
        soa.add(parse_rdata(rdclass, RecordType.SOA, f". . {serial} 0 0 0 0"), 0)
    if keyring is not None:
        question.use_tsig(keyring, keyname, algorithm=keyalgorithm)
    yield from _sync_frames(
        where,
        port,
        source,
        source_port,
        timeout,
        None if lifetime is None else time() + lifetime,
        _request(question),
        origin if relativize else None,
        use_udp,
        raise_on_serial_went_backwards,
    )


def inbound_xfr_sync(
    where,
    txn_manager,
    query,
    port,
    timeout,
    lifetime,
    source,
    source_port,
    udp_mode,
    raise_on_serial_went_backwards,
):
    request, origin = _manager_request(txn_manager, query)
    serial = request[3]
    expiration = None if lifetime is None else time() + lifetime

    def consume(udp):
        frames = _sync_frames(
            where,
            port,
            source,
            source_port,
            timeout,
            expiration,
            request,
            origin,
            udp,
            raise_on_serial_went_backwards,
        )
        try:
            while True:
                next(frames)
        except StopIteration as finished:
            result = finished.value
            if serial is None or _newer(_serial(result.soa), serial):
                result.apply_to(txn_manager)

    udp_mode = syncquery.UDPMode(udp_mode)
    if serial is not None and udp_mode != syncquery.UDPMode.NEVER:
        try:
            consume(True)
            return
        except UseTCP:
            if udp_mode == syncquery.UDPMode.ONLY:
                raise
    consume(False)


async def inbound_xfr(
    where,
    txn_manager,
    query=None,
    port=53,
    timeout=None,
    lifetime=None,
    source=None,
    source_port=0,
    udp_mode=asyncquery.UDPMode.NEVER,
    backend=None,
    raise_on_serial_went_backwards=True,
):
    """Receive an AXFR or IXFR and commit it only after validating the last frame."""
    (query, packet, key, serial), _ = _manager_request(txn_manager, query)
    backend = get_default_backend() if backend is None else backend
    expiration = None if lifetime is None else time() + lifetime

    def remaining_lifetime():
        if expiration is None:
            return None
        delay = expiration - time()
        if delay <= 0:
            raise TimeoutError("DNS transfer lifetime elapsed")
        return delay

    def frame_expiration():
        remaining_lifetime()
        return (
            expiration
            if timeout is None
            else min(time() + timeout, expiration or float("inf"))
        )

    def decoder():
        verifier = None if key is None else StreamVerifier(key, query.mac or None)
        result = _transfer_decoder(
            query, serial, verifier, 1000000, raise_on_serial_went_backwards
        )
        next(result)
        return result

    def apply(result):
        if serial is not None and _newer(serial, _serial(result.soa)):
            return
        result.apply_to(txn_manager)

    async def open_socket(kind):
        family, _, protocol, _, peer = socket.getaddrinfo(
            where,
            port,
            type=kind,
            flags=socket.AI_NUMERICHOST,
        )[0]
        local = None
        if source is not None or source_port:
            host = source or ("::" if family == socket.AF_INET6 else "0.0.0.0")
            local = socket.getaddrinfo(
                host, source_port, family, kind, 0, socket.AI_NUMERICHOST
            )[0][4]
        sock = await backend.make_socket(
            family, kind, protocol, local, peer, remaining_lifetime()
        )
        return sock, peer

    udp_mode = asyncquery.UDPMode(udp_mode)
    if serial is not None and udp_mode != asyncquery.UDPMode.NEVER:
        sock, peer = await open_socket(socket.SOCK_DGRAM)
        try:
            async with sock:
                await asyncquery.send_udp(sock, packet, None, frame_expiration())
                reply, _, _ = await asyncquery.receive_udp(
                    sock,
                    peer,
                    frame_expiration(),
                    keyring=None if key is None else False,
                    raise_on_truncation=True,
                )
                state = decoder()
                try:
                    state.send(reply.wire)
                except StopIteration as finished:
                    apply(finished.value)
                    return
                finally:
                    state.close()
                raise UseTCP("IXFR requires more than one UDP response")
        except (UseTCP, Truncated) as exc:
            if udp_mode == asyncquery.UDPMode.ONLY:
                raise UseTCP("IXFR requires TCP") from exc

    sock, _ = await open_socket(socket.SOCK_STREAM)
    state = decoder()
    try:
        async with sock:
            await asyncquery.send_tcp(sock, packet, frame_expiration())
            while True:
                reply, _ = await asyncquery.receive_tcp(
                    sock, frame_expiration(), keyring=None if key is None else False
                )
                try:
                    state.send(reply.wire)
                except StopIteration as finished:
                    apply(finished.value)
                    return
    finally:
        state.close()
