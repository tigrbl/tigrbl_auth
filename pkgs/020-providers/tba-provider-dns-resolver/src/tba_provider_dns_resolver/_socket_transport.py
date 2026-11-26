"""DNS datagram and framed stream exchanges over native sockets."""

import ipaddress
import math
import socket
import ssl
from collections.abc import Iterator
from contextlib import contextmanager
from time import monotonic

from tba_codec_dns.wire import Message, Truncated, WireError, response_flags


class BadResponse(WireError):
    """The peer's DNS message does not answer the sent query."""


def deadline_after(timeout: float) -> float:
    if not math.isfinite(timeout) or timeout <= 0:
        raise ValueError("DNS timeout must be finite and positive")
    return monotonic() + timeout


def remaining(deadline: float | None) -> float | None:
    if deadline is None:
        return None
    delay = deadline - monotonic()
    if delay <= 0:
        raise TimeoutError("DNS query deadline elapsed")
    return delay


class DnsStream:
    def __init__(self, sock: socket.socket, deadline: float | None):
        self.sock = sock
        self.deadline = deadline

    def _read(self, size: int) -> bytes:
        data = bytearray()
        while len(data) < size:
            self.sock.settimeout(remaining(self.deadline))
            chunk = self.sock.recv(size - len(data))
            if not chunk:
                raise WireError("incomplete DNS stream frame")
            data.extend(chunk)
        return bytes(data)

    def send(self, packet: bytes) -> None:
        if not 12 <= len(packet) <= 65535:
            raise WireError("invalid DNS stream frame size")
        self.sock.settimeout(remaining(self.deadline))
        self.sock.sendall(len(packet).to_bytes(2, "big") + packet)

    def receive(self) -> bytes:
        length = int.from_bytes(self._read(2), "big")
        if length < 12:
            raise WireError("invalid DNS stream frame size")
        return self._read(length)


def _custom_query_sockets():
    # Resolve the mutable public factory for resolver and protocol callers too.
    from . import query

    return None if query.socket_factory is query.default_socket_factory else query


@contextmanager
def stream(
    server: str,
    port: int,
    deadline: float | None,
    *,
    server_name: str | None = None,
    context: ssl.SSLContext | None = None,
    source: tuple[str, int] | None = None,
    certificate_ip: str | None = None,
    connect=None,
) -> Iterator[DnsStream]:
    if connect is None:
        custom = _custom_query_sockets()
        if custom is not None:
            connect = custom._connect_stream
    if connect is None:
        options = {} if source is None else {"source_address": source}
        sock = socket.create_connection(
            (server, port), timeout=remaining(deadline), **options
        )
    else:
        sock = connect(server, port, deadline, source)
    with sock:
        if server_name is None and context is None and certificate_ip is None:
            yield DnsStream(sock, deadline)
        else:
            tls = tls_client_context(context)
            if certificate_ip is not None:
                _require_verified_context(tls)
            sock.settimeout(remaining(deadline))
            with tls.wrap_socket(sock, server_hostname=server_name or server) as secure:
                if certificate_ip is not None:
                    _check_tls_peer_ip(secure.getpeercert(), certificate_ip)
                yield DnsStream(secure, deadline)


def tls_client_context(context: ssl.SSLContext | None) -> ssl.SSLContext:
    if context is None:
        context = ssl.create_default_context()
        if context.minimum_version < ssl.TLSVersion.TLSv1_2:
            context.minimum_version = ssl.TLSVersion.TLSv1_2
    elif context.minimum_version < ssl.TLSVersion.TLSv1_2:
        raise ValueError("DNS-over-TLS requires TLS 1.2 or newer")
    return context


def _require_verified_context(context: ssl.SSLContext) -> None:
    if context.verify_mode != ssl.CERT_REQUIRED or not context.check_hostname:
        raise ValueError(
            "DNS certificate IP validation requires chain and hostname checks"
        )


def _check_tls_peer_ip(certificate: dict | None, address: str) -> None:
    expected = ipaddress.ip_address(address).packed
    if certificate and any(
        ipaddress.ip_address(value).packed == expected
        for kind, value in certificate.get("subjectAltName", ())
        if kind == "IP Address"
    ):
        return
    raise WireError("TLS certificate does not cover the original DNS resolver address")


@contextmanager
def _borrowed_stream(
    sock: socket.socket, deadline: float | None
) -> Iterator[DnsStream]:
    initial = sock.gettimeout()
    try:
        yield DnsStream(sock, deadline)
    finally:
        sock.settimeout(initial)


