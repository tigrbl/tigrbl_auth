"""In-house DNS stub resolver over plain and encrypted transports."""

import asyncio
import ipaddress
import math
import secrets
import ssl
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field, replace
from pathlib import Path
from threading import RLock
from time import sleep, time
from urllib.parse import urlsplit

from tba_codec_dns.rdata import decoded
from tba_codec_dns.rrset import RRset
from tba_codec_dns.wire import (
    EdnsOption,
    Message,
    Question,
    RecordType,
    ResourceRecord,
    WireError,
    opt_record,
)
from tba_primitives_dns_name.name import Name as DomainName
from tba_primitives_dns_name.names import (
    Name,
    check_name,
    is_absolute_text,
    is_subdomain,
    name_text,
    parse_name,
)

from ._cache import Cache as Cache
from ._cache import CacheStatistics as CacheStatistics
from ._configuration import _parse_resolv_conf, _resolver_configuration
from .transport import (
    check_response,
    deadline_after,
    https_query,
    quic_query,
    remaining,
    tcp_query,
    tls_query,
    udp_with_fallback,
)
from .tsig import AuthKey, sign, verify


class NXDOMAIN(LookupError):
    """The queried name does not exist."""


class NoAnswer(LookupError):
    """The name exists without the requested record type."""

    def __init__(self, name=None, answer: "Answer | None" = None):
        super().__init__(name)
        self.answer = answer


class NoNameservers(OSError):
    """The available name servers could not answer the query."""


@dataclass(frozen=True)
class Answer(Sequence[ResourceRecord]):
    """A resolved name, alias chain, response, and expiring record set."""

    question: Question
    response: Message
    canonical_name: DomainName
    rrset: RRset | None
    expiration: float
    aliases: tuple[ResourceRecord, ...] = ()

    @property
    def qname(self) -> DomainName:
        return DomainName((*self.question.name, b""))

    @property
    def rdtype(self) -> int:
        return self.question.type

    @property
    def rdclass(self) -> int:
        return self.question.rdclass

    @property
    def records(self) -> tuple[ResourceRecord, ...]:
        return () if self.rrset is None else self.rrset.records

    def __len__(self) -> int:
        return len(self.records)

    def __getitem__(self, index):
        return self.records[index]


@dataclass(frozen=True)
class TlsNameserver:
    address: str
    hostname: str | None = None
    port: int = 853
    context: ssl.SSLContext | None = field(default=None, repr=False)
    certificate_ip: str | None = None

    def query(self, query: Message, timeout: float) -> Message:
        return tls_query(
            query,
            self.address,
            port=self.port,
            timeout=timeout,
            server_name=self.hostname,
            context=self.context,
            certificate_ip=self.certificate_ip,
        )


@dataclass(frozen=True)
class HttpsNameserver:
    url: str
    post: bool = True
    context: ssl.SSLContext | None = field(default=None, repr=False)
    http_version: int = 1
    ca_file: str | None = field(default=None, repr=False)
    ca_data: bytes | None = field(default=None, repr=False)
    bootstrap_address: str | None = None
    certificate_ip: str | None = None
    session: object | None = field(default=None, repr=False)

    def query(self, query: Message, timeout: float) -> Message:
        return https_query(
            query,
            self.url,
            timeout=timeout,
            post=self.post,
            context=self.context,
            http_version=self.http_version,
            ca_file=self.ca_file,
            ca_data=self.ca_data,
            bootstrap_address=self.bootstrap_address,
            certificate_ip=self.certificate_ip,
            session=self.session,
        )


@dataclass(frozen=True)
class QuicNameserver:
    address: str
    hostname: str | None = None
    port: int = 853
    ca_file: str | None = field(default=None, repr=False)
    ca_data: bytes | None = field(default=None, repr=False)
    certificate_ip: str | None = None

    def query(self, query: Message, timeout: float) -> Message:
        return asyncio.run(
            quic_query(
                query,
                self.address,
                port=self.port,
                timeout=timeout,
                server_name=self.hostname,
                ca_file=self.ca_file,
                ca_data=self.ca_data,
                certificate_ip=self.certificate_ip,
            )
        )


_Nameserver = str | TlsNameserver | HttpsNameserver | QuicNameserver


