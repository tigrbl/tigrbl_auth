"""Native asyncio and Trio drivers for the QUIC state machine."""

import asyncio
import socket
import ssl
from contextlib import asynccontextmanager
from dataclasses import replace
from importlib.util import find_spec
from time import monotonic

from tba_codec_dns.wire import Message, WireError

from ._quic import (
    UnexpectedEOF,
    _check_certificate_ip,
    _client_configuration,
    _doq_request,
    _new_connection,
    _restore_id,
)
from ._socket_transport import check_response, deadline_after, remaining
from .asyncbackend import get_backend


async def _timed(backend, awaitable, timeout):
    try:
        return await backend.wait_for(awaitable, timeout)
    except asyncio.TimeoutError as exc:
        raise TimeoutError("DNS QUIC operation timed out") from exc


class AsyncQuicStream:
    """A single DoQ or HTTP/3 stream on an asynchronous QUIC connection."""

    def __init__(self, connection):
        self._connection = connection
        self._changed = connection._manager._event()
        self._id = None
        self._data = bytearray()
        self._headers = None
        self._error = None
        self._ended = False
        self._sent_end = False
        self._closed = False

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        await self.close()

    def headers(self):
        return self._headers

    def _start(self):
        connection = self._connection
        if self._closed or connection._closing or connection._error is not None:
            raise UnexpectedEOF("DNS QUIC stream is closed")
        if self._id is None:
            self._id = connection._quic.get_next_available_stream_id()
            connection._streams[self._id] = self

    async def send(self, datagram, is_end=False):
        if self._connection.is_h3() or self._sent_end:
            raise WireError("cannot send DoQ data on this stream")
        if not 0 < len(datagram) <= 65535:
            raise WireError("DNS QUIC message is outside the wire size limit")
        self._start()
        self._connection._quic.send_stream_data(
            self._id, len(datagram).to_bytes(2, "big") + datagram, end_stream=is_end
        )
        self._sent_end = is_end
        self._connection._wake.set()

    def send_h3(self, url, datagram, post=True):
        from ._quic_h3 import request_fields

        if not self._connection.is_h3() or self._id is not None:
            raise WireError("cannot send an HTTP/3 request on this stream")
        fields, body = request_fields(datagram, url, post)
        self._start()
        http = self._connection._http
        http.send_headers(self._id, fields, end_stream=body is None)
        if body is not None:
            http.send_data(self._id, body, end_stream=True)
        self._sent_end = True
        self._connection._wake.set()

    def _notify(self):
        self._changed.set()
        self._changed = self._connection._manager._event()

    def _input(self, data, is_end):
        limit = 65535 if self._connection.is_h3() else 65537
        if len(self._data) + len(data) > limit:
            self._error = WireError("DNS QUIC response exceeds the wire limit")
        else:
            self._data.extend(data)
        self._ended = is_end
        self._notify()

    async def _receive(self, expect_end):
        if self._id is None:
            raise ValueError("send a DNS query before receiving a response")
        while True:
            if self._error is not None:
                raise self._error
            if self._closed:
                raise UnexpectedEOF("DNS QUIC stream is closed")
            if self._connection.is_h3():
                if self._ended:
                    if self._headers is None:
                        raise WireError("missing DNS HTTP/3 response headers")
                    return bytes(self._data)
            elif len(self._data) >= 2:
                size = 2 + int.from_bytes(self._data[:2], "big")
                if len(self._data) >= size and (not expect_end or self._ended):
                    if expect_end and len(self._data) != size:
                        raise WireError("extra data after DNS QUIC response")
                    data = bytes(self._data[2:size])
                    del self._data[:size]
                    return data
            if self._ended:
                raise UnexpectedEOF("incomplete DNS message on QUIC stream")
            if self._connection._error is not None:
                raise self._connection._error
            if self._connection._closing:
                raise UnexpectedEOF("DNS QUIC connection closed")
            await self._changed.wait()

    async def receive(self, timeout=None):
        return await _timed(
            self._connection._manager._backend, self._receive(False), timeout
        )

    async def _receive_response(self, timeout):
        return await _timed(
            self._connection._manager._backend, self._receive(True), timeout
        )

    async def close(self):
        if self._closed:
            return
        self._closed = True
        self._notify()
        if self._id is None:
            return
        connection = self._connection
        connection._streams.pop(self._id, None)
        if not connection._closing and connection._error is None:
            code = 0x10C if connection.is_h3() else 3
            if not self._ended:
                connection._quic.stop_stream(self._id, error_code=code)
            if not self._sent_end:
                connection._quic.reset_stream(self._id, error_code=code)
            connection._wake.set()


