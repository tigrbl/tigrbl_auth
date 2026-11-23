"""Cancellation-aware DNS UDP, TCP, and TLS exchange for asyncio and Trio."""

import asyncio
import socket
import ssl
from contextlib import AsyncExitStack
from functools import partial
from time import monotonic

from tba_codec_dns.wire import Message, WireError, response_flags

from . import _doh, _socket_transport, transport
from ._async_sockets import read_exactly
from .transport import Truncated, check_response, deadline_after, remaining


def _asyncio_active() -> bool:
    try:
        asyncio.get_running_loop()
        return True
    except RuntimeError:
        return False


async def run_blocking(function, /, *args, **kwargs):
    if _asyncio_active():
        return await asyncio.to_thread(function, *args, **kwargs)
    from trio import to_thread

    return await to_thread.run_sync(
        partial(function, *args, **kwargs), abandon_on_cancel=True
    )


def _deadline(timeout):
    return None if timeout is None else deadline_after(timeout)


def _timeout(expiration):
    return None if expiration is None else remaining(expiration)


async def send_udp(sock, what, destination, expiration=None):
    packet = what.to_wire() if isinstance(what, Message) else bytes(what)
    sent = await sock.sendto(packet, destination, _timeout(expiration))
    return sent, monotonic()


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
    options = {} if keyring is None else {"keyring": keyring}
    while True:
        packet, address = await sock.recvfrom(65535, _timeout(expiration))
        if destination is not None and address != destination:
            if ignore_unexpected:
                continue
            raise transport.UnexpectedSource(f"DNS response from {address!r}")
        try:
            response = Message.from_wire(
                packet,
                request_mac=request_mac,
                one_rr_per_rrset=one_rr_per_rrset,
                ignore_trailing=ignore_trailing,
                raise_on_truncation=raise_on_truncation,
                **options,
            )
            if ignore_errors and query is not None and not query.is_response(response):
                continue
        except Truncated as exc:
            if (
                ignore_errors
                and query is not None
                and (exc.partial is None or not query.is_response(exc.partial))
            ):
                continue
            raise
        except WireError:
            if not ignore_errors:
                raise
            continue
        return response, monotonic(), address


async def send_tcp(sock, what, expiration=None):
    packet = what.to_wire() if isinstance(what, Message) else bytes(what)
    await sock.sendall(len(packet).to_bytes(2, "big") + packet, _timeout(expiration))
    return len(packet) + 2, monotonic()


async def receive_tcp(
    sock,
    expiration=None,
    one_rr_per_rrset=False,
    keyring=None,
    request_mac=b"",
    ignore_trailing=False,
):
    def timeout():
        return _timeout(expiration)

    prefix = await read_exactly(sock, 2, timeout)
    packet = await read_exactly(sock, int.from_bytes(prefix, "big"), timeout)
    options = {} if keyring is None else {"keyring": keyring}
    response = Message.from_wire(
        packet,
        request_mac=request_mac,
        one_rr_per_rrset=one_rr_per_rrset,
        ignore_trailing=ignore_trailing,
        **options,
    )
    return response, monotonic()


def _backend(backend):
    if backend is not None:
        return backend
    from .asyncbackend import get_default_backend

    return get_default_backend()


async def _udp_packet(
    query,
    server,
    port,
    deadline,
    source,
    sock,
    backend,
    ignore_unexpected=True,
):
    if len(query.questions) != 1:
        raise ValueError("UDP query requires one DNS question")
    packet = query.to_wire()
    question = Message.from_wire(packet).questions[0]
    family, kind, protocol, _, address = socket.getaddrinfo(
        server,
        port,
        type=socket.SOCK_DGRAM,
        flags=socket.AI_NUMERICHOST,
    )[0]
    async with AsyncExitStack() as stack:
        if sock is None:
            sock = await _backend(backend).make_socket(
                family, kind, protocol, source, address, _timeout(deadline)
            )
            await stack.enter_async_context(sock)
        destination = None if await sock.getpeername() is not None else address
        await send_udp(sock, packet, destination, deadline)
        while True:
            response, peer = await sock.recvfrom(65535, _timeout(deadline))
            if peer != address:
                if ignore_unexpected:
                    continue
                raise transport.UnexpectedSource(f"DNS response from {peer!r}")
            try:
                response_flags(
                    response,
                    query.id,
                    question,
                    opcode=query.opcode,
                    allow_empty_question=query.opcode == 5,
                )
            except WireError:
                continue
            return response


async def udp_query(
    query: Message,
    server: str,
    *,
    port: int = 53,
    timeout: float | None = 3,
    source: tuple[str, int] | None = None,
    sock=None,
    backend=None,
    ignore_unexpected=True,
    one_rr_per_rrset=False,
    ignore_trailing=False,
    raise_on_truncation=True,
) -> Message:
    packet = await _udp_packet(
        query,
        server,
        port,
        _deadline(timeout),
        source,
        sock,
        backend,
        ignore_unexpected,
    )
    result = Message.from_wire(
        packet,
        one_rr_per_rrset=one_rr_per_rrset,
        ignore_trailing=ignore_trailing,
        raise_on_truncation=raise_on_truncation,
    )
    check_response(query, result, allow_empty_question=query.opcode == 5)
    return result


