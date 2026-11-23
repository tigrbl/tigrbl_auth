"""Synchronous DNS query and borrowed-socket APIs."""

import asyncio
import socket
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager, nullcontext
from dataclasses import replace
from importlib.metadata import entry_points
from importlib.util import find_spec
from time import monotonic, time
from urllib.parse import urlsplit

from tba_codec_dns import message, wire

from . import _socket_transport as sockets
from . import _doh, _quic
from ._doh import HTTPVersion as HTTPVersion
from ._doh import NoDOH as NoDOH
from .asyncquery import (
    BadResponse as BadResponse,
    UDPMode as UDPMode,
    UnexpectedSource as UnexpectedSource,
    _packet,
    _result,
    _tls_context,
    _wire_query,
)

have_doh = find_spec("httpx") is not None


class NoDOQ(wire.WireError):
    """The DNS-over-QUIC transport is unavailable."""


def default_socket_factory(af, kind, proto):
    """Create a native socket for a synchronous DNS exchange."""
    return socket.socket(af, kind, proto)


socket_factory = default_socket_factory


def make_socket(af, type, source=None):
    """Create a nonblocking socket, optionally bound to a source endpoint."""
    sock = socket_factory(af, type, 0)
    try:
        sock.setblocking(False)
        if source is not None:
            sock.bind(source)
        return sock
    except BaseException:
        sock.close()
        raise


def make_ssl_socket(af, type, ssl_context, server_hostname=None, source=None):
    """Wrap a factory socket for a deferred TLS handshake."""
    if hasattr(server_hostname, "to_text"):
        server_hostname = server_hostname.to_text()
    sock = make_socket(af, type, source)
    try:
        return ssl_context.wrap_socket(
            sock, server_hostname=server_hostname, do_handshake_on_connect=False
        )
    except BaseException:
        sock.close()
        raise


def _connect_stream(server, port, deadline, source):
    error = None
    for family, kind, _, _, address in socket.getaddrinfo(
        server, port, type=socket.SOCK_STREAM
    ):
        try:
            sock = make_socket(family, kind, source)
            try:
                sock.settimeout(sockets.remaining(deadline))
                sock.connect(address)
                return sock
            except BaseException:
                sock.close()
                raise
        except OSError as exc:
            error = exc
    if error is not None:
        raise error
    raise OSError("no IP addresses for the DNS server")


def _deadline(timeout):
    return None if timeout is None else sockets.deadline_after(timeout)


def _run_exchange(exchange):
    """Drive an owned async transport from the blocking API."""
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        pass
    else:
        with ThreadPoolExecutor(max_workers=1) as worker:
            return worker.submit(asyncio.run, exchange).result()
    return asyncio.run(exchange)


def _encrypted_request(q, one_rr_per_rrset, ignore_trailing):
    request, key = _wire_query(q, _packet(q))
    options = dict(one_rr_per_rrset=one_rr_per_rrset, ignore_trailing=ignore_trailing)
    if request.had_tsig:
        if key is None:
            raise ValueError("a signed DNS query requires its TSIG key")
        options.update(keyring=key, request_mac=request.mac)
    return request, options


def _zero_identifier(q):
    if isinstance(q, message.Message):
        q.set_id(0)
    elif q._sign_on_wire and q.id != 0 and not q.had_tsig:
        return replace(q, id=0, _original_id=0)
    return q


def _check_http_status(status, _content_type=None):
    if not 200 <= status < 300:
        raise wire.WireError(f"unexpected DNS HTTPS response ({status})")