class AsyncQuicConnection:
    """A reusable QUIC connection owned by an asynchronous manager."""

    def __init__(self, manager, endpoint, source, source_port, config):
        self._manager = manager
        self._endpoint = endpoint
        self._source = source
        self._source_port = source_port
        self._ready = manager._event()
        self._done = manager._event()
        self._wake = manager._event()
        self._streams = {}
        self._closing = False
        self._started = False
        self._opening_socket = True
        self._error = None
        self._quic = _new_connection(
            config,
            manager._peer_policy,
            lambda ticket: manager.save_session_ticket(*endpoint, ticket),
            lambda token: manager.save_token(*endpoint, token),
        )
        self._http = None
        if manager.is_h3():
            from aioquic.h3.connection import H3Connection

            self._http = H3Connection(self._quic)

    def is_h3(self):
        return self._http is not None

    async def make_stream(self, timeout=None):
        await _timed(self._manager._backend, self._ready.wait(), timeout)
        if self._error is not None:
            raise self._error
        if self._closing:
            raise UnexpectedEOF("DNS QUIC connection closed")
        return AsyncQuicStream(self)

    def _fail(self, exc):
        if self._error is None:
            self._error = exc
        self._ready.set()
        self._wake.set()
        for stream in self._streams.values():
            stream._notify()

    def _events(self):
        from aioquic.quic.events import (
            ConnectionTerminated,
            HandshakeCompleted,
            StreamDataReceived,
            StreamReset,
        )

        while (event := self._quic.next_event()) is not None:
            if isinstance(event, ConnectionTerminated):
                reason = event.reason_phrase or "DNS QUIC connection terminated"
                # TLS alerts can arrive after the local handshake event, for
                # example if the server rejects our client certificate.
                tls_alert = 0x100 <= event.error_code <= 0x1FF
                error = (
                    ConnectionError
                    if tls_alert or not self._ready.is_set()
                    else UnexpectedEOF
                )
                self._fail(
                    getattr(self._quic, "_dns_peer_error", None) or error(reason)
                )
                return
            if isinstance(event, HandshakeCompleted):
                self._ready.set()
            if isinstance(event, StreamReset):
                stream = self._streams.get(event.stream_id)
                if stream is not None:
                    stream._error = UnexpectedEOF("DNS QUIC stream was reset")
                    stream._notify()
            if self._http is not None:
                self._http_events(event)
            elif isinstance(event, StreamDataReceived):
                stream = self._streams.get(event.stream_id)
                if stream is not None:
                    stream._input(event.data, event.end_stream)

    def _http_events(self, event):
        from aioquic.h3.events import DataReceived, HeadersReceived

        for item in self._http.handle_event(event):
            if not isinstance(item, (DataReceived, HeadersReceived)):
                continue
            stream = self._streams.get(item.stream_id)
            if stream is None:
                continue
            if isinstance(item, HeadersReceived):
                if stream._headers is None:
                    try:
                        status = int(dict(item.headers).get(b":status", b"0"))
                    except ValueError as exc:
                        stream._error = exc
                    else:
                        if not 100 <= status < 200:
                            stream._headers = item.headers
                stream._input(b"", item.stream_ended)
            else:
                stream._input(item.data, item.stream_ended)

    async def _listen(self, sock):
        try:
            while not self._closing and self._error is None:
                packet, addr = await sock.recvfrom(65535)
                self._quic.receive_datagram(packet, addr, now=monotonic())
                self._events()
                self._wake.set()
        except Exception as exc:
            self._fail(exc)

    async def _flush(self, sock, peer):
        for data, address in self._quic.datagrams_to_send(now=monotonic()):
            if address == peer:
                await sock.sendto(data, None)

    async def _drive(self, sock, peer):
        self._quic.connect(peer, now=monotonic())
        async with self._manager._listener(self._listen, sock):
            while not self._closing and self._error is None:
                wake = self._wake = self._manager._event()
                await self._flush(sock, peer)
                timer = self._quic.get_timer()
                delay = None if timer is None else max(0, timer - monotonic())
                try:
                    await _timed(self._manager._backend, wake.wait(), delay)
                except TimeoutError:
                    self._quic.handle_timer(now=monotonic())
                    self._events()
        if self._closing and self._error is None:
            self._quic.close()
            await self._flush(sock, peer)

    async def _run(self):
        self._started = True
        try:
            if self._closing:
                return
            manager = self._manager
            lookup = manager._getaddrinfo
            family = socket.AF_UNSPEC
            source = None
            if self._source is not None:
                family, _, _, _, source = (
                    await lookup(
                        self._source,
                        self._source_port,
                        type=socket.SOCK_DGRAM,
                        flags=socket.AI_NUMERICHOST,
                    )
                )[0]
            family, kind, _, _, peer = (
                await lookup(*self._endpoint, family=family, type=socket.SOCK_DGRAM)
            )[0]
            if source is None and self._source_port:
                source = (
                    "::" if family == socket.AF_INET6 else "0.0.0.0",
                    self._source_port,
                )
            sock = await manager._open_socket(family, kind, source, peer)
            self._opening_socket = False
            try:
                await self._drive(sock, peer)
            finally:
                await manager._close_socket(sock)
        except Exception as exc:
            self._fail(exc)
        finally:
            self._closing = True
            self._fail(UnexpectedEOF("DNS QUIC connection closed"))
            self._manager.closed(*self._endpoint, connection=self)
            self._done.set()
            self._manager._active.discard(self)

    async def close(self):
        self._closing = True
        self._wake.set()
        if self._opening_socket and self._started and not self._done.is_set():
            self._manager._cancel(self)
        await self._done.wait()


