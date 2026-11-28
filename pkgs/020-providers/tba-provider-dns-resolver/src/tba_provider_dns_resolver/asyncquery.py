"""Asynchronous DNS query API with borrowed sockets and absolute deadlines."""

import os
import socket
import ssl
from contextlib import AsyncExitStack
from dataclasses import replace
from enum import IntEnum
from importlib.metadata import entry_points
from importlib.util import find_spec
from time import monotonic, time
from urllib.parse import urlsplit

from tba_codec_dns import message, wire

from . import _doh, _quic
from . import async_transport as transport
from ._doh import HTTPVersion as HTTPVersion
from ._doh import NoDOH as NoDOH
from ._http3_tls import HTTP3SSLContext as HTTP3SSLContext
from ._http3_tls import (
    configure_http3_client_identity as configure_http3_client_identity,
)
from ._http3_tls import configure_http3_crls as configure_http3_crls
from ._socket_transport import BadResponse as BadResponse
from .asyncbackend import get_default_backend


UnexpectedSource = transport.transport.UnexpectedSource
have_doh = find_spec("httpx") is not None


class UDPMode(IntEnum):
    NEVER = 0
    TRY_FIRST = 1
    ONLY = 2


def _monotonic_expiration(expiration):
    return None if expiration is None else monotonic() + (expiration - time())


def _expiration(timeout):
    return None if timeout is None else time() + timeout


def _remaining(expiration):
    if expiration is None:
        return None
    delay = expiration - time()
    if delay <= 0:
        raise TimeoutError("DNS query timed out")
    return delay


def _source(family, source, port):
    if source is None and not port:
        return None
    address = source or ("::" if family == socket.AF_INET6 else "0.0.0.0")
    return socket.getaddrinfo(address, port, family, 0, 0, socket.AI_NUMERICHOST)[0][4]


def _address(where, port, socktype):
    return socket.getaddrinfo(where, port, 0, socktype, 0, socket.AI_NUMERICHOST)[0]


def _packet(what):
    return (
        what.to_wire()
        if isinstance(what, (message.Message, wire.Message))
        else bytes(what)
    )


def _wire_query(q, packet):
    query = wire.Message.from_wire(packet)
    key = q.keyring if isinstance(q, message.Message) else q.tsig_key
    return replace(query, tsig_key=key), key


def _prepare_zero_id_tsig(q):
    """Set the transport identifier before rendering a TSIG-configured query."""
    if isinstance(q, message.Message):
        if q._state._sign_on_wire:
            q.set_id(0)
    elif q._sign_on_wire:
        return _quic._zero_id_request(q)
    return q


def _result(q, received, elapsed):
    result = (
        message.Message._from_wire_message(received)
        if isinstance(q, message.Message)
        else received
    )
    # Wire messages remain value objects. Timing does not participate in equality.
    if isinstance(result, wire.Message):
        return replace(result, time=elapsed)
    result.time = elapsed
    return result


async def send_udp(sock, what, destination, expiration=None):
    sent, _ = await transport.send_udp(
        sock, _packet(what), destination, _monotonic_expiration(expiration)
    )
    return sent, time()