def send_tcp(
    sock: socket.socket, query: Message | bytes, *, timeout: float = 3
) -> tuple[int, float]:
    """Send a framed DNS message over a connected caller-owned stream."""
    packet = query if isinstance(query, bytes) else query.to_wire()
    with _borrowed_stream(sock, deadline_after(timeout)) as connection:
        connection.send(packet)
        return len(packet) + 2, monotonic()


def receive_tcp(
    sock: socket.socket, *, timeout: float = 3, ignore_trailing: bool = False
) -> tuple[Message, float]:
    """Read one DNS frame while leaving the stream available to its owner."""
    with _borrowed_stream(sock, deadline_after(timeout)) as connection:
        packet = connection.receive()
        received = monotonic()
        return Message.from_wire(packet, ignore_trailing=ignore_trailing), received


def check_response(
    query: Message,
    response: Message,
    *,
    allow_empty_question: bool = False,
    allow_truncated: bool = False,
) -> None:
    def normalized(questions):
        return tuple(
            (tuple(label.lower() for label in q.name), q.type, q.rdclass)
            for q in questions
        )

    if (
        response.flags & 0x8000 == 0
        or (response.flags & 0x0200 and not allow_truncated)
        or response.id != query.id
        or response.opcode != query.opcode
        or (
            normalized(response.questions) != normalized(query.questions)
            and not (allow_empty_question and not response.questions)
        )
    ):
        raise BadResponse("DNS response does not match the request")


def exchange_udp_packet(
    query: Message,
    packet: bytes,
    server: str,
    port: int,
    deadline: float,
    source: tuple[str, int] | None,
    *,
    ignore_errors: bool = True,
) -> bytes:
    if len(query.questions) != 1:
        raise ValueError("UDP query requires one DNS question")
    family, kind, protocol, _, address = socket.getaddrinfo(
        server, port, type=socket.SOCK_DGRAM, flags=socket.AI_NUMERICHOST
    )[0]
    question = Message.from_wire(packet).questions[0]
    custom = _custom_query_sockets()
    connection = (
        socket.socket(family, kind, protocol)
        if custom is None
        else custom.make_socket(family, kind, source)
    )
    with connection as sock:
        sock.settimeout(remaining(deadline))
        if source is not None and custom is None:
            sock.bind(source)
        sock.connect(address)
        sock.send(packet)
        while True:
            sock.settimeout(remaining(deadline))
            packet = sock.recv(65535)
            try:
                response_flags(
                    packet,
                    query.id,
                    question,
                    opcode=query.opcode,
                    allow_empty_question=query.opcode == 5,
                )
            except WireError:
                if not ignore_errors:
                    raise
                continue
            return packet


def send_udp(
    sock: socket.socket,
    query: Message | bytes,
    destination: tuple,
    *,
    timeout: float = 3,
) -> tuple[int, float]:
    """Send a DNS datagram through a caller-owned socket."""
    data = query if isinstance(query, bytes) else query.to_wire()
    if not 12 <= len(data) <= 65535:
        raise WireError("invalid DNS UDP packet size")
    deadline = deadline_after(timeout)
    initial = sock.gettimeout()
    try:
        sock.settimeout(remaining(deadline))
        count = sock.sendto(data, destination)
        if count != len(data):
            raise WireError("incomplete DNS UDP send")
        return count, monotonic()
    finally:
        sock.settimeout(initial)


def receive_udp(
    sock: socket.socket,
    *,
    timeout: float = 3,
    expected_peer: tuple | None = None,
    query: Message | None = None,
    ignore_unexpected: bool = True,
    ignore_errors: bool = False,
    ignore_trailing: bool = False,
    raise_on_truncation: bool = False,
) -> tuple[Message, float, tuple]:
    """Receive a DNS datagram and optionally check its endpoint and question."""
    deadline = deadline_after(timeout)
    initial = sock.gettimeout()
    try:
        while True:
            sock.settimeout(remaining(deadline))
            packet, peer = sock.recvfrom(65535)
            received = monotonic()
            if expected_peer is not None and peer != expected_peer:
                if ignore_unexpected:
                    continue
                raise UnexpectedSource("DNS response came from an unexpected endpoint")
            try:
                response = Message.from_wire(
                    packet,
                    question_only=bool(
                        raise_on_truncation and len(packet) >= 12 and packet[2] & 2
                    ),
                    ignore_trailing=ignore_trailing,
                )
                if query is not None:
                    check_response(
                        query,
                        response,
                        allow_empty_question=query.opcode == 5,
                        allow_truncated=True,
                    )
            except WireError:
                if ignore_errors:
                    continue
                raise
            if raise_on_truncation and response.flags & 0x0200:
                raise Truncated("truncated DNS UDP response", response)
            return response, received, peer
    finally:
        sock.settimeout(initial)


