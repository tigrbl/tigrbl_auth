"""Reusable DNS-over-QUIC and HTTP/3 connections."""

import asyncio
import socket
import ssl
from contextlib import nullcontext
from dataclasses import replace
from importlib.util import find_spec
from threading import Lock, Thread

from tba_codec_dns.wire import WireError

from ._async_quic import AsyncioQuicManager as AsyncioQuicManager
from ._async_quic import AsyncQuicConnection as AsyncQuicConnection
from ._async_quic import AsyncQuicManager as AsyncQuicManager
from ._async_quic import AsyncQuicStream as AsyncQuicStream
from ._async_quic import TrioQuicManager as TrioQuicManager
from ._quic import UnexpectedEOF as UnexpectedEOF
from ._quic import _client_configuration, _connect_from

have_quic = find_spec("aioquic") is not None
socket_factory = socket.socket


def _doq_protocol():
    from aioquic.asyncio import QuicConnectionProtocol
    from aioquic.quic.events import StreamReset

    class DoQPeer(QuicConnectionProtocol):
        def quic_event_received(self, event):
            if isinstance(event, StreamReset):
                reader = self._stream_readers.get(event.stream_id)
                if reader is not None:
                    reader.feed_eof()
            super().quic_event_received(event)

    return DoQPeer


class SyncQuicStream:
    """One caller-owned HTTP/3 or length-framed DoQ stream."""

    def __init__(self, connection, peer):
        self._connection = connection
        self._peer = peer
        self._exchange = None
        self._reader = None
        self._stream_id = None
        self._pending_length = None
        self._send_ended = False
        self._closed = False

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    def _check_open(self):
        if self._closed or self._peer._closed.is_set():
            raise UnexpectedEOF("DNS QUIC stream is closed")

    def send(self, datagram, is_end=False):
        """Send a length-prefixed DNS message over DoQ."""
        self._connection._manager._run(self._send, datagram, is_end)

    async def _send(self, datagram, is_end):
        self._check_open()
        if self._connection.is_h3() or self._send_ended:
            raise WireError("cannot send DoQ data on this stream")
        if not 0 < len(datagram) <= 65535:
            raise WireError("DNS QUIC message is outside the wire size limit")
        if self._reader is None:
            self._reader, writer = await self._peer.create_stream()
            self._stream_id = writer.get_extra_info("stream_id")
            self._writer = writer
        self._writer.write(len(datagram).to_bytes(2, "big") + datagram)
        if is_end:
            self._writer.write_eof()
            self._send_ended = True

    def send_h3(self, url, datagram, post=True):
        """Send an HTTP/3 DNS request."""
        self._connection._manager._run(self._send_h3, url, datagram, post)

    async def _send_h3(self, url, datagram, post):
        self._check_open()
        if not self._connection.is_h3() or self._exchange is not None:
            raise WireError("cannot send an HTTP/3 request on this stream")
        self._exchange = self._peer.send_dns(url, datagram, post)

    def receive(self, timeout=None):
        """Receive one DNS datagram or the complete HTTP response body."""
        return self._connection._manager._run(self._receive, timeout)

    async def _receive(self, timeout, expect_end=False):
        if self._closed:
            raise UnexpectedEOF("DNS QUIC stream is closed")
        if self._exchange is not None:
            return await asyncio.wait_for(
                asyncio.shield(self._exchange.result), timeout
            )
        if self._reader is None:
            raise ValueError("send a DNS query before receiving a response")

        async def read():
            try:
                if self._pending_length is None:
                    self._pending_length = int.from_bytes(
                        await self._reader.readexactly(2), "big"
                    )
                data = await self._reader.readexactly(self._pending_length)
                self._pending_length = None
                if expect_end and await self._reader.read(1):
                    raise WireError("extra data after DNS QUIC response")
                return data
            except asyncio.IncompleteReadError as exc:
                raise UnexpectedEOF("incomplete DNS message on QUIC stream") from exc

        return await asyncio.wait_for(read(), timeout)

    def _receive_response(self, timeout):
        return self._connection._manager._run(self._receive, timeout, True)

    def headers(self):
        """Return the HTTP/3 response headers, if available."""
        return self._connection._manager._run(self._headers)

    async def _headers(self):
        return None if self._exchange is None else self._exchange.headers

    def close(self):
        """Release this stream while keeping its connection reusable."""
        self._connection._manager._run_if_open(self._close)

    async def _close(self):
        if self._closed:
            return
        self._closed = True
        if self._exchange is not None:
            self._peer.close_exchange(self._exchange)
        if self._reader is not None:
            if not self._peer._closed.is_set() and not self._reader.at_eof():
                self._peer._quic.stop_stream(self._stream_id, error_code=3)
                self._peer.transmit()
            self._writer.close()
            self._reader.feed_eof()
        self._connection._streams.discard(self)


