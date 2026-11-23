"""In-house DNS stub resolver over plain and encrypted transports."""

import asyncio
import ipaddress
import math
import secrets
import socket
import ssl
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field, replace
from pathlib import Path
from threading import RLock
from time import sleep, time
from urllib.parse import urlsplit

from tba_codec_dns import message as editable_message
from tba_codec_dns.rdata import Rdata, decoded, from_record
from tba_codec_dns.rrset import RRset
from tba_codec_dns.wire import (
    EdnsOption,
    Message,
    Question,
    RecordClass,
    RecordType,
    ResourceRecord,
    Truncated,
    WireError,
    opt_record,
    record_class,
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
from ._cache import LRUCache as LRUCache
from ._configuration import _parse_resolv_conf, _resolver_configuration
from .nameserver import Nameserver
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

    def __init__(self, *args, qnames=None, responses=None):
        super().__init__(*args)
        self._qnames = [] if qnames is None else list(qnames)
        self._responses = {} if responses is None else dict(responses)

    def __str__(self):
        if self._qnames:
            return "DNS query names do not exist: " + ", ".join(map(str, self._qnames))
        return super().__str__()

    def qnames(self):
        return list(self._qnames)

    def responses(self):
        return dict(self._responses)

    def response(self, qname):
        return self._responses[qname]

    @property
    def canonical_name(self):
        if not self._qnames:
            raise TypeError("NXDOMAIN has no recorded query name")
        for qname in self._qnames:
            response = self._responses.get(qname)
            if response is not None:
                try:
                    canonical = response.canonical_name()
                except WireError:
                    continue
                if canonical != qname:
                    return canonical
        return self._qnames[0]

    def __add__(self, other):
        if not isinstance(other, NXDOMAIN):
            return NotImplemented
        return NXDOMAIN(
            qnames=tuple(dict.fromkeys((*self._qnames, *other._qnames))),
            responses={**self._responses, **other._responses},
        )


class NoAnswer(LookupError):
    """The name exists without the requested record type."""

    def __init__(self, name=None, answer: "Answer | None" = None, *, response=None):
        super().__init__(name if response is None else response.question)
        self.answer = answer
        self._response = response if answer is None else answer.response

    def response(self):
        return self._response


class NotAbsolute(ValueError):
    """The operation requires an absolute DNS name."""


class NoRootSOA(NoAnswer):
    """No enclosing SOA was found, including at the DNS root."""


class NoNameservers(OSError):
    """The available name servers could not answer the query."""


@dataclass(frozen=True)
class Answer(Sequence[Rdata]):
    """A resolved name, alias chain, response, and expiring record set."""

    question: Question
    response: editable_message.QueryMessage
    canonical_name: DomainName
    rrset: RRset | None
    expiration: float
    aliases: tuple[ResourceRecord, ...] = ()
    nameserver: str | None = None
    port: int | None = None
    minimum_ttl: int = 0

    def __post_init__(self):
        if isinstance(self.response, Message):
            object.__setattr__(
                self,
                "response",
                editable_message.Message._from_wire_message(self.response),
            )

    @property
    def chaining_result(self):
        names = []
        for alias in self.aliases:
            rrset = editable_message.RRset(
                DomainName((*alias.name, b"")),
                alias.rdclass,
                alias.type,
            )
            rrset.add(from_record(alias), alias.ttl)
            names.append(rrset)
        return editable_message.ChainingResult(
            self.canonical_name,
            self.rrset,
            self.minimum_ttl,
            names,
        )

    @property
    def name(self):
        if self.rrset is None:
            raise AttributeError("name")
        return self.rrset.name

    @property
    def ttl(self):
        if self.rrset is None:
            raise AttributeError("ttl")
        return self.rrset.ttl

    @property
    def covers(self):
        if self.rrset is None:
            raise AttributeError("covers")
        return self.rrset.covers

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
        if self.rrset is None:
            raise IndexError(index)
        return self.rrset[index]

    def __iter__(self):
        return iter(()) if self.rrset is None else iter(self.rrset)


class Answers(dict):
    """Resolved answers indexed by RR type."""


class EmptyHostAnswers(NoAnswer):
    """A host lookup did not supply any answers."""


class HostAnswers(Answers):
    @classmethod
    def make(cls, v6=None, v4=None, add_empty=True):
        return cls(
            (kind, answer)
            for kind, answer in ((RecordType.AAAA, v6), (RecordType.A, v4))
            if answer is not None and (add_empty or answer.rrset is not None)
        )

    def addresses_and_families(self, family=socket.AF_UNSPEC):
        for kind in _address_types(family):
            answer = self.get(kind)
            if answer is not None:
                af = socket.AF_INET6 if kind == RecordType.AAAA else socket.AF_INET
                for record in answer:
                    yield record.address, af

    def addresses(self, family=socket.AF_UNSPEC):
        return (address for address, _ in self.addresses_and_families(family))

    def canonical_name(self):
        answer = self.get(RecordType.AAAA, self.get(RecordType.A))
        if answer is None:
            raise EmptyHostAnswers
        return answer.canonical_name


@dataclass(frozen=True)
class TlsNameserver:
    address: str
    hostname: str | None = None
    port: int = 853
    context: ssl.SSLContext | None = field(default=None, repr=False)
    certificate_ip: str | None = None

    def query(
        self, query: Message, timeout: float, *, source=None, source_port=0
    ) -> Message:
        return tls_query(
            query,
            self.address,
            port=self.port,
            timeout=timeout,
            server_name=self.hostname,
            context=self.context,
            certificate_ip=self.certificate_ip,
            source=_source_binding(self.address, source, source_port),
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

    def query(
        self, query: Message, timeout: float, *, source=None, source_port=0
    ) -> Message:
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
            local_address=source,
            local_port=source_port,
        )


@dataclass(frozen=True)
class QuicNameserver:
    address: str
    hostname: str | None = None
    port: int = 853
    ca_file: str | None = field(default=None, repr=False)
    ca_data: bytes | None = field(default=None, repr=False)
    certificate_ip: str | None = None

    def query(
        self, query: Message, timeout: float, *, source=None, source_port=0
    ) -> Message:
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
                local_address=source,
                local_port=source_port,
            )
        )