def https(
    q,
    where,
    timeout=None,
    port=443,
    source=None,
    source_port=0,
    one_rr_per_rrset=False,
    ignore_trailing=False,
    session=None,
    path="/dns-query",
    post=True,
    bootstrap_address=None,
    verify=True,
    resolver=None,
    family=socket.AF_UNSPEC,
    http_version=HTTPVersion.DEFAULT,
):
    """Send a DNS query over HTTPS, optionally borrowing a synchronous session."""
    version = HTTPVersion(http_version)
    if "://" not in where:
        host = f"[{where}]" if ":" in where and not where.startswith("[") else where
        where = f"https://{host}:{port}{path}"
    target = urlsplit(where)
    if (
        target.scheme != "https"
        or not target.hostname
        or target.username is not None
        or target.fragment
    ):
        raise ValueError(
            "DoH requires an HTTPS endpoint without credentials or a fragment"
        )
    h3, httpx, h2 = _doh._https_transport(version, session, have_doh)
    if bootstrap_address is None and session is None and (h3 or resolver is not None):
        if h3:
            bootstrap_address = _doh._literal_address(target.hostname)
            if bootstrap_address is None and resolver is None:
                from .resolver import get_default_resolver

                resolver = get_default_resolver()
        if bootstrap_address is None:
            answer = resolver.resolve_name(target.hostname, family=family)
            addresses = answer.addresses() if hasattr(answer, "addresses") else answer
            bootstrap_address = str(next(iter(addresses)))
    begin = time()
    if h3:
        request, options = _encrypted_request(
            _zero_identifier(q), one_rr_per_rrset, ignore_trailing
        )
        response = _https3(
            request,
            where,
            timeout,
            source,
            source_port,
            post,
            bootstrap_address,
            verify,
            session,
            options,
        )
    else:
        request, options = _encrypted_request(q, one_rr_per_rrset, ignore_trailing)
        response = _https12(
            request,
            where,
            timeout,
            source,
            source_port,
            post,
            bootstrap_address,
            verify,
            session,
            options,
            family,
            httpx,
            version != HTTPVersion.H2,
            h2,
        )
    return _result(q, response, time() - begin)


def _https12(
    query,
    url,
    timeout,
    source,
    source_port,
    post,
    bootstrap_address,
    verify,
    session,
    options,
    family,
    httpx,
    h1,
    h2,
):
    target, method, path, headers, body = _doh._https_request(
        query, url, post, zero_id=False
    )
    url = f"https://{target.netloc}{path}"
    if session is None and (
        source_port or bootstrap_address is not None or family != socket.AF_UNSPEC
    ):
        from ._https2 import bootstrap_query

        async def exchange():
            return await bootstrap_query(
                query,
                url,
                method,
                headers,
                body,
                _tls_context(verify),
                bootstrap_address,
                None,
                options,
                source=source,
                source_port=source_port,
                family=family,
                http1=h1,
                http2=h2,
                zero_id=False,
                check_status=_check_http_status,
            )

        return _run_exchange(_doh._wait_http_exchange(exchange, _deadline(timeout)))
    if session is None:
        context = httpx.Client(
            transport=httpx.HTTPTransport(
                verify=_tls_context(verify),
                http1=h1,
                http2=h2,
                local_address=source,
            )
        )
    elif isinstance(session, httpx.Client):
        context = nullcontext(session)
    else:
        raise ValueError("session must be a synchronous HTTP client")

    with (
        context as client,
        client.stream(
            method,
            url,
            headers=headers,
            content=body,
            timeout=timeout,
            follow_redirects=False,
        ) as reply,
    ):
        _check_http_status(reply.status_code)
        data = bytearray()
        for chunk in reply.iter_raw():
            _doh._extend_https(data, chunk)
    return _doh._https_response(query, data, options, zero_id=False)


def _https3(
    query,
    url,
    timeout,
    source,
    source_port,
    post,
    bootstrap_address,
    verify,
    session,
    options,
):
    deadline = _deadline(timeout)
    if session is None:
        from .quic import SyncQuicManager

        target = urlsplit(url)
        with SyncQuicManager(
            verify_mode=verify, server_name=target.hostname, h3=True
        ) as manager:
            peer = manager.connect(
                bootstrap_address or target.hostname,
                target.port or 443,
                source,
                source_port,
            )
            return _exchange_h3(query, url, post, options, peer, deadline)
    if not hasattr(session, "make_stream"):
        raise ValueError("session must support synchronous HTTP/3 streams")
    return _exchange_h3(query, url, post, options, session, deadline, timeout)