async def receive_udp(
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
    query = query._wire_message() if isinstance(query, message.Message) else query
    result, _, address = await transport.receive_udp(
        sock,
        destination,
        _monotonic_expiration(expiration),
        ignore_unexpected,
        one_rr_per_rrset,
        keyring,
        request_mac,
        ignore_trailing,
        raise_on_truncation,
        ignore_errors,
        query,
    )
    return result, time(), address


async def send_tcp(sock, what, expiration=None):
    sent, _ = await transport.send_tcp(
        sock, _packet(what), _monotonic_expiration(expiration)
    )
    return sent, time()


async def receive_tcp(
    sock,
    expiration=None,
    one_rr_per_rrset=False,
    keyring=None,
    request_mac=b"",
    ignore_trailing=False,
):
    result, _ = await transport.receive_tcp(
        sock,
        _monotonic_expiration(expiration),
        one_rr_per_rrset,
        keyring,
        request_mac,
        ignore_trailing,
    )
    return result, time()


async def udp(
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
    backend=None,
    ignore_errors=False,
):
    begin = time()
    expiration = _expiration(timeout)
    packet = _packet(q)
    query, key = _wire_query(q, packet)
    family, kind, proto, _, address = _address(where, port, socket.SOCK_DGRAM)
    async with AsyncExitStack() as stack:
        if sock is None:
            backend = backend if backend is not None else get_default_backend()
            peer = address if backend.datagram_connection_required() else None
            sock = await backend.make_socket(
                family,
                kind,
                proto,
                _source(family, source, source_port),
                peer,
            )
            await stack.enter_async_context(sock)
        destination = None if await sock.getpeername() is not None else address
        await send_udp(sock, packet, destination, expiration)
        received, received_at, _ = await receive_udp(
            sock,
            address,
            expiration,
            ignore_unexpected,
            one_rr_per_rrset,
            key,
            query.mac,
            ignore_trailing,
            raise_on_truncation,
            ignore_errors,
            query,
        )
        if not query.is_response(received):
            raise BadResponse("unrelated DNS response")
        return _result(q, received, received_at - begin)


async def udp_with_fallback(
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
    backend=None,
    ignore_errors=False,
):
    expiration = _expiration(timeout)
    try:
        result = await udp(
            q,
            where,
            timeout,
            port,
            source,
            source_port,
            ignore_unexpected,
            one_rr_per_rrset,
            ignore_trailing,
            True,
            udp_sock,
            backend,
            ignore_errors,
        )
        return result, False
    except wire.Truncated:
        result = await tcp(
            q,
            where,
            _remaining(expiration),
            port,
            source,
            source_port,
            one_rr_per_rrset,
            ignore_trailing,
            tcp_sock,
            backend,
        )
        return result, True


async def _stream(
    q,
    where,
    timeout,
    port,
    source,
    source_port,
    one_rr_per_rrset,
    ignore_trailing,
    sock,
    backend,
    context=None,
    hostname=None,
):
    begin = time()
    expiration = _expiration(timeout)
    packet = _packet(q)
    query, key = _wire_query(q, packet)
    async with AsyncExitStack() as stack:
        if sock is None:
            backend = backend if backend is not None else get_default_backend()
            family, kind, proto, _, address = _address(where, port, socket.SOCK_STREAM)
            sock = await backend.make_socket(
                family,
                kind,
                proto,
                _source(family, source, source_port),
                address,
                _remaining(expiration),
                context,
                hostname,
            )
            await stack.enter_async_context(sock)
        await send_tcp(sock, packet, expiration)
        received, received_at = await receive_tcp(
            sock,
            expiration,
            one_rr_per_rrset,
            key,
            query.mac,
            ignore_trailing,
        )
    if not query.is_response(received):
        raise BadResponse("unrelated DNS response")
    return _result(q, received, received_at - begin)


async def tcp(
    q,
    where,
    timeout=None,
    port=53,
    source=None,
    source_port=0,
    one_rr_per_rrset=False,
    ignore_trailing=False,
    sock=None,
    backend=None,
):
    return await _stream(
        q,
        where,
        timeout,
        port,
        source,
        source_port,
        one_rr_per_rrset,
        ignore_trailing,
        sock,
        backend,
    )


def _tls_context(verify):
    if isinstance(verify, ssl.SSLContext):
        return verify
    context = ssl.create_default_context(
        cafile=os.fspath(verify) if isinstance(verify, (str, os.PathLike)) else None
    )
    if verify is False:
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
    return context


async def tls(
    q,
    where,
    timeout=None,
    port=853,
    source=None,
    source_port=0,
    one_rr_per_rrset=False,
    ignore_trailing=False,
    sock=None,
    backend=None,
    ssl_context=None,
    server_hostname=None,
    verify=True,
):
    context = None if sock is not None else (ssl_context or _tls_context(verify))
    return await _stream(
        q,
        where,
        timeout,
        port,
        source,
        source_port,
        one_rr_per_rrset,
        ignore_trailing,
        sock,
        backend,
        context,
        server_hostname or where,
    )


async def https(
    q,
    where,
    timeout=None,
    port=443,
    source=None,
    source_port=0,
    one_rr_per_rrset=False,
    ignore_trailing=False,
    client=None,
    path="/dns-query",
    post=True,
    verify=True,
    bootstrap_address=None,
    resolver=None,
    family=socket.AF_UNSPEC,
    http_version=HTTPVersion.DEFAULT,
):
    version = HTTPVersion(http_version)
    use_h3, httpx, use_h2 = _doh._https_transport(version, client, have_doh)
    parse_options = dict(
        one_rr_per_rrset=one_rr_per_rrset, ignore_trailing=ignore_trailing
    )
    if "://" not in where:
        host = f"[{where}]" if ":" in where and not where.startswith("[") else where
        where = f"https://{host}:{port}{path}"
    target = urlsplit(where)
    if target.scheme != "https" or target.hostname is None:
        raise ValueError("DNS over HTTPS requires an HTTPS endpoint")
    begin = time()
    if use_h3:
        q = _prepare_zero_id_tsig(q)
    packet = _packet(q)
    query, key = _wire_query(q, packet)
    if (
        bootstrap_address is None
        and client is None
        and (use_h3 or resolver is not None)
    ):
        from .client import AsyncResolver

        if use_h3:
            bootstrap_address = _doh._literal_address(target.hostname)
            if bootstrap_address is None and resolver is None:
                from .asyncresolver import get_default_resolver

                resolver = get_default_resolver()
        if bootstrap_address is None:
            lookup_family = (
                {socket.AF_UNSPEC: 0, socket.AF_INET: 4, socket.AF_INET6: 6}.get(
                    family, family
                )
                if isinstance(resolver, AsyncResolver)
                else family
            )
            answer = await resolver.resolve_name(target.hostname, family=lookup_family)
            addresses = answer.addresses() if hasattr(answer, "addresses") else answer
            bootstrap_address = str(next(iter(addresses)))
    if use_h3:
        if key is not None:
            parse_options.update(keyring=key, request_mac=query.mac)
        if client is not None:
            if hasattr(client, "make_stream"):
                expiration = _expiration(timeout)
                request = _quic._zero_id_request(query)
                async with await client.make_stream(_remaining(expiration)) as stream:
                    stream.send_h3(where, request.to_wire(), post)
                    data = await stream.receive(_remaining(expiration))
                    fields = dict(stream.headers())
                    status = fields.get(b":status", fields.get(":status", 0))
                    content_type = fields.get(
                        b"content-type", fields.get("content-type", "")
                    )
                    if isinstance(content_type, bytes):
                        content_type = content_type.decode("ascii")
                    _doh._check_https_status(int(status), content_type)
                    if len(data) > 65535:
                        raise wire.WireError(
                            "DNS HTTPS response exceeds the wire limit"
                        )
                response = _doh._https_response(query, data, parse_options)
            elif hasattr(client, "query"):
                response = await client.query(query, timeout=timeout)
                if not query.is_response(response):
                    raise BadResponse("unrelated DNS HTTPS response")
            else:
                raise TypeError("HTTP/3 client must support HTTP/3 streams")
        else:
            response = await transport.https_query(
                query,
                where,
                timeout=timeout,
                http_version=3,
                context=verify if isinstance(verify, ssl.SSLContext) else None,
                local_address=source,
                local_port=source_port,
                post=post,
                ca_file=os.fspath(verify)
                if isinstance(verify, (str, os.PathLike))
                else None,
                verify=verify is not False,
                bootstrap_address=bootstrap_address,
                parse_options=parse_options,
            )
        return _result(q, response, time() - begin)
    if client is None and (
        source_port or bootstrap_address is not None or family != socket.AF_UNSPEC
    ):
        from ._https2 import bootstrap_query

        _, method, request_path, headers, body = _doh._https_request(query, where, post)
        if key is not None:
            parse_options.update(keyring=key, request_mac=query.mac)

        async def exchange():
            return await bootstrap_query(
                query,
                f"https://{target.netloc}{request_path}",
                method,
                headers,
                body,
                _tls_context(verify),
                bootstrap_address,
                None,
                parse_options,
                source=source,
                source_port=source_port,
                family=family,
                http1=version != HTTPVersion.HTTP_2,
                http2=use_h2,
            )

        response = await _doh._wait_http_exchange(exchange, _doh._deadline(timeout))
        return _result(q, response, time() - begin)

    _, method, request_path, headers, body = _doh._https_request(query, where, post)
    async with AsyncExitStack() as stack:
        if client is None:
            h1 = version in (HTTPVersion.DEFAULT, HTTPVersion.HTTP_1)
            factory = get_default_backend().get_transport_class()
            client = await stack.enter_async_context(
                httpx.AsyncClient(
                    transport=factory(
                        verify=_tls_context(verify),
                        http1=h1,
                        http2=use_h2,
                        local_address=source,
                    ),
                )
            )
        async with client.stream(
            method,
            f"https://{target.netloc}{request_path}",
            headers=headers,
            content=body,
            timeout=timeout,
            follow_redirects=False,
        ) as reply:
            _doh._check_session_response(reply, version)
            data = bytearray()
            async for chunk in reply.aiter_raw():
                _doh._extend_https(data, chunk)
    response = wire.Message.from_wire(
        bytes(data),
        one_rr_per_rrset=one_rr_per_rrset,
        ignore_trailing=ignore_trailing,
    )
    if not replace(query, id=0).is_response(response):
        raise BadResponse("unrelated DNS HTTPS response")
    return _result(q, _quic._restore_id(response, query.id), time() - begin)


async def quic(
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
    backend=None,
    hostname=None,
    server_hostname=None,
):
    begin = time()
    q = _prepare_zero_id_tsig(q)
    packet = _packet(q)
    query, key = _wire_query(q, packet)
    request = _quic._doq_request(query)
    if connection is not None and hasattr(connection, "make_stream"):
        expiration = _expiration(timeout)
        async with await connection.make_stream(timeout) as stream:
            await stream.send(request.to_wire(), True)
            data = await stream.receive(_remaining(expiration))
        response = wire.Message.from_wire(
            data,
            one_rr_per_rrset=one_rr_per_rrset,
            ignore_trailing=ignore_trailing,
            **({} if key is None else {"keyring": key, "request_mac": query.mac}),
        )
        if not request.is_response(response):
            raise BadResponse("unrelated DNS QUIC response")
        response = _quic._restore_id(response, query.id)
    elif connection is not None:
        response = await connection.query(
            query,
            timeout=timeout,
            one_rr_per_rrset=one_rr_per_rrset,
            ignore_trailing=ignore_trailing,
        )
    else:
        response = await transport.quic_query(
            query,
            where,
            timeout=timeout,
            port=port,
            backend=backend,
            local_port=source_port,
            local_address=source,
            server_name=hostname or server_hostname,
            ca_file=os.fspath(verify)
            if isinstance(verify, (str, os.PathLike))
            else None,
            verify=verify is not False,
            one_rr_per_rrset=one_rr_per_rrset,
            ignore_trailing=ignore_trailing,
        )
    if not query.is_response(response):
        raise BadResponse("unrelated DNS QUIC response")
    return _result(q, response, time() - begin)


async def inbound_xfr(
    where,
    txn_manager,
    query=None,
    port=53,
    timeout=None,
    lifetime=None,
    source=None,
    source_port=0,
    udp_mode=UDPMode.NEVER,
    backend=None,
    raise_on_serial_went_backwards=True,
):
    """Run the zone-transfer implementation from the DNS protocol package."""
    implementations = entry_points(group="tba.dns.inbound_xfr", name="protocol")
    if len(implementations) != 1:
        raise RuntimeError("inbound_xfr requires the tba-protocol-dns package")
    transfer = next(iter(implementations)).load()
    await transfer(
        where,
        txn_manager,
        query,
        port,
        timeout,
        lifetime,
        source,
        source_port,
        udp_mode,
        backend,
        raise_on_serial_went_backwards,
    )