@dataclass(frozen=True)
class _Exchange:
    request: Message
    server: _Nameserver
    timeout: float
    port: int
    tcp: bool


def _drive(steps, dispatch):
    try:
        operation = next(steps)
        while True:
            try:
                value = dispatch(operation)
            except (OSError, WireError) as exc:
                operation = steps.throw(exc)
            else:
                operation = steps.send(value)
    except StopIteration as finished:
        return finished.value
    finally:
        steps.close()


async def _drive_async(steps, dispatch):
    try:
        operation = next(steps)
        while True:
            try:
                value = await dispatch(operation)
            except (OSError, WireError) as exc:
                operation = steps.throw(exc)
            else:
                operation = steps.send(value)
    except StopIteration as finished:
        return finished.value
    finally:
        steps.close()


def _send_sync(operation):
    if isinstance(operation, float):
        sleep(operation)
        return None
    request, server = operation.request, operation.server
    if isinstance(server, str):
        options = {"port": operation.port, "timeout": operation.timeout}
        if operation.tcp:
            return tcp_query(request, server, **options)
        return udp_with_fallback(request, server, **options)[0]
    return server.query(request, operation.timeout)


def _address_types(family: int) -> tuple[str, ...]:
    try:
        return {0: ("AAAA", "A"), 4: ("A",), 6: ("AAAA",)}[family]
    except KeyError as exc:
        raise ValueError("DNS address family must be 0, 4, or 6") from exc