def _exchange_h3(query, url, post, options, session, deadline, timeout=None):
    stream_timeout = sockets.remaining(deadline) if timeout is None else timeout
    with session.make_stream(stream_timeout) as channel:
        channel.send_h3(url, _quic._zero_id_request(query).to_wire(), post)
        data = channel.receive(sockets.remaining(deadline))
        fields = dict(channel.headers())
    status = fields.get(b":status", fields.get(":status", 0))
    _check_http_status(int(status))
    payload = bytearray()
    _doh._extend_https(payload, data)
    return _doh._https_response(query, payload, options)


def quic(
    q,
    where,
    timeout=None,
    port=853,
    source=None,
    source_port=0,
    one_rr_per_rrset=False,
    ignore_trailing=False,
    connection=None,
    verify=True,
    hostname=None,
    server_hostname=None,
):
    """Exchange a DNS message over QUIC using an owned or borrowed connection."""
    begin = time()
    query, options = _encrypted_request(
        _zero_identifier(q), one_rr_per_rrset, ignore_trailing
    )
    request = _quic._doq_request(query)
    deadline = _deadline(timeout)
    if connection is None:
        from .quic import SyncQuicManager, have_quic

        if not have_quic:
            raise NoDOQ("DNS-over-QUIC requires the quic extra")
        name = server_hostname if hostname is None else hostname
        with SyncQuicManager(verify_mode=verify, server_name=name) as manager:
            connection = manager.connect(where, port, source, source_port)
            with connection.make_stream(sockets.remaining(deadline)) as channel:
                channel.send(request.to_wire(), True)
                data = channel._receive_response(sockets.remaining(deadline))
    else:
        with connection.make_stream(timeout) as channel:
            channel.send(request.to_wire(), True)
            data = channel.receive(sockets.remaining(deadline))
    response = wire.Message.from_wire(data, **options)
    if not request.is_response(response):
        raise BadResponse("unrelated DNS QUIC response")
    response = _quic._restore_id(response, query.id)
    return _result(q, response, time() - begin)


def _transfer_api(name):
    implementations = entry_points(group="tba.dns.inbound_xfr", name=name)
    if len(implementations) != 1:
        raise RuntimeError(f"{name} requires the tba-protocol-dns package")
    return next(iter(implementations)).load()


def xfr(
    where,
    zone,
    rdtype=wire.RecordType.AXFR,
    rdclass=wire.RecordClass.IN,
    timeout=None,
    port=53,
    keyring=None,
    keyname=None,
    relativize=True,
    lifetime=None,
    source=None,
    source_port=0,
    serial=0,
    use_udp=False,
    keyalgorithm="hmac-sha256.",
    raise_on_serial_went_backwards=True,
):
    """Yield the messages of an AXFR or IXFR in wire order."""
    yield from _transfer_api("xfr")(
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
    )


def inbound_xfr(
    where,
    txn_manager,
    query=None,
    port=53,
    timeout=None,
    lifetime=None,
    source=None,
    source_port=0,
    udp_mode=UDPMode.NEVER,
    raise_on_serial_went_backwards=True,
):
    """Receive and transactionally apply an AXFR or IXFR."""
    _transfer_api("sync")(
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
    )


def _monotonic_expiration(expiration):
    return None if expiration is None else monotonic() + expiration - time()


@contextmanager
def _socket_timeout(sock, deadline):
    original = sock.gettimeout()
    try:
        sock.settimeout(sockets.remaining(deadline))
        yield
    finally:
        sock.settimeout(original)