class SyncQuicConnection:
    """A reusable connection whose streams share one TLS handshake."""

    def __init__(self, manager, address, port):
        self._manager = manager
        self._endpoint = (address, port)
        self._streams = set()
        self._context = None
        self._peer = None
        self._closed = False

    async def _open(self, config, source, source_port):
        address, port = self._endpoint
        manager = self._manager
        self._context = _connect_from(
            address,
            port,
            source,
            local_port=source_port,
            configuration=config,
            create_protocol=manager._protocol,
            token_handler=lambda token: manager.save_token(address, port, token),
            session_ticket_handler=lambda ticket: manager.save_session_ticket(
                address, port, ticket
            ),
            validate_peer=manager._peer_policy,
            socket_factory=socket_factory,
        )
        self._peer = await self._context.__aenter__()

    def is_h3(self):
        return self._manager.is_h3()

    def make_stream(self, timeout=None):
        """Wait for the handshake and return a new synchronous stream."""
        return self._manager._run(self._make_stream, timeout)

    async def _make_stream(self, timeout):
        await asyncio.wait_for(
            asyncio.shield(asyncio.wrap_future(self._opening)), timeout
        )
        if self._closed or self._peer._closed.is_set():
            raise UnexpectedEOF("DNS QUIC connection closed")
        stream = SyncQuicStream(self, self._peer)
        self._streams.add(stream)
        return stream

    def close(self):
        """Close this connection and all of its streams."""
        self._manager._run_if_open(self._close)

    async def _close(self):
        if self._closed:
            return
        self._closed = True
        if self._peer is None:
            self._opening.cancel()
        await asyncio.gather(asyncio.wrap_future(self._opening), return_exceptions=True)
        try:
            for stream in tuple(self._streams):
                await stream._close()
        finally:
            if self._peer is not None:
                await self._context.__aexit__(None, None, None)
            self._manager.closed(*self._endpoint, connection=self)


