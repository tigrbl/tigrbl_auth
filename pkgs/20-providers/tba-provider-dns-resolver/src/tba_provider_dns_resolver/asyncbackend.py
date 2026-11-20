"""Selectable asyncio and Trio backends for the asynchronous resolver."""

import asyncio
from contextvars import ContextVar
from typing import Protocol

from tba_codec_dns.wire import Message

from . import async_transport
from ._async_sockets import DatagramSocket as DatagramSocket
from ._async_sockets import Socket as Socket
from ._async_sockets import StreamSocket as StreamSocket
from ._async_sockets import open_asyncio, open_trio


class AsyncLibraryNotFoundError(RuntimeError):
    """DNS async I/O requires an active asyncio or Trio runtime."""


class Backend(Protocol):
    async def query(
        self, request: Message, server, *, port: int, timeout: float, tcp: bool
    ) -> Message: ...

    async def sleep(self, interval: float) -> None: ...

    def name(self) -> str: ...

    def datagram_connection_required(self) -> bool: ...

    async def make_socket(
        self,
        af,
        socktype,
        proto=0,
        source=None,
        destination=None,
        timeout=None,
        ssl_context=None,
        server_hostname=None,
    ) -> Socket: ...

    async def wait_for(self, awaitable, timeout=None): ...

    def get_transport_class(self): ...


class DoQBackend(Protocol):
    """Optional backend capability for an entire DNS-over-QUIC exchange."""

    async def quic_query(self, query: Message, server: str, **options) -> Message: ...


class _NativeBackend:
    def __init__(self, name: str):
        self._name = name

    def name(self) -> str:
        return self._name

    def datagram_connection_required(self) -> bool:
        return False

    async def make_socket(
        self,
        af,
        socktype,
        proto=0,
        source=None,
        destination=None,
        timeout=None,
        ssl_context=None,
        server_hostname=None,
    ):
        self._check_runtime()
        args = (
            af,
            socktype,
            proto,
            source,
            destination,
            timeout,
            ssl_context,
            server_hostname,
        )
        if self._name == "asyncio":
            return await open_asyncio(*args)
        return await open_trio(*args, self.wait_for)

    async def wait_for(self, awaitable, timeout=None):
        if self._name == "asyncio":
            return await asyncio.wait_for(awaitable, timeout)
        import trio

        try:
            with (
                trio.fail_after(timeout) if timeout is not None else trio.CancelScope()
            ):
                return await awaitable
        except trio.TooSlowError as exc:
            raise TimeoutError("DNS socket operation timed out") from exc

    def get_transport_class(self):
        from httpx import AsyncHTTPTransport

        return AsyncHTTPTransport

    def _check_runtime(self) -> None:
        if sniff() != self._name:
            raise AsyncLibraryNotFoundError(
                f"the {self._name} DNS backend needs a {self._name} runtime"
            )

    async def quic_query(self, query: Message, server: str, **options) -> Message:
        self._check_runtime()
        return await async_transport._native_quic_query(query, server, **options)

    async def query(self, request, server, *, port, timeout, tcp):
        from .client import HttpsNameserver, QuicNameserver, TlsNameserver

        self._check_runtime()
        if isinstance(server, str):
            if tcp:
                return await async_transport.tcp_query(
                    request, server, port=port, timeout=timeout, backend=self
                )
            reply, _ = await async_transport.udp_with_fallback(
                request, server, port=port, timeout=timeout, backend=self
            )
            return reply
        if isinstance(server, TlsNameserver):
            return await async_transport.tls_query(
                request,
                server.address,
                port=server.port,
                timeout=timeout,
                server_name=server.hostname,
                context=server.context,
                certificate_ip=server.certificate_ip,
                backend=self,
            )
        if isinstance(server, HttpsNameserver):
            return await async_transport.https_query(
                request,
                server.url,
                timeout=timeout,
                post=server.post,
                context=server.context,
                http_version=server.http_version,
                ca_file=server.ca_file,
                ca_data=server.ca_data,
                bootstrap_address=server.bootstrap_address,
                certificate_ip=server.certificate_ip,
                session=server.session,
            )
        if isinstance(server, QuicNameserver):
            return await self.quic_query(
                request,
                server.address,
                port=server.port,
                timeout=timeout,
                server_name=server.hostname,
                ca_file=server.ca_file,
                ca_data=server.ca_data,
                certificate_ip=server.certificate_ip,
            )
        raise TypeError("unsupported DNS nameserver")

    async def sleep(self, interval: float):
        self._check_runtime()
        if self._name == "asyncio":
            await asyncio.sleep(interval)
        else:
            import trio

            await trio.sleep(interval)


_BACKENDS = {name: _NativeBackend(name) for name in ("asyncio", "trio")}
_DEFAULT: ContextVar[Backend | None] = ContextVar("dns_async_backend", default=None)


def sniff() -> str:
    if async_transport._asyncio_active():
        return "asyncio"
    try:
        from trio.lowlevel import current_trio_token

        current_trio_token()
    except (ImportError, RuntimeError) as exc:
        raise AsyncLibraryNotFoundError("no active DNS async runtime") from exc
    return "trio"


def get_backend(name: str) -> Backend:
    try:
        return _BACKENDS[name]
    except KeyError as exc:
        raise NotImplementedError(f"unknown DNS async backend {name!r}") from exc


def get_default_backend() -> Backend:
    backend = _DEFAULT.get()
    return get_backend(sniff()) if backend is None else backend


def set_default_backend(name: str | None) -> Backend | None:
    backend = None if name is None else get_backend(name)
    _DEFAULT.set(backend)
    return backend