def send_udp(sock, what, destination, expiration=None):
    with _socket_timeout(sock, _monotonic_expiration(expiration)):
        packet = _packet(what)
        sent = time()
        count = (
            sock.send(packet)
            if destination is None
            else sock.sendto(packet, destination)
        )
    return count, sent


def _receive_udp(
    sock, deadline, destination, ignore_unexpected, parse_options, ignore_errors, query
):
    with _socket_timeout(sock, deadline):
        while True:
            sock.settimeout(sockets.remaining(deadline))
            packet, peer = sock.recvfrom(65535)
            received = time()
            if destination is not None and peer != destination:
                if ignore_unexpected:
                    continue
                raise UnexpectedSource("DNS response came from an unexpected endpoint")
            try:
                response = wire.Message.from_wire(packet, **parse_options)
                if query is not None and not query.is_response(response):
                    raise BadResponse("DNS response does not match the request")
            except wire.Truncated as exc:
                if query is None or (
                    exc.partial is not None and query.is_response(exc.partial)
                ):
                    raise
                if not ignore_errors:
                    raise BadResponse(
                        "truncated reply does not match the query"
                    ) from exc
                continue
            except wire.WireError:
                if not ignore_errors:
                    raise
                continue
            return response, received, peer


def receive_udp(
    sock,
    destination=None,
    expiration=None,
    ignore_unexpected=False,
    one_rr_per_rrset=False,
    keyring=None,
    request_mac=b"",
    ignore_trailing=False,
    raise_on_truncation=False,
    ignore_errors=False,
    query=None,
):
    expected = query._wire_message() if isinstance(query, message.Message) else query
    options = dict(
        one_rr_per_rrset=one_rr_per_rrset,
        keyring=keyring,
        request_mac=request_mac,
        ignore_trailing=ignore_trailing,
        raise_on_truncation=raise_on_truncation,
    )
    packet, received, peer = _receive_udp(
        sock,
        _monotonic_expiration(expiration),
        destination,
        ignore_unexpected,
        options,
        ignore_errors,
        expected if ignore_errors else None,
    )
    result = message.Message._from_wire_message(packet), received
    return (*result, peer) if destination is None else result


def udp(
    q,
    where,
    timeout=None,
    port=53,
    source=None,
    source_port=0,
    ignore_unexpected=False,
    one_rr_per_rrset=False,
    ignore_trailing=False,
    raise_on_truncation=False,
    sock=None,
    ignore_errors=False,
):
    deadline = _deadline(timeout)
    return _udp(
        q,
        where,
        deadline,
        port,
        source,
        source_port,
        ignore_unexpected,
        one_rr_per_rrset,
        ignore_trailing,
        raise_on_truncation,
        sock,
        ignore_errors,
    )


def _source(family, source, port):
    if source is None and not port:
        return None
    return source or ("::" if family == socket.AF_INET6 else "0.0.0.0"), port


@contextmanager
def _datagram(sock, family, source, source_port):
    if sock is not None:
        yield sock
        return
    with make_socket(
        family, socket.SOCK_DGRAM, _source(family, source, source_port)
    ) as owned:
        yield owned


def _udp(
    q,
    where,
    deadline,
    port,
    source,
    source_port,
    ignore_unexpected,
    one_rr_per_rrset,
    ignore_trailing,
    raise_on_truncation,
    sock,
    ignore_errors,
):
    begin = time()
    packet = _packet(q)
    query, key = _wire_query(q, packet)
    family, _, _, _, destination = socket.getaddrinfo(
        where,
        port,
        family=0 if sock is None else sock.family,
        type=socket.SOCK_DGRAM,
        flags=socket.AI_NUMERICHOST,
    )[0]
    options = dict(
        one_rr_per_rrset=one_rr_per_rrset,
        ignore_trailing=ignore_trailing,
        raise_on_truncation=raise_on_truncation,
    )
    if key is not None:
        options.update(keyring=key, request_mac=query.mac)
    with _datagram(sock, family, source, source_port) as connection:
        with _socket_timeout(connection, deadline):
            connection.sendto(packet, destination)
        response, received, _ = _receive_udp(
            connection,
            deadline,
            destination,
            ignore_unexpected,
            options,
            ignore_errors,
            query,
        )
    return _result(q, response, received - begin)