class Resolver:
    """Query absolute DNS names using configured recursive name servers."""

    def __init__(
        self,
        nameservers: Iterable[_Nameserver] | None = None,
        *,
        port: int = 53,
        timeout: float = 1,
        search: Iterable[str] | None = None,
        ndots: int | None = None,
        cache: Cache | None = None,
        lifetime: float = 3,
        use_search_by_default: bool = False,
        nameserver_ports: Mapping[str, int] | None = None,
        retry_servfail: bool = False,
        configure: bool = True,
        filename=None,
    ) -> None:
        if not math.isfinite(timeout) or timeout <= 0:
            raise ValueError("DNS timeout must be finite and positive")
        if not 1 <= port <= 65535:
            raise ValueError("DNS port must be in 1..65535")
        deadline_after(lifetime)
        defaults, suffixes, default_ndots = [], [], 1
        if nameservers is None and configure:
            if filename is None:
                defaults, suffixes, default_ndots = _resolver_configuration()
            else:
                text = (
                    filename.read()
                    if hasattr(filename, "read")
                    else Path(filename).read_text(encoding="ascii")
                )
                defaults, suffixes, default_ndots = _parse_resolv_conf(text)
        servers = defaults if nameservers is None else nameservers
        self.nameservers = servers
        self.port = port
        self.timeout = timeout
        self.lifetime = lifetime
        self.use_search_by_default = use_search_by_default
        self.retry_servfail = retry_servfail
        self.nameserver_ports = {
            str(ipaddress.ip_address(address)): server_port
            for address, server_port in (nameserver_ports or {}).items()
        }
        if any(
            not 1 <= server_port <= 65535
            for server_port in self.nameserver_ports.values()
        ):
            raise ValueError("DNS nameserver port is outside 1..65535")
        self.search = tuple(
            parse_name(suffix, canonical=True)
            for suffix in (suffixes if search is None else search)
        )
        self.ndots = default_ndots if ndots is None else ndots
        if not 0 <= self.ndots <= 15:
            raise ValueError("DNS ndots must be in 0..15")
        self.cache = cache
        self._edns = None
        self._auth_key = None

    @property
    def nameservers(self) -> tuple[_Nameserver, ...]:
        return self._nameservers

    @nameservers.setter
    def nameservers(self, servers: Iterable[_Nameserver]) -> None:
        values = []
        for server in servers:
            if isinstance(server, str):
                if server.lower().startswith("https://"):
                    server = HttpsNameserver(server)
                else:
                    server = str(ipaddress.ip_address(server))
            elif not isinstance(
                server, (HttpsNameserver, TlsNameserver, QuicNameserver)
            ):
                raise ValueError("unsupported DNS nameserver type")
            values.append(server)
        self._nameservers = tuple(dict.fromkeys(values))

    def use_edns(
        self,
        edns: int | bool | None = 0,
        *,
        ednsflags: int = 0,
        payload: int = 1232,
        options: tuple[EdnsOption, ...] = (),
    ) -> None:
        if edns is None or edns is False or edns == -1:
            self._edns = None
        else:
            self._edns = opt_record(
                payload,
                version=0 if edns is True else edns,
                flags=ednsflags,
                options=tuple(options),
            )

    def use_tsig(self, key: AuthKey | None) -> None:
        self._auth_key = key

    def _query(self, question: Question, deadline: float, **options) -> Message:
        return _drive(self._query_steps(question, deadline, **options), _send_sync)

    def _query_steps(
        self,
        question: Question,
        deadline: float,
        *,
        tcp: bool,
        edns_payload: int | None,
        want_dnssec: bool,
        edns_options: tuple[EdnsOption, ...] = (),
    ) -> Message:
        template = question.query_message(
            0,
            edns_payload=edns_payload,
            want_dnssec=want_dnssec,
            edns_options=edns_options,
        )
        if not template.additional and self._edns is not None:
            template = replace(template, additional=(self._edns,))
        authentication = self._auth_key
        cache = self.cache if not tcp and authentication is None else None
        servers = self.nameservers
        key = (
            servers,
            self.port,
            tuple(sorted(self.nameserver_ports.items())),
            question,
            template.additional,
        )
        if cache is not None:
            cached = cache.get(key)
            if cached is not None:
                return cached
        last_error = None
        for round_number in range(3):
            retry = []
            for server in servers:
                attempt = min(self.timeout, remaining(deadline))
                try:
                    encrypted_stream = isinstance(
                        server, (HttpsNameserver, QuicNameserver)
                    )
                    identifier = 0 if encrypted_stream else secrets.randbits(16)
                    request = replace(template, id=identifier)
                    mac = None
                    if authentication is not None:
                        wire, mac = sign(request.to_wire(), authentication)
                        request = Message.from_wire(wire)
                    if isinstance(server, str):
                        port = self.nameserver_ports.get(server, self.port)
                    elif isinstance(server, HttpsNameserver):
                        port = urlsplit(server.url).port or 443
                    else:
                        port = server.port
                    message = yield _Exchange(request, server, attempt, port, tcp)
                    check_response(
                        request, message, allow_empty_question=request.opcode == 5
                    )
                    if authentication is not None:
                        verify(message.to_wire(), authentication, request_mac=mac)
                    if message.rcode in (0, 3):
                        if cache is not None:
                            cache.put(key, message)
                        return message
                    if message.rcode == 2 and self.retry_servfail:
                        retry.append(server)
                    last_error = NoNameservers(
                        f"DNS server returned rcode {message.rcode}"
                    )
                except (OSError, WireError) as exc:
                    if isinstance(exc, TimeoutError):
                        retry.append(server)
                    last_error = exc
            if not retry:
                break
            servers = tuple(retry)
            if round_number < 2:
                yield min(0.05 * 2**round_number, remaining(deadline) / 2)
        raise NoNameservers("no DNS server produced a usable response") from last_error

    def query(
        self,
        question: Question,
        *,
        lifetime: float | None = None,
        tcp: bool = False,
        edns_payload: int | None = None,
        want_dnssec: bool = False,
        edns_options: tuple[EdnsOption, ...] = (),
    ) -> Message:
        return self._query(
            question,
            deadline_after(self.lifetime if lifetime is None else lifetime),
            tcp=tcp,
            edns_payload=edns_payload,
            want_dnssec=want_dnssec,
            edns_options=edns_options,
        )

    def resolve(
        self,
        name: str | DomainName,
        rdtype: int | str = "A",
        *,
        search: bool | None = None,
        lifetime: float | None = None,
        rdclass: int | str = 1,
        tcp: bool = False,
    ) -> tuple[ResourceRecord, ...]:
        return self._resolve(
            name, rdtype, search=search, lifetime=lifetime, rdclass=rdclass, tcp=tcp
        )

    def _resolve(
        self,
        name: str | DomainName,
        rdtype: int | str,
        *,
        search: bool | None,
        lifetime: float | None,
        rdclass: int | str,
        tcp: bool,
    ) -> tuple[ResourceRecord, ...]:
        return Resolver.resolve_answer(
            self,
            name,
            rdtype,
            search=search,
            lifetime=lifetime,
            rdclass=rdclass,
            tcp=tcp,
        ).records

    def resolve_answer(
        self,
        name: str | DomainName,
        rdtype: int | str = "A",
        *,
        search: bool | None = None,
        lifetime: float | None = None,
        rdclass: int | str = 1,
        tcp: bool = False,
        raise_on_no_answer: bool = True,
    ) -> Answer:
        steps = self._resolve_steps(
            name,
            rdtype,
            search=search,
            lifetime=lifetime,
            rdclass=rdclass,
            tcp=tcp,
            raise_on_no_answer=raise_on_no_answer,
        )
        return _drive(
            steps,
            lambda operation: self._query(
                operation[0],
                operation[1],
                tcp=operation[2],
                edns_payload=None,
                want_dnssec=False,
            ),
        )

    def _resolve_steps(
        self,
        name: str | DomainName,
        rdtype: int | str = "A",
        *,
        search: bool | None = None,
        lifetime: float | None = None,
        rdclass: int | str = 1,
        tcp: bool = False,
        raise_on_no_answer: bool = True,
    ):
        text = name.to_text() if isinstance(name, DomainName) else name
        question = Question.from_text(text, rdtype, rdclass)
        deadline = deadline_after(self.lifetime if lifetime is None else lifetime)
        candidates = [question.name]
        search = self.use_search_by_default if search is None else search
        if search and not is_absolute_text(text) and text != "@":
            expanded = [check_name(question.name + suffix) for suffix in self.search]
            candidates = (
                candidates + expanded
                if len(question.name) - 1 >= self.ndots
                else expanded + candidates
            )
        last_no_data = None
        for candidate in dict.fromkeys(candidates):
            try:
                return (
                    yield from self._name_steps(
                        Question(candidate, question.type, question.rdclass),
                        deadline,
                        tcp,
                    )
                )
            except NoAnswer as exc:
                last_no_data = exc
            except NXDOMAIN:
                continue
        if last_no_data is not None:
            if not raise_on_no_answer and last_no_data.answer is not None:
                return last_no_data.answer
            raise last_no_data
        raise NXDOMAIN(name)

    def _resolve_name(self, question: Question, deadline: float, tcp: bool) -> Answer:
        return _drive(
            self._name_steps(question, deadline, tcp),
            lambda operation: self._query(
                operation[0],
                operation[1],
                tcp=operation[2],
                edns_payload=None,
                want_dnssec=False,
            ),
        )

    def _name_steps(self, question: Question, deadline: float, tcp: bool):
        original = question
        seen = set()
        chain = []
        while True:
            message = yield question, deadline, tcp
            if message.rcode == 3:
                raise NXDOMAIN(original.name)
            queried_name = question.name
            while True:
                records = tuple(
                    rr
                    for rr in message.answers
                    if rr.name == question.name and rr.rdclass == question.rdclass
                )
                answer = tuple(rr for rr in records if rr.type == question.type)
                if answer:
                    ttl = min(rr.ttl for rr in answer)
                    return Answer(
                        original,
                        message,
                        DomainName((*question.name, b"")),
                        RRset(
                            question.name, question.rdclass, question.type, ttl, answer
                        ),
                        time() + min(rr.ttl for rr in (*answer, *chain)),
                        tuple(chain),
                    )
                aliases = tuple(rr for rr in records if rr.type == RecordType.CNAME)
                if not aliases:
                    dnames = tuple(
                        rr
                        for rr in message.answers
                        if rr.type == RecordType.DNAME
                        and rr.rdclass == question.rdclass
                        and rr.name != question.name
                        and is_subdomain(question.name, rr.name)
                    )
                    if not dnames:
                        if queried_name == question.name:
                            soa = next(
                                (
                                    rr
                                    for rr in message.authority
                                    if rr.type == RecordType.SOA
                                ),
                                None,
                            )
                            ttl = (
                                min(soa.ttl, decoded(soa)[-1]) if soa is not None else 0
                            )
                            if chain:
                                ttl = min(ttl, *(rr.ttl for rr in chain))
                            empty = Answer(
                                original,
                                message,
                                DomainName((*question.name, b"")),
                                None,
                                time() + ttl,
                                tuple(chain),
                            )
                            raise NoAnswer(original.name, empty)
                        break
                    dname = max(dnames, key=lambda rr: len(rr.name))
                    aliases = tuple(rr for rr in dnames if rr.name == dname.name)
                if len(aliases) != 1 or question.name in seen or len(seen) >= 16:
                    raise WireError("invalid DNS alias chain")
                seen.add(question.name)
                chain.append(aliases[0])
                target, consumed = aliases[0].read_name()
                if consumed != len(aliases[0].data):
                    raise WireError("trailing data in DNS alias record")
                if aliases[0].type == RecordType.DNAME:
                    prefix: Name = question.name[
                        : len(question.name) - len(aliases[0].name)
                    ]
                    target = check_name(prefix + target)
                question = Question(target, question.type, question.rdclass)

    def resolve_address(
        self, address: str, *, lifetime: float | None = None
    ) -> tuple[ResourceRecord, ...]:
        return self._resolve_name(
            Question.from_text(ipaddress.ip_address(address).reverse_pointer, "PTR"),
            deadline_after(self.lifetime if lifetime is None else lifetime),
            False,
        ).records

    def resolve_name(
        self, name: str, *, family: int = 0, lifetime: float = 3, search: bool = False
    ) -> tuple[ipaddress.IPv4Address | ipaddress.IPv6Address, ...]:
        """Return IPv6 and IPv4 addresses for a name, or restrict to family 4 or 6."""
        kinds = _address_types(family)
        deadline = deadline_after(lifetime)
        addresses = []
        for kind in kinds:
            try:
                records = self._resolve(
                    name,
                    kind,
                    search=search,
                    lifetime=remaining(deadline),
                    rdclass=1,
                    tcp=False,
                )
                addresses.extend(decoded(record)[0] for record in records)
            except (NoAnswer, NXDOMAIN):
                continue
        if not addresses:
            raise NoAnswer(name)
        return tuple(dict.fromkeys(addresses))

    def canonical_name(self, name: str, *, lifetime: float = 3) -> Name:
        return _drive(
            self._canonical_steps(name, lifetime),
            lambda operation: self._query(
                operation[0],
                operation[1],
                tcp=operation[2],
                edns_payload=None,
                want_dnssec=False,
            ),
        )

    def _canonical_steps(self, name, lifetime):
        deadline = deadline_after(lifetime)
        question = Question.from_text(name, "A")
        seen = set()
        while True:
            response = yield question, deadline, False
            targets = [
                rr
                for rr in response.answers
                if rr.name == question.name
                and rr.type == RecordType.CNAME
                and rr.rdclass == question.rdclass
            ]
            if not targets:
                return question.name
            if len(targets) != 1 or question.name in seen or len(seen) >= 16:
                raise WireError("invalid DNS alias chain")
            seen.add(question.name)
            target, end = targets[0].read_name()
            if end != len(targets[0].data):
                raise WireError("trailing data in DNS alias record")
            question = Question(target, question.type, question.rdclass)

    def zone_for_name(self, name: str, *, lifetime: float = 3) -> Name:
        return _drive(
            self._zone_steps(name, lifetime),
            lambda operation: self._query(
                operation[0],
                operation[1],
                tcp=operation[2],
                edns_payload=None,
                want_dnssec=False,
            ),
        )

    def _zone_steps(self, name, lifetime):
        owner = parse_name(name, canonical=True)
        deadline = deadline_after(lifetime)
        for start in range(len(owner) + 1):
            candidate = owner[start:]
            question = Question(candidate, RecordType.SOA)
            response = yield question, deadline, False
            if response.rcode == 0 and any(
                rr.name == candidate
                and rr.type == RecordType.SOA
                and rr.rdclass == question.rdclass
                for rr in response.answers
            ):
                return candidate
        raise NoAnswer(f"could not find enclosing DNS zone for {name_text(owner)}")


