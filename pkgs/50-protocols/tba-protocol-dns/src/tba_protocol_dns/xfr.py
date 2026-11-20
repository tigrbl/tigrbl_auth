"""AXFR and IXFR zone transfers (RFC 5936 and RFC 1995)."""

import secrets
import socket
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from time import monotonic, time

from tba_codec_dns import message as editable_message
from tba_codec_dns.rdata import decoded, from_record
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
)
from tba_concrete_dns_zone.zone import Zone
from tba_primitives_dns_name.names import Name, is_subdomain, parse_name
from tba_provider_dns_resolver import asyncquery
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

    def apply_to(self, zone: Zone) -> None:
        """Commit a complete transfer atomically to an existing zone."""
        origin, _, _ = zone.origin_information()
        if (origin.labels[:-1], zone.get_class()) != (self.origin, self.rdclass):
            raise ValueError("DNS transfer requires the matching local zone")
        with zone.writer(replacement=self.snapshot is not None) as txn:
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
                    txn.delete(rr.name, from_record(rr))
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


class SerialWentBackwards(WireError):
    """A primary advertised a serial older than the local zone."""


class UseTCP(WireError):
    """A UDP response cannot complete this IXFR."""


def _transfer_decoder(
    query, serial, verifier, max_records, raise_on_serial_went_backwards=True
):
    owner, class_number = query.questions[0].name, query.questions[0].rdclass
    records = []
    opening = None
    incremental = False
    soa_count = 0
    while True:
        response_packet = yield
        response = Message.from_wire(response_packet)
        check_response(query, response, allow_empty_question=bool(records))
        if response.rcode or not response.answers or not response.flags & 0x0400:
            raise WireError(f"invalid or refused DNS transfer (rcode {response.rcode})")
        completed = False
        for rr in response.answers:
            if completed or len(records) >= max_records:
                raise WireError("excess records in DNS transfer")
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
        if serial is not None and len(records) and _newer(serial, _serial(opening)):
            if verifier is not None:
                verifier.verify(response_packet, last=True)
            if raise_on_serial_went_backwards:
                raise SerialWentBackwards(
                    "primary zone serial is older than the local serial"
                )
            return Transfer(owner, class_number, opening)
        unchanged = (
            len(records) == 1 and serial is not None and _serial(opening) == serial
        )
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


async def transfer_async(origin: str, server: str, **kwargs) -> Transfer:
    return await run_blocking(transfer, origin, server, **kwargs)


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
    origin, _, _ = txn_manager.origin_information()
    owner = origin.labels[:-1]
    rdclass = txn_manager.get_class()
    if query is None:
        with txn_manager.reader() as reader:
            apex = reader.get(origin, RecordType.SOA)
        baseline = () if not apex else (apex[0].record(owner, apex.ttl),)
        query = Message(
            secrets.randbits(16),
            0,
            (
                Question(
                    owner, RecordType.IXFR if baseline else RecordType.AXFR, rdclass
                ),
            ),
            authority=baseline,
        )
    key = (
        query.keyring if isinstance(query, editable_message.Message) else query.tsig_key
    )
    packet = query.to_wire()
    query = Message.from_wire(packet)
    if query.had_tsig and key is None:
        raise ValueError("a signed DNS transfer query requires its TSIG key")
    if len(query.questions) != 1:
        raise ValueError("a DNS transfer requires one question")
    question = query.questions[0]
    if (question.name, question.rdclass) != (owner, rdclass):
        raise ValueError("DNS transfer query does not match the transaction manager")
    serial = None
    if question.type == RecordType.IXFR:
        if len(query.authority) != 1 or query.authority[0].type != RecordType.SOA:
            raise ValueError("IXFR requires an apex SOA")
        serial = _serial(query.authority[0])
    elif question.type != RecordType.AXFR:
        raise ValueError("expected an AXFR or IXFR question")
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
                reply, _ = await asyncquery.receive_tcp(sock, frame_expiration())
                try:
                    state.send(reply.wire)
                except StopIteration as finished:
                    apply(finished.value)
                    return
    finally:
        state.close()