async def _stream_query(
    query,
    server,
    port,
    deadline,
    source,
    context,
    server_name,
    certificate_ip=None,
    *,
    sock=None,
    backend=None,
    one_rr_per_rrset=False,
    ignore_trailing=False,
):
    async with AsyncExitStack() as stack:
        if sock is None:
            family, kind, proto, _, address = socket.getaddrinfo(
                server,
                port,
                type=socket.SOCK_STREAM,
            )[0]
            sock = await _backend(backend).make_socket(
                family,
                kind,
                proto,
                source,
                address,
                _timeout(deadline),
                ssl_context=context,
                server_hostname=server_name,
            )
            await stack.enter_async_context(sock)
        if certificate_ip is not None:
            peer = await sock.getpeercert(_timeout(deadline))
            _socket_transport._check_tls_peer_ip(peer, certificate_ip)
        await send_tcp(sock, query, deadline)
        response, _ = await receive_tcp(
            sock, deadline, one_rr_per_rrset, ignore_trailing=ignore_trailing
        )
        check_response(query, response, allow_empty_question=query.opcode == 5)
        return response


async def tcp_query(
    query: Message,
    server: str,
    *,
    port: int = 53,
    timeout: float | None = 3,
    source: tuple[str, int] | None = None,
    sock=None,
    backend=None,
    one_rr_per_rrset=False,
    ignore_trailing=False,
) -> Message:
    return await _stream_query(
        query,
        server,
        port,
        _deadline(timeout),
        source,
        None,
        None,
        sock=sock,
        backend=backend,
        one_rr_per_rrset=one_rr_per_rrset,
        ignore_trailing=ignore_trailing,
    )


async def tls_query(
    query: Message,
    server: str,
    *,
    port: int = 853,
    timeout: float | None = 3,
    server_name: str | None = None,
    context: ssl.SSLContext | None = None,
    source: tuple[str, int] | None = None,
    certificate_ip: str | None = None,
    sock=None,
    backend=None,
    one_rr_per_rrset=False,
    ignore_trailing=False,
) -> Message:
    context = ssl.create_default_context() if context is None else context
    if certificate_ip is not None:
        _socket_transport._require_verified_context(context)
    return await _stream_query(
        query,
        server,
        port,
        _deadline(timeout),
        source,
        context,
        server_name or server,
        certificate_ip,
        sock=sock,
        backend=backend,
        one_rr_per_rrset=one_rr_per_rrset,
        ignore_trailing=ignore_trailing,
    )


async def udp_with_fallback(
    query: Message,
    server: str,
    *,
    port: int = 53,
    timeout: float | None = 3,
    source: tuple[str, int] | None = None,
    udp_sock=None,
    tcp_sock=None,
    backend=None,
    ignore_unexpected=True,
    one_rr_per_rrset=False,
    ignore_trailing=False,
) -> tuple[Message, bool]:
    deadline = _deadline(timeout)
    packet = await _udp_packet(
        query, server, port, deadline, source, udp_sock, backend, ignore_unexpected
    )
    if packet[2] & 2:
        result = await _stream_query(
            query,
            server,
            port,
            deadline,
            source,
            None,
            None,
            sock=tcp_sock,
            backend=backend,
            one_rr_per_rrset=one_rr_per_rrset,
            ignore_trailing=ignore_trailing,
        )
        return result, True
    result = Message.from_wire(
        packet, one_rr_per_rrset=one_rr_per_rrset, ignore_trailing=ignore_trailing
    )
    check_response(query, result, allow_empty_question=query.opcode == 5)
    return result, False


async def https_query(
    query: Message,
    url: str,
    *,
    timeout: float = 3,
    post: bool = True,
    context: ssl.SSLContext | None = None,
    http_version: int = 1,
    ca_file: str | None = None,
    ca_data: bytes | None = None,
    bootstrap_address: str | None = None,
    certificate_ip: str | None = None,
    token: bytes = b"",
    session=None,
    parse_options=None,
    verify=True,
    local_address=None,
    local_port=0,
) -> Message:
    if session is not None:
        _doh._check_http_session_options(
            http_version,
            context,
            ca_file,
            ca_data,
            bootstrap_address,
            certificate_ip,
            token,
            local_address,
            local_port,
        )
        return await _doh._async_https_with_session(
            query, url, timeout, post, http_version, session
        )
    if token and http_version != 3:
        raise ValueError("HTTPS tokens require HTTP/3")
    context = _doh._https_context(
        http_version, context, ca_file, ca_data, certificate_ip
    )
    if http_version == 2:
        return await _doh._https2_query(
            query,
            url,
            timeout=timeout,
            post=post,
            context=context,
            bootstrap_address=bootstrap_address,
            certificate_ip=certificate_ip,
            parse_options=parse_options,
            local_address=local_address,
            local_port=local_port,
        )
    if http_version == 3:
        from ._async_quic import query_h3

        options = dict(
            timeout=timeout,
            post=post,
            ca_file=ca_file,
            ca_data=ca_data,
            bootstrap_address=bootstrap_address,
            certificate_ip=certificate_ip,
            token=token,
            parse_options=parse_options,
            verify=verify,
            context=context,
            local_address=local_address,
            local_port=local_port,
        )
        return await query_h3(
            "asyncio" if _asyncio_active() else "trio", query, url, **options
        )
    return await run_blocking(
        _doh._https1_query,
        query,
        url,
        timeout=timeout,
        post=post,
        context=context,
        bootstrap_address=bootstrap_address,
        certificate_ip=certificate_ip,
        parse_options=parse_options,
        local_address=local_address,
        local_port=local_port,
    )


async def quic_query(query: Message, server: str, *, backend=None, **kwargs) -> Message:
    selected = _backend(backend)
    exchange = getattr(selected, "quic_query", None)
    if exchange is None:
        raise NotImplementedError("the selected DNS backend does not support DoQ")
    return await exchange(query, server, **kwargs)


async def _native_quic_query(query: Message, server: str, **kwargs) -> Message:
    from ._async_quic import query_doq

    return await query_doq(
        "asyncio" if _asyncio_active() else "trio", query, server, **kwargs
    )