class AsyncResolver(Resolver):
    """Awaitable resolver using the same wire and timeout semantics."""

    async def _async_query(self, question, deadline, backend, **options):
        async def execute(operation):
            if isinstance(operation, float):
                return await backend.sleep(operation)
            try:
                return await backend.query(
                    operation.request,
                    operation.server,
                    port=operation.port,
                    timeout=operation.timeout,
                    tcp=operation.tcp,
                )
            except asyncio.TimeoutError as exc:
                raise TimeoutError("DNS async backend timed out") from exc

        return await _drive_async(
            self._query_steps(question, deadline, **options), execute
        )

    async def query(
        self,
        question: Question,
        *,
        lifetime: float | None = None,
        tcp: bool = False,
        edns_payload: int | None = None,
        want_dnssec: bool = False,
        edns_options: tuple[EdnsOption, ...] = (),
        backend=None,
    ) -> Message:
        from .asyncbackend import get_default_backend

        return await self._async_query(
            question,
            deadline_after(self.lifetime if lifetime is None else lifetime),
            get_default_backend() if backend is None else backend,
            tcp=tcp,
            edns_payload=edns_payload,
            want_dnssec=want_dnssec,
            edns_options=edns_options,
        )

    async def _resolve_async_steps(self, steps, backend):
        from .asyncbackend import get_default_backend

        backend = get_default_backend() if backend is None else backend

        async def execute(operation):
            question, deadline, tcp = operation
            return await self._async_query(
                question,
                deadline,
                backend,
                tcp=tcp,
                edns_payload=None,
                want_dnssec=False,
            )

        return await _drive_async(steps, execute)

    async def resolve(self, *args, **kwargs) -> tuple[ResourceRecord, ...]:
        return (await self.resolve_answer(*args, **kwargs)).records

    async def resolve_answer(self, *args, backend=None, **kwargs) -> Answer:
        return await self._resolve_async_steps(
            self._resolve_steps(*args, **kwargs), backend
        )

    async def resolve_address(
        self, address, *, lifetime=None, backend=None
    ) -> tuple[ResourceRecord, ...]:
        question = Question.from_text(
            ipaddress.ip_address(address).reverse_pointer, "PTR"
        )
        deadline = deadline_after(self.lifetime if lifetime is None else lifetime)
        return (
            await self._resolve_async_steps(
                self._name_steps(question, deadline, False), backend
            )
        ).records

    async def resolve_name(
        self, name, *, family=0, lifetime=3, search=False, backend=None
    ):
        kinds = _address_types(family)
        deadline = deadline_after(lifetime)
        addresses = []
        for kind in kinds:
            try:
                answer = await self.resolve_answer(
                    name,
                    kind,
                    lifetime=remaining(deadline),
                    search=search,
                    backend=backend,
                )
            except (NXDOMAIN, NoAnswer):
                continue
            addresses.extend(decoded(record)[0] for record in answer.records)
        if not addresses:
            raise NoAnswer(name)
        return tuple(dict.fromkeys(addresses))

    async def canonical_name(self, name, *, lifetime=3, backend=None) -> Name:
        return await self._resolve_async_steps(
            self._canonical_steps(name, lifetime), backend
        )

    async def zone_for_name(self, name, *, lifetime=3, backend=None) -> Name:
        return await self._resolve_async_steps(
            self._zone_steps(name, lifetime), backend
        )



_default: Resolver | None = None
_default_lock = RLock()


def get_default_resolver() -> Resolver:
    global _default
    with _default_lock:
        if _default is None:
            _default = Resolver()
        return _default


def reset_default_resolver() -> Resolver:
    global _default
    with _default_lock:
        _default = Resolver()
        return _default


def resolve(name: str, rdtype: int | str = "A", **kwargs) -> tuple[ResourceRecord, ...]:
    return get_default_resolver().resolve(name, rdtype, **kwargs)


def resolve_at(
    server: str,
    name: str,
    rdtype: int | str = "A",
    *,
    port: int = 53,
    lifetime: float = 3,
    **kwargs,
) -> tuple[ResourceRecord, ...]:
    return Resolver([server], port=port, timeout=lifetime).resolve(
        name, rdtype, lifetime=lifetime, **kwargs
    )
