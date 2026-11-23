"""Build and send RFC 2136 DNS UPDATE requests."""

import secrets
import ssl
from dataclasses import replace

from tba_codec_dns.message import UpdateMessage as UpdateMessage
from tba_codec_dns.rdata import Rdata
from tba_codec_dns.rdata import from_text as parse_rdata
from tba_codec_dns.rdataset import Rdataset
from tba_codec_dns.tsig import AuthKey, sign, verify
from tba_codec_dns.wire import (
    Message,
    Question,
    RecordClass,
    RecordType,
    ResourceRecord,
    record_class,
    record_type,
)
from tba_primitives_dns_name.name import Name as DomainName
from tba_primitives_dns_name.names import Name, is_subdomain, parse_name
from tba_provider_dns_resolver.async_transport import run_blocking
from tba_provider_dns_resolver.transport import (
    check_response,
    deadline_after,
    exchange_udp_packet,
    stream,
)


class Update:
    def __init__(self, zone: str | DomainName, *, rdclass: int | str = RecordClass.IN):
        self.zone = parse_name(str(zone), canonical=True)
        self.rdclass = record_class(rdclass)
        if self.rdclass in (0, RecordClass.NONE, RecordClass.ANY):
            raise ValueError("UPDATE requires a concrete zone class")
        self.prerequisites: list[ResourceRecord] = []
        self.changes: list[ResourceRecord] = []

    def _owner(self, name: str | Name | DomainName) -> Name:
        if isinstance(name, DomainName):
            name = name.to_text()
        owner = (
            parse_name(name, self.zone, canonical=True)
            if isinstance(name, str)
            else name
        )
        if not is_subdomain(owner, self.zone):
            raise ValueError("UPDATE owner is outside the zone")
        return owner

    def _placeholder(
        self, name: str | Name, kind: int | str, rdclass: int
    ) -> ResourceRecord:
        return ResourceRecord(self._owner(name), record_type(kind), rdclass, 0, b"")

    def _record(self, record: ResourceRecord) -> ResourceRecord:
        self._owner(record.name)
        if record.rdclass != self.rdclass or record.type in (
            RecordType.ANY,
            RecordType.AXFR,
            RecordType.IXFR,
            RecordType.OPT,
            RecordType.TSIG,
            RecordType.TKEY,
        ):
            raise ValueError("record class or type cannot be used for UPDATE")
        return record

    def _values(
        self, name: str | Name | DomainName, values: tuple, ttl: int
    ) -> tuple[ResourceRecord, ...]:
        owner = self._owner(name)
        if isinstance(values[0], Rdata):
            return tuple(self._record(value.record(owner, ttl)) for value in values)
        kind, *text = values
        if not text:
            raise ValueError("DNS update requires at least one RDATA value")
        origin = DomainName((*self.zone, b""))
        return tuple(
            self._record(
                parse_rdata(self.rdclass, kind, value, origin).record(owner, ttl)
            )
            for value in text
        )

    def _records(self, arguments: tuple) -> tuple[ResourceRecord, ...]:
        if not arguments or isinstance(arguments[0], ResourceRecord):
            return tuple(self._record(record) for record in arguments)
        owner, *args = arguments
        if len(args) == 1 and isinstance(args[0], Rdataset):
            return tuple(self._record(rr) for rr in args[0].records(self._owner(owner)))
        if len(args) < 2:
            raise ValueError("DNS update requires records, a dataset, or TTL and RDATA")
        return self._values(owner, tuple(args[1:]), args[0])

    def present(
        self,
        name: str | Name | DomainName,
        kind: int | str | Rdata | Rdataset = RecordType.ANY,
        *values,
    ) -> None:
        if isinstance(kind, Rdataset):
            if values:
                raise ValueError("unexpected RDATA after a DNS dataset")
            self.require_values(*kind.records(self._owner(name)))
        elif values or isinstance(kind, Rdata):
            self.require_values(*self._values(name, (kind, *values), 0))
        else:
            self.prerequisites.append(self._placeholder(name, kind, RecordClass.ANY))

    def absent(self, name: str | Name, kind: int | str = RecordType.ANY) -> None:
        self.prerequisites.append(self._placeholder(name, kind, RecordClass.NONE))

    def require_values(self, *records: ResourceRecord) -> None:
        self.prerequisites.extend(
            tuple(replace(self._record(rr), ttl=0) for rr in records)
        )

    def add(self, *arguments) -> None:
        self.changes.extend(self._records(arguments))

    def delete(
        self,
        name: str | Name | DomainName,
        kind: int | str | Rdata | Rdataset = RecordType.ANY,
        *values,
    ) -> None:
        if isinstance(kind, Rdataset):
            if values:
                raise ValueError("unexpected RDATA after a DNS dataset")
            self.delete_values(*kind.records(self._owner(name)))
        elif values or isinstance(kind, Rdata):
            self.delete_values(*self._values(name, (kind, *values), 0))
        else:
            self.changes.append(self._placeholder(name, kind, RecordClass.ANY))

    def delete_values(self, *records: ResourceRecord) -> None:
        self.changes.extend(
            tuple(
                replace(self._record(rr), ttl=0, rdclass=RecordClass.NONE)
                for rr in records
            )
        )

    def replace(self, *arguments) -> None:
        accepted = self._records(arguments)
        for owner, kind in dict.fromkeys((rr.name, rr.type) for rr in accepted):
            self.delete(owner, kind)
        self.changes.extend(accepted)

    def message(self, identifier: int | None = None) -> Message:
        return Message(
            secrets.randbits(16) if identifier is None else identifier,
            5 << 11,
            (Question(self.zone, RecordType.SOA, self.rdclass),),
            tuple(self.prerequisites),
            tuple(self.changes),
        )


def send_update(
    update: Update,
    server: str,
    *,
    port: int = 53,
    timeout: float = 3,
    key: AuthKey | None = None,
    udp: bool = False,
    server_name: str | None = None,
    context: ssl.SSLContext | None = None,
) -> Message:
    request = update.message()
    packet = request.to_wire()
    request_mac = None
    if key is not None:
        packet, request_mac = sign(packet, key)
    deadline = deadline_after(timeout)
    if udp:
        if server_name is not None or context is not None:
            raise ValueError("DNS UDP updates cannot use a TLS context")
        reply = exchange_udp_packet(request, packet, server, port, deadline, None)
    else:
        with stream(
            server, port, deadline, server_name=server_name, context=context
        ) as connection:
            connection.send(packet)
            reply = connection.receive()
    if key is not None:
        verify(reply, key, request_mac=request_mac)
    response = Message.from_wire(reply)
    check_response(request, response, allow_empty_question=True)
    return response


async def send_update_async(update: Update, server: str, **kwargs) -> Message:
    return await run_blocking(send_update, update, server, **kwargs)