class AsyncQuicManager:
    """Common lifecycle, configuration, and resumption state for async QUIC."""

    def __init__(self, conf, verify_mode, server_name, h3, backend):
        if find_spec("aioquic") is None:
            raise ImportError("asynchronous QUIC requires the quic extra")
        self._configuration, self._peer_policy = _client_configuration(
            conf, verify_mode, server_name, h3
        )
        self._h3 = h3
        self._backend = get_backend(backend)
        self._connections = {}
        self._active = set()
        self._session_tickets = {}
        self._tokens = {}
        self._token_handler = None
        self._closed = False

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        await self.close()

    def is_h3(self):
        return self._h3

    def connect(
        self,
        address,
        port=853,
        source=None,
        source_port=0,
        want_session_ticket=True,
        want_token=True,
    ):
        if self._closed:
            raise RuntimeError("DNS QUIC manager is closed")
        endpoint = address, port
        connection = self._connections.get(endpoint)
        if (
            connection is not None
            and not connection._closing
            and connection._error is None
        ):
            return connection
        config = replace(
            self._configuration,
            server_name=self._configuration.server_name or address,
            session_ticket=self._session_tickets.pop(
                endpoint, self._configuration.session_ticket
            )
            if want_session_ticket
            else None,
            token=self._tokens.pop(endpoint, self._configuration.token)
            if want_token
            else b"",
        )
        connection = AsyncQuicConnection(self, endpoint, source, source_port, config)
        self._spawn(connection)
        self._connections[endpoint] = connection
        self._active.add(connection)
        return connection

    def closed(self, address, port, *, connection=None):
        endpoint = address, port
        if connection is None or self._connections.get(endpoint) is connection:
            self._connections.pop(endpoint, None)

    @staticmethod
    def _save(cache, endpoint, value):
        cache.pop(endpoint, None)
        cache[endpoint] = value
        if len(cache) > 128:
            del cache[next(iter(cache))]

    def save_session_ticket(self, address, port, ticket):
        self._save(self._session_tickets, (address, port), ticket)

    def save_token(self, address, port, token):
        self._save(self._tokens, (address, port), token)
        if self._token_handler is not None:
            self._token_handler(token)

    async def close(self):
        self._closed = True
        for connection in tuple(self._active):
            await connection.close()