def send_tcp(sock, what, expiration=None):
    packet = _packet(what)
    sent = time()
    with sockets._borrowed_stream(sock, _monotonic_expiration(expiration)) as channel:
        channel.send(packet)
    return len(packet) + 2, sent


def receive_tcp(
    sock,
    expiration=None,
    one_rr_per_rrset=False,
    keyring=None,
    request_mac=b"",
    ignore_trailing=False,
):
    with sockets._borrowed_stream(sock, _monotonic_expiration(expiration)) as channel:
        packet = channel.receive()
        received = time()
    response = message.from_wire(
        packet,
        one_rr_per_rrset=one_rr_per_rrset,
        keyring=keyring,
        request_mac=request_mac,
        ignore_trailing=ignore_trailing,
    )
    return response, received


def _stream(
    q,
    where,
    deadline,
    port,
    source,
    source_port,
    one_rr_per_rrset,
    ignore_trailing,
    sock,
    context=None,
    hostname=None,
):
    begin = time()
    packet = _packet(q)
    query, key = _wire_query(q, packet)
    if sock is None:
        family = socket.AF_INET6 if ":" in where else socket.AF_INET
        channel = sockets.stream(
            where,
            port,
            deadline,
            source=_source(family, source, source_port),
            context=context,
            server_name=hostname,
            connect=_connect_stream,
        )
    else:
        sock.getpeername()
        channel = sockets._borrowed_stream(sock, deadline)
    with channel as connection:
        connection.send(packet)
        response_packet = connection.receive()
        received = time()
    options = dict(one_rr_per_rrset=one_rr_per_rrset, ignore_trailing=ignore_trailing)
    if key is not None:
        options.update(keyring=key, request_mac=query.mac)
    response = wire.Message.from_wire(response_packet, **options)
    if not query.is_response(response):
        raise BadResponse("DNS response does not match the request")
    return _result(q, response, received - begin)


def tcp(
    q,
    where,
    timeout=None,
    port=53,
    source=None,
    source_port=0,
    one_rr_per_rrset=False,
    ignore_trailing=False,
    sock=None,
):
    return _stream(
        q,
        where,
        _deadline(timeout),
        port,
        source,
        source_port,
        one_rr_per_rrset,
        ignore_trailing,
        sock,
    )


def tls(
    q,
    where,
    timeout=None,
    port=853,
    source=None,
    source_port=0,
    one_rr_per_rrset=False,
    ignore_trailing=False,
    sock=None,
    ssl_context=None,
    server_hostname=None,
    verify=True,
):
    context = None if sock is not None else ssl_context or _tls_context(verify)
    return _stream(
        q,
        where,
        _deadline(timeout),
        port,
        source,
        source_port,
        one_rr_per_rrset,
        ignore_trailing,
        sock,
        context,
        server_hostname,
    )


def udp_with_fallback(
    q,
    where,
    timeout=None,
    port=53,
    source=None,
    source_port=0,
    ignore_unexpected=False,
    one_rr_per_rrset=False,
    ignore_trailing=False,
    udp_sock=None,
    tcp_sock=None,
    ignore_errors=False,
):
    deadline = _deadline(timeout)
    try:
        response = _udp(
            q,
            where,
            deadline,
            port,
            source,
            source_port,
            ignore_unexpected,
            one_rr_per_rrset,
            ignore_trailing,
            True,
            udp_sock,
            ignore_errors,
        )
        return response, False
    except wire.Truncated:
        response = _stream(
            q,
            where,
            deadline,
            port,
            source,
            source_port,
            one_rr_per_rrset,
            ignore_trailing,
            tcp_sock,
        )
        return response, True