class SyncQuicManager:
    """Own and reuse authenticated blocking QUIC connections in a context."""

    def __init__(
        self, conf=None, verify_mode=ssl.CERT_REQUIRED, server_name=None, h3=False
    ):
        if not have_quic:
            raise ImportError("synchronous QUIC requires the quic extra")
        self._h3 = h3
        if h3:
            from ._quic_h3 import H3Peer

            self._protocol = H3Peer
        else:
            self._protocol = _doq_protocol()
        self._configuration, self._peer_policy = _client_configuration(
            conf, verify_mode, server_name, h3
        )
        self._connections = {}
        self._session_tickets = {}
        self._tokens = {}
        self._lock = Lock()
        self._loop = None
        self._closed = False

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    def is_h3(self):
        return self._h3

    def _worker(self):
        asyncio.set_event_loop(self._loop)
        try:
            self._loop.run_forever()
            tasks = asyncio.all_tasks(self._loop)
            for task in tasks:
                task.cancel()
            if tasks:
                self._loop.run_until_complete(
                    asyncio.gather(*tasks, return_exceptions=True)
                )
            self._loop.run_until_complete(self._loop.shutdown_asyncgens())
            self._loop.run_until_complete(self._loop.shutdown_default_executor())
        finally:
            self._loop.close()

    def connect(
        self,
        address,
        port=853,
        source=None,
        source_port=0,
        want_session_ticket=True,
        want_token=True,
    ):
        """Start or reuse a connection to the given address and port."""
        with self._lock:
            if self._closed:
                raise RuntimeError("DNS QUIC manager is closed")
            if self._loop is None:
                self._loop = asyncio.new_event_loop()
                self._thread = Thread(target=self._worker, name="DNS QUIC", daemon=True)
                self._thread.start()
            endpoint = address, port
            existing = self._connections.get(endpoint)
            if existing is not None and not existing._closed:
                pending = not existing._opening.done()
                connected = (
                    existing._peer is not None and not existing._peer._closed.is_set()
                )
                if pending or connected:
                    return existing
                asyncio.run_coroutine_threadsafe(existing._close(), self._loop)
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
            connection = SyncQuicConnection(self, address, port)
            connection._opening = asyncio.run_coroutine_threadsafe(
                connection._open(config, source, source_port), self._loop
            )
            self._connections[endpoint] = connection
            return connection

    def closed(self, address, port, *, connection=None):
        with self._lock:
            endpoint = address, port
            if connection is None or self._connections.get(endpoint) is connection:
                self._connections.pop(endpoint, None)

    def _save(self, cache, endpoint, value):
        with self._lock:
            cache.pop(endpoint, None)
            cache[endpoint] = value
            if len(cache) > 128:
                cache.pop(next(iter(cache)))

    def save_token(self, address, port, token):
        self._save(self._tokens, (address, port), token)

    def save_session_ticket(self, address, port, ticket):
        self._save(self._session_tickets, (address, port), ticket)

    def _run(self, operation, *args, if_open=False):
        with self._lock:
            if self._closed:
                if if_open:
                    return None
                raise RuntimeError("DNS QUIC manager is closed")
            future = asyncio.run_coroutine_threadsafe(operation(*args), self._loop)
        try:
            return future.result()
        except asyncio.TimeoutError as exc:
            raise TimeoutError("DNS QUIC operation timed out") from exc

    def _run_if_open(self, operation):
        return self._run(operation, if_open=True)

    def close(self):
        """Close all tracked connections and release the worker thread."""
        with self._lock:
            if self._closed:
                return
            self._closed = True
            if self._loop is None:
                return
            connections = tuple(self._connections.values())

        async def shutdown():
            await asyncio.gather(*(item._close() for item in connections))

        try:
            asyncio.run_coroutine_threadsafe(shutdown(), self._loop).result()
        finally:
            self._loop.call_soon_threadsafe(self._loop.stop)
            self._thread.join()


def factories_for_backend(backend=None):
    """Return an async context factory and the selected QUIC manager factory."""
    from .asyncbackend import get_default_backend

    backend = get_default_backend() if backend is None else backend
    if backend.name() == "asyncio":
        return nullcontext, _asyncio_manager_factory
    if backend.name() == "trio":
        import trio

        return trio.open_nursery, TrioQuicManager
    raise NotImplementedError(f"no QUIC manager for the {backend.name()} backend")


def _asyncio_manager_factory(context, *args, **kwargs):
    return AsyncioQuicManager(*args, **kwargs)


__all__ = [
    "AsyncioQuicManager",
    "AsyncQuicConnection",
    "AsyncQuicManager",
    "AsyncQuicStream",
    "TrioQuicManager",
    "SyncQuicConnection",
    "SyncQuicManager",
    "SyncQuicStream",
    "UnexpectedEOF",
    "have_quic",
    "factories_for_backend",
    "socket_factory",
]