class _AsyncioDatagram:
    """An owned connected UDP socket with awaited I/O before shutdown."""

    def __init__(self, sock, loop, peer):
        self._sock = sock
        self._loop = loop
        self._peer = peer

    async def recvfrom(self, size):
        return await self._loop.sock_recv(self._sock, size), self._peer

    async def sendto(self, data, _destination):
        await self._loop.sock_sendall(self._sock, data)

    async def close(self):
        self._sock.close()


class AsyncioQuicManager(AsyncQuicManager):
    """Use asyncio datagram sockets and tasks for reusable QUIC connections."""

    def __init__(
        self, conf=None, verify_mode=ssl.CERT_REQUIRED, server_name=None, h3=False
    ):
        super().__init__(conf, verify_mode, server_name, h3, "asyncio")

    _event = staticmethod(asyncio.Event)

    @staticmethod
    def _getaddrinfo(*args, **kwargs):
        return asyncio.get_running_loop().getaddrinfo(*args, **kwargs)

    @staticmethod
    async def _open_socket(family, kind, source, peer):
        loop = asyncio.get_running_loop()
        sock = socket.socket(family, kind)
        try:
            sock.setblocking(False)
            if source is not None:
                sock.bind(source)
            await loop.sock_connect(sock, peer)
        except BaseException:
            sock.close()
            raise
        return _AsyncioDatagram(sock, loop, peer)

    @staticmethod
    def _spawn(connection):
        connection._task = asyncio.create_task(connection._run())

    @staticmethod
    def _cancel(connection):
        connection._task.cancel()

    @staticmethod
    @asynccontextmanager
    async def _listener(receive, sock):
        task = asyncio.create_task(receive(sock))
        try:
            yield
        finally:
            task.cancel()
            await asyncio.gather(task, return_exceptions=True)

    @staticmethod
    async def _close_socket(sock):
        await sock.close()


class TrioQuicManager(AsyncQuicManager):
    """Use Trio datagram sockets and a nursery for reusable QUIC connections."""

    def __init__(
        self,
        nursery=None,
        conf=None,
        verify_mode=ssl.CERT_REQUIRED,
        server_name=None,
        h3=False,
    ):
        import trio

        super().__init__(conf, verify_mode, server_name, h3, "trio")
        self._trio = trio
        self._nursery = nursery
        self._owned_nursery = None

    async def __aenter__(self):
        if self._nursery is None:
            self._owned_nursery = self._trio.open_nursery()
            self._nursery = await self._owned_nursery.__aenter__()
        return self

    async def __aexit__(self, *exc):
        try:
            await self.close()
        finally:
            if self._owned_nursery is not None:
                await self._owned_nursery.__aexit__(*exc)

    async def close(self):
        with self._trio.CancelScope(shield=True):
            await super().close()

    def _event(self):
        return self._trio.Event()

    def _getaddrinfo(self, *args, **kwargs):
        return self._trio.socket.getaddrinfo(*args, **kwargs)

    async def _open_socket(self, family, kind, source, peer):
        return await self._backend.make_socket(
            family, kind, source=source, destination=peer
        )

    def _spawn(self, connection):
        if self._nursery is None:
            raise RuntimeError("enter the Trio QUIC manager or supply a nursery")
        self._nursery.start_soon(self._run_scoped, connection)

    async def _run_scoped(self, connection):
        with self._trio.CancelScope() as scope:
            connection._scope = scope
            await connection._run()

    @staticmethod
    def _cancel(connection):
        connection._scope.cancel()

    @asynccontextmanager
    async def _listener(self, receive, sock):
        async with self._trio.open_nursery() as nursery:
            nursery.start_soon(receive, sock)
            try:
                yield
            finally:
                nursery.cancel_scope.cancel()

    async def _close_socket(self, sock):
        with self._trio.CancelScope(shield=True):
            await sock.close()