_Nameserver = str | TlsNameserver | HttpsNameserver | QuicNameserver | Nameserver


@dataclass(frozen=True)
class _Exchange:
    request: Message
    server: _Nameserver
    timeout: float
    port: int
    tcp: bool
    source: str | None = None
    source_port: int = 0


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


def _source_binding(server, source, source_port):
    if source is None and not source_port:
        return None
    return source or (
        "::" if ipaddress.ip_address(server).version == 6 else "0.0.0.0"
    ), source_port


def _send_sync(operation):
    if isinstance(operation, float):
        sleep(operation)
        return None
    request, server = operation.request, operation.server
    if isinstance(server, str):
        options = {"port": operation.port, "timeout": operation.timeout}
        binding = _source_binding(server, operation.source, operation.source_port)
        if binding is not None:
            options["source"] = binding
        if operation.tcp:
            return tcp_query(request, server, **options)
        return udp_with_fallback(request, server, **options)[0]
    if isinstance(server, Nameserver):
        try:
            return server.query(
                request,
                operation.timeout,
                operation.source,
                operation.source_port,
                operation.tcp,
            )
        except Truncated:
            if operation.tcp or server.is_always_max_size():
                raise
            return server.query(
                request,
                operation.timeout,
                operation.source,
                operation.source_port,
                True,
            )
    options = {}
    if operation.source is not None or operation.source_port:
        options.update(source=operation.source, source_port=operation.source_port)
    return server.query(request, operation.timeout, **options)


def _address_types(family: int) -> tuple[RecordType, ...]:
    if family == socket.AF_UNSPEC:
        return RecordType.AAAA, RecordType.A
    if family in (4, socket.AF_INET):
        return (RecordType.A,)
    if family in (6, socket.AF_INET6):
        return (RecordType.AAAA,)
    raise NotImplementedError(f"unsupported DNS address family {family}")