class UnexpectedSource(WireError):
    """A caller-owned datagram socket received DNS from a different endpoint."""


def udp_query(
    query: Message,
    server: str,
    *,
    port: int = 53,
    timeout: float = 3,
    source: tuple[str, int] | None = None,
    sock: socket.socket | None = None,
    ignore_unexpected: bool = True,
    ignore_errors: bool = True,
    ignore_trailing: bool = False,
    raise_on_truncation: bool = True,
) -> Message:
    deadline = deadline_after(timeout)
    if sock is not None:
        destination = socket.getaddrinfo(
            server,
            port,
            family=sock.family,
            type=socket.SOCK_DGRAM,
            flags=socket.AI_NUMERICHOST,
        )[0][4]
        send_udp(sock, query, destination, timeout=remaining(deadline))
        return receive_udp(
            sock,
            timeout=remaining(deadline),
            expected_peer=destination,
            query=query,
            ignore_unexpected=ignore_unexpected,
            ignore_errors=ignore_errors,
            ignore_trailing=ignore_trailing,
            raise_on_truncation=raise_on_truncation,
        )[0]
    packet = exchange_udp_packet(
        query,
        query.to_wire(),
        server,
        port,
        deadline,
        source,
        ignore_errors=ignore_errors,
    )
    result = Message.from_wire(
        packet, ignore_trailing=ignore_trailing, raise_on_truncation=raise_on_truncation
    )
    check_response(
        query, result, allow_empty_question=query.opcode == 5, allow_truncated=True
    )
    return result


def tcp_query(
    query: Message,
    server: str,
    *,
    port: int = 53,
    timeout: float = 3,
    source: tuple[str, int] | None = None,
    sock: socket.socket | None = None,
    ignore_trailing: bool = False,
) -> Message:
    return _tcp_query(
        query,
        query.to_wire(),
        server,
        port,
        deadline_after(timeout),
        source,
        sock=sock,
        ignore_trailing=ignore_trailing,
    )


def _tcp_query(
    query: Message,
    packet: bytes,
    server: str,
    port: int,
    deadline: float,
    source: tuple[str, int] | None,
    *,
    sock: socket.socket | None = None,
    ignore_trailing: bool = False,
) -> Message:
    channel = (
        stream(server, port, deadline, source=source)
        if sock is None
        else _borrowed_stream(sock, deadline)
    )
    with channel as connection:
        connection.send(packet)
        response = Message.from_wire(
            connection.receive(), ignore_trailing=ignore_trailing
        )
    check_response(query, response, allow_empty_question=query.opcode == 5)
    return response


def udp_with_fallback(
    query: Message,
    server: str,
    *,
    port: int = 53,
    timeout: float = 3,
    source: tuple[str, int] | None = None,
    tcp_sock: socket.socket | None = None,
    udp_sock: socket.socket | None = None,
    ignore_trailing: bool = False,
) -> tuple[Message, bool]:
    deadline = deadline_after(timeout)
    try:
        result = udp_query(
            query,
            server,
            port=port,
            timeout=remaining(deadline),
            source=source,
            sock=udp_sock,
            ignore_trailing=ignore_trailing,
        )
    except Truncated:
        return _tcp_query(
            query,
            query.to_wire(),
            server,
            port,
            deadline,
            source,
            sock=tcp_sock,
            ignore_trailing=ignore_trailing,
        ), True
    return result, False


def tls_query(
    query: Message,
    server: str,
    *,
    port: int = 853,
    timeout: float = 3,
    server_name: str | None = None,
    context: ssl.SSLContext | None = None,
    source: tuple[str, int] | None = None,
    sock: ssl.SSLSocket | None = None,
    ignore_trailing: bool = False,
    certificate_ip: str | None = None,
) -> Message:
    deadline = deadline_after(timeout)
    if sock is None:
        channel = stream(
            server,
            port,
            deadline,
            server_name=server_name or server,
            context=context,
            source=source,
            certificate_ip=certificate_ip,
        )
    else:
        if not isinstance(sock, ssl.SSLSocket):
            raise TypeError("DoT requires a connected TLS socket")
        if certificate_ip is not None:
            _require_verified_context(sock.context)
            _check_tls_peer_ip(sock.getpeercert(), certificate_ip)
        channel = _borrowed_stream(sock, deadline)
    with channel as connection:
        connection.send(query.to_wire())
        response = Message.from_wire(
            connection.receive(), ignore_trailing=ignore_trailing
        )
    check_response(query, response)
    return response