def _native_manager(
    backend,
    server_name,
    verify_mode,
    ca_file,
    ca_data,
    certificate_ip,
    token,
    *,
    h3=False,
):
    cls = AsyncioQuicManager if backend == "asyncio" else TrioQuicManager
    manager = cls(
        verify_mode=ca_file
        if ca_file is not None and verify_mode is not False
        else verify_mode,
        server_name=server_name,
        h3=h3,
    )
    manager._configuration.token = token
    if ca_data is not None:
        manager._configuration.cadata = ca_data
    if certificate_ip is not None:
        policy = manager._peer_policy
        if manager._configuration.verify_mode == ssl.CERT_NONE and policy is None:
            raise ValueError("certificate IP checking requires QUIC verification")

        def validate(certificates):
            if policy is not None:
                policy(certificates)
            _check_certificate_ip(certificates, certificate_ip)

        manager._peer_policy = validate
    return manager


async def query_doq(
    backend,
    query,
    server,
    *,
    port=853,
    timeout=3,
    server_name=None,
    ca_file=None,
    ca_data=None,
    certificate_ip=None,
    token=b"",
    token_handler=None,
    local_port=0,
    local_address=None,
    verify=True,
    one_rr_per_rrset=False,
    ignore_trailing=False,
):
    deadline = None if timeout is None else deadline_after(timeout)
    request = _doq_request(query)
    packet = request.to_wire()
    authentication = {}
    if request.tsig_key is not None:
        authentication = dict(
            keyring=request.tsig_key, request_mac=Message.from_wire(packet).mac
        )
    async with _native_manager(
        backend,
        server_name or server,
        verify,
        ca_file,
        ca_data,
        certificate_ip,
        token,
    ) as manager:
        manager._token_handler = token_handler
        connection = manager.connect(server, port, local_address, local_port)
        async with await connection.make_stream(remaining(deadline)) as stream:
            await stream.send(packet, True)
            data = await stream._receive_response(remaining(deadline))
    response = Message.from_wire(
        data,
        one_rr_per_rrset=one_rr_per_rrset,
        ignore_trailing=ignore_trailing,
        **authentication,
    )
    check_response(request, response)
    return _restore_id(response, query.id)


async def query_h3(
    backend,
    query,
    url,
    *,
    timeout=3,
    post=True,
    ca_file=None,
    ca_data=None,
    bootstrap_address=None,
    certificate_ip=None,
    token=b"",
    parse_options=None,
    verify=True,
    context=None,
    local_address=None,
    local_port=0,
):
    from ._doh import _check_https_status, _https3_request, _https_response

    target, packet, parse_options = _https3_request(query, url, post, parse_options)
    deadline = None if timeout is None else deadline_after(timeout)
    async with _native_manager(
        backend,
        target.hostname,
        verify if context is None else context,
        ca_file,
        ca_data,
        certificate_ip,
        token,
        h3=True,
    ) as manager:
        connection = manager.connect(
            bootstrap_address or target.hostname,
            target.port or 443,
            local_address,
            local_port,
        )
        async with await connection.make_stream(remaining(deadline)) as stream:
            stream.send_h3(url, packet, post)
            data = await stream.receive(remaining(deadline))
            fields = dict(stream.headers())
    _check_https_status(
        int(fields.get(b":status", b"0")),
        fields.get(b"content-type", b"").decode("ascii"),
    )
    return _https_response(query, data, parse_options)