def _host_steps(resolver, name, family, options):
    options = dict(options)
    options.pop("rdtype", None)
    options["rdclass"] = RecordClass.IN
    types = _address_types(family)
    if len(types) == 1:
        answer = yield name, types[0], options
        return HostAnswers({types[0]: answer})
    raise_on_no_answer = options.pop("raise_on_no_answer", True)
    lifetime = options.pop("lifetime", None)
    deadline = deadline_after(resolver.lifetime if lifetime is None else lifetime)
    options.update(raise_on_no_answer=False, lifetime=remaining(deadline))
    v6 = yield name, RecordType.AAAA, options
    options.update(search=False, lifetime=remaining(deadline))
    v4 = yield v6.qname, RecordType.A, options
    answers = HostAnswers.make(v6, v4, add_empty=not raise_on_no_answer)
    if not answers:
        raise NoAnswer(name, v6)
    return answers


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
                server, (HttpsNameserver, TlsNameserver, QuicNameserver, Nameserver)
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
        source: str | None = None,
        source_port: int = 0,
        cache_response: bool = True,
        include_endpoint: bool = False,
    ):
        template = question.query_message(
            0,
            edns_payload=edns_payload,
            want_dnssec=want_dnssec,
            edns_options=edns_options,
        )
        if not template.additional and self._edns is not None:
            template = replace(template, additional=(self._edns,))
        authentication = self._auth_key
        cache = (
            self.cache
            if cache_response
            and not (tcp or source is not None or source_port or authentication)
            else None
        )
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
                    ) or (
                        isinstance(server, Nameserver)
                        and server.kind() in {"DoH", "DoQ"}
                    )
                    identifier = 0 if encrypted_stream else secrets.randbits(16)
                    request = replace(template, id=identifier)
                    mac = None
                    if authentication is not None:
                        wire, mac = sign(request.to_wire(), authentication)
                        request = replace(
                            Message.from_wire(wire), tsig_key=authentication
                        )
                    if isinstance(server, str):
                        port = self.nameserver_ports.get(server, self.port)
                    elif isinstance(server, HttpsNameserver):
                        port = urlsplit(server.url).port or 443
                    elif isinstance(server, Nameserver):
                        port = server.answer_port()
                    else:
                        port = server.port
                    message = yield _Exchange(
                        request, server, attempt, port, tcp, source, source_port
                    )
                    check_response(
                        request, message, allow_empty_question=request.opcode == 5
                    )
                    if authentication is not None:
                        verify(message.to_wire(), authentication, request_mac=mac)
                    if message.rcode in (0, 3):
                        if cache is not None:
                            cache.put(key, message)
                        if include_endpoint:
                            if isinstance(server, str):
                                endpoint = server
                            elif isinstance(server, Nameserver):
                                endpoint = server.answer_nameserver()
                            elif isinstance(server, HttpsNameserver):
                                endpoint = server.url
                            else:
                                endpoint = server.address
                            return message, endpoint, port
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
        qname: str | DomainName,
        rdtype: int | str = "A",
        rdclass: int | str = 1,
        tcp: bool = False,
        source: str | None = None,
        raise_on_no_answer: bool = True,
        source_port: int = 0,
        lifetime: float | None = None,
        search: bool | None = None,
    ) -> Answer:
        return Resolver.resolve_answer(
            self,
            qname,
            rdtype,
            rdclass=rdclass,
            tcp=tcp,
            source=source,
            raise_on_no_answer=raise_on_no_answer,
            source_port=source_port,
            lifetime=lifetime,
            search=search,
        )

    def _resolve(self, *args, **kwargs) -> tuple[ResourceRecord, ...]:
        return Resolver.resolve_answer(self, *args, **kwargs).records

    def try_ddr(self, lifetime: float = 5.0) -> None:
        from .ddr import try_ddr

        try_ddr(self, lifetime=lifetime)

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
        source: str | None = None,
        source_port: int = 0,
    ) -> Answer:
        steps = self._resolve_steps(
            name,
            rdtype,
            search=search,
            lifetime=lifetime,
            rdclass=rdclass,
            tcp=tcp,
            raise_on_no_answer=raise_on_no_answer,
            use_cache=not (source is not None or source_port),
        )
        return _drive(
            steps,
            lambda operation: self._query(
                operation[0],
                operation[1],
                tcp=operation[2],
                edns_payload=None,
                want_dnssec=False,
                source=source,
                source_port=source_port,
                cache_response=False,
                include_endpoint=True,
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
        use_cache: bool = True,
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
        missing = NXDOMAIN(name)
        cache = self.cache if use_cache and not tcp and self._auth_key is None else None
        for candidate in dict.fromkeys(candidates):
            key = (DomainName((*candidate, b"")), question.type, question.rdclass)
            answer = None
            if isinstance(cache, Cache):
                answer = cache._get(key, age_answer=True)
            elif cache is not None:
                answer = cache.get(key)
            if answer is None:
                try:
                    answer = yield from self._name_steps(
                        Question(candidate, question.type, question.rdclass),
                        deadline,
                        tcp,
                    )
                except NoAnswer as exc:
                    answer = exc.answer
                    if answer is None:
                        last_no_data = exc
                        continue
                except NXDOMAIN as exc:
                    missing = missing + exc
                    continue
                if cache is not None:
                    cache.put(key, answer)
            if answer.rrset is not None:
                return answer
            last_no_data = NoAnswer(candidate, answer)
        if last_no_data is not None:
            if not raise_on_no_answer and last_no_data.answer is not None:
                return last_no_data.answer
            raise last_no_data
        raise missing

    def _name_steps(self, question: Question, deadline: float, tcp: bool):
        original = question
        seen = set()
        chain = []
        while True:
            response = yield question, deadline, tcp
            if isinstance(response, Message):
                message, endpoint, port = response, None, None
            else:
                message, endpoint, port = response
            if message.rcode == 3:
                qname = DomainName((*original.name, b""))
                raise NXDOMAIN(
                    qnames=(qname,),
                    responses={
                        qname: editable_message.QueryMessage._from_wire_message(message)
                    },
                )
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
                    minimum = min(rr.ttl for rr in (*answer, *chain))
                    return Answer(
                        original,
                        message,
                        DomainName((*question.name, b"")),
                        RRset(
                            question.name, question.rdclass, question.type, ttl, answer
                        ),
                        time() + minimum,
                        tuple(chain),
                        endpoint,
                        port,
                        minimum,
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
                                min(soa.ttl, decoded(soa)[-1])
                                if soa is not None
                                else 300
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
                                endpoint,
                                port,
                                ttl,
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

    def resolve_address(self, ipaddr, **kwargs) -> Answer:
        kwargs.update(rdtype=RecordType.PTR, rdclass=RecordClass.IN)
        return self.resolve(
            ipaddress.ip_address(ipaddr).reverse_pointer + ".", **kwargs
        )

    def resolve_name(self, name, family=socket.AF_UNSPEC, **kwargs) -> HostAnswers:
        return _drive(
            _host_steps(self, name, family, kwargs),
            lambda op: self.resolve(op[0], op[1], **op[2]),
        )

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

    def zone_for_name(
        self,
        name: str | DomainName,
        *,
        lifetime: float = 3,
        rdclass=RecordClass.IN,
        tcp=False,
    ) -> Name:
        return _drive(
            self._zone_steps(name, lifetime, rdclass, tcp),
            lambda operation: self._query(
                operation[0],
                operation[1],
                tcp=operation[2],
                edns_payload=None,
                want_dnssec=False,
            ),
        )

    def _zone_steps(self, name, lifetime, rdclass, tcp):
        if isinstance(name, DomainName):
            if not name.is_absolute():
                raise NotAbsolute("zone lookup requires an absolute name")
            owner = name.canonicalize().labels[:-1]
        else:
            owner = parse_name(name, canonical=True)
        deadline = deadline_after(lifetime)
        rdclass = record_class(rdclass)
        for start in range(len(owner) + 1):
            candidate = owner[start:]
            question = Question(candidate, RecordType.SOA, rdclass)
            response = yield question, deadline, tcp
            if response.rcode == 0 and any(
                rr.name == candidate
                and rr.type == RecordType.SOA
                and rr.rdclass == rdclass
                for rr in response.answers
            ):
                return candidate
            for rr in response.authority:
                if (
                    rr.type == RecordType.SOA
                    and rr.rdclass == rdclass
                    and rr.name != candidate
                    and is_subdomain(candidate, rr.name)
                ):
                    return rr.name
        raise NoRootSOA(f"could not find enclosing DNS zone for {name_text(owner)}")


class AsyncResolver(Resolver):
    """Awaitable resolver using the same wire and timeout semantics."""

    async def _async_query(self, question, deadline, backend, **options):
        async def execute(operation):
            if isinstance(operation, float):
                return await backend.sleep(operation)
            try:
                if isinstance(operation.server, Nameserver):
                    server = operation.server
                    options = dict(
                        request=operation.request,
                        timeout=operation.timeout,
                        source=operation.source,
                        source_port=operation.source_port,
                        max_size=operation.tcp,
                        backend=backend,
                    )
                    try:
                        return await server.async_query(**options)
                    except Truncated:
                        if operation.tcp or server.is_always_max_size():
                            raise
                        options["max_size"] = True
                        return await server.async_query(**options)
                options = {}
                if operation.source is not None or operation.source_port:
                    options.update(
                        source=operation.source, source_port=operation.source_port
                    )
                return await backend.query(
                    operation.request,
                    operation.server,
                    port=operation.port,
                    timeout=operation.timeout,
                    tcp=operation.tcp,
                    **options,
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

    async def _resolve_async_steps(
        self,
        steps,
        backend,
        *,
        source=None,
        source_port=0,
        cache_response=True,
        include_endpoint=False,
    ):
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
                source=source,
                source_port=source_port,
                cache_response=cache_response,
                include_endpoint=include_endpoint,
            )

        return await _drive_async(steps, execute)

    async def resolve(
        self,
        qname: str | DomainName,
        rdtype: int | str = "A",
        rdclass: int | str = 1,
        tcp: bool = False,
        source: str | None = None,
        raise_on_no_answer: bool = True,
        source_port: int = 0,
        lifetime: float | None = None,
        search: bool | None = None,
        backend=None,
    ) -> Answer:
        return await self.resolve_answer(
            qname,
            rdtype,
            rdclass=rdclass,
            tcp=tcp,
            source=source,
            raise_on_no_answer=raise_on_no_answer,
            source_port=source_port,
            lifetime=lifetime,
            search=search,
            backend=backend,
        )

    async def resolve_answer(
        self,
        *args,
        backend=None,
        source=None,
        source_port=0,
        **kwargs,
    ) -> Answer:
        return await self._resolve_async_steps(
            self._resolve_steps(
                *args, use_cache=not (source is not None or source_port), **kwargs
            ),
            backend,
            source=source,
            source_port=source_port,
            cache_response=False,
            include_endpoint=True,
        )

    async def try_ddr(self, lifetime: float = 5.0) -> None:
        from .ddr import try_ddr_async

        await try_ddr_async(self, lifetime=lifetime)

    async def resolve_address(self, ipaddr, **kwargs) -> Answer:
        kwargs.update(rdtype=RecordType.PTR, rdclass=RecordClass.IN)
        return await self.resolve(
            ipaddress.ip_address(ipaddr).reverse_pointer + ".", **kwargs
        )

    async def resolve_name(
        self, name, family=socket.AF_UNSPEC, **kwargs
    ) -> HostAnswers:
        return await _drive_async(
            _host_steps(self, name, family, kwargs),
            lambda op: self.resolve(op[0], op[1], **op[2]),
        )

    async def canonical_name(self, name, *, lifetime=3, backend=None) -> Name:
        return await self._resolve_async_steps(
            self._canonical_steps(name, lifetime), backend
        )

    async def zone_for_name(
        self,
        name,
        *,
        lifetime=3,
        backend=None,
        rdclass=RecordClass.IN,
        tcp=False,
    ) -> Name:
        return await self._resolve_async_steps(
            self._zone_steps(name, lifetime, rdclass, tcp), backend
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


def resolve(qname: str | DomainName, *args, **kwargs) -> Answer:
    return get_default_resolver().resolve(qname, *args, **kwargs)


def resolve_at(
    server: str,
    name: str,
    rdtype: int | str = "A",
    *,
    port: int = 53,
    lifetime: float = 3,
    **kwargs,
) -> Answer:
    return Resolver([server], port=port, timeout=lifetime).resolve(
        name, rdtype, lifetime=lifetime, **kwargs
    )
