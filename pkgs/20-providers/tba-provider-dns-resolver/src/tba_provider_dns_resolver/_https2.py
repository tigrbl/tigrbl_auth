"""HTTP/2 DoH over a caller-selected, certificate-verified bootstrap address."""

import asyncio
import errno
import socket

import anyio
import httpcore
from tba_codec_dns.wire import WireError

from ._doh import (
    _check_https_status,
    _extend_https,
    _https_response,
)
from ._socket_transport import _check_tls_peer_ip


class _TlsCheckingStream(httpcore.AsyncNetworkStream):
    def __init__(
        self,
        stream: httpcore.AsyncNetworkStream,
        certificate_ip: str | None,
        require_h2=True,
    ):
        self._stream = stream
        self._certificate_ip = certificate_ip
        self._require_h2 = require_h2

    async def read(self, max_bytes, timeout=None):
        return await self._stream.read(max_bytes, timeout)

    async def write(self, buffer, timeout=None):
        await self._stream.write(buffer, timeout)

    async def aclose(self):
        await self._stream.aclose()

    def get_extra_info(self, info):
        return self._stream.get_extra_info(info)

    async def start_tls(self, ssl_context, server_hostname=None, timeout=None):
        secure = await self._stream.start_tls(ssl_context, server_hostname, timeout)
        try:
            peer = secure.get_extra_info("ssl_object")
            if peer is None or (
                self._require_h2 and peer.selected_alpn_protocol() != "h2"
            ):
                raise WireError("the DNS HTTPS server did not negotiate HTTP/2")
            if self._certificate_ip is not None:
                _check_tls_peer_ip(peer.getpeercert(), self._certificate_ip)
        except BaseException:
            await secure.aclose()
            raise
        return secure


class BootstrapBackend(httpcore.AsyncNetworkBackend):
    def __init__(
        self,
        address: str | None,
        certificate_ip: str | None,
        require_h2=True,
        source_port=0,
        family=socket.AF_UNSPEC,
    ):
        self._address = address
        self._require_h2 = require_h2
        self._source_port = source_port
        self._family = family
        self._certificate_ip = certificate_ip
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            self._backend = httpcore.TrioBackend()
        else:
            self._backend = httpcore.AnyIOBackend()

    async def connect_tcp(
        self, host, port, timeout=None, local_address=None, socket_options=None
    ):
        host = self._address or host
        if self._source_port or self._family != socket.AF_UNSPEC:
            stream = await _bound_stream(
                host,
                port,
                local_address,
                self._source_port,
                self._family,
                timeout,
                socket_options,
            )
        else:
            stream = await self._backend.connect_tcp(
                host, port, timeout, local_address, socket_options
            )
        return _TlsCheckingStream(stream, self._certificate_ip, self._require_h2)

    async def sleep(self, seconds: float):
        await self._backend.sleep(seconds)


async def _bound_stream(
    host, port, source, source_port, family, timeout, socket_options
):
    from httpcore._backends.anyio import AnyIOStream

    pending = {
        errno.EINPROGRESS,
        errno.EWOULDBLOCK,
        errno.EALREADY,
        errno.EINTR,
        getattr(errno, "WSAEWOULDBLOCK", 10035),
        getattr(errno, "WSAEINPROGRESS", 10036),
    }
    last_error = None
    try:
        with anyio.fail_after(timeout):
            if source is not None:
                bindings = await anyio.getaddrinfo(
                    source,
                    source_port,
                    family=family,
                    type=socket.SOCK_STREAM,
                    flags=socket.AI_NUMERICHOST,
                )
                family = bindings[0][0]
                local = bindings[0][4]
            addresses = await anyio.getaddrinfo(
                host,
                port,
                family=family,
                type=socket.SOCK_STREAM,
            )
            for af, kind, proto, _, address in addresses:
                sock = socket.socket(af, kind, proto)
                try:
                    sock.setblocking(False)
                    if source is None:
                        binding = (
                            ("::", source_port, 0, 0)
                            if af == socket.AF_INET6
                            else ("0.0.0.0", source_port)
                        )
                    else:
                        binding = local
                    sock.bind(binding)
                    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                    for option in socket_options or ():
                        sock.setsockopt(*option)
                    result = sock.connect_ex(address)
                    if result in pending:
                        await anyio.wait_writable(sock)
                        result = sock.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
                    if result:
                        raise OSError(result, "source-bound TCP connection failed")
                    stream = await anyio.abc.SocketStream.from_socket(sock)
                except OSError as exc:
                    last_error = exc
                    sock.close()
                    continue
                except BaseException:
                    sock.close()
                    raise
                return AnyIOStream(stream)
    except TimeoutError as exc:
        raise httpcore.ConnectTimeout(str(exc)) from exc
    except OSError as exc:
        raise httpcore.ConnectError(str(exc)) from exc
    raise httpcore.ConnectError(
        str(last_error or "no compatible TCP address")
    ) from last_error


async def bootstrap_query(
    query,
    url,
    method,
    headers,
    body,
    context,
    address,
    ip,
    parse_options=None,
    *,
    source=None,
    source_port=0,
    family=socket.AF_UNSPEC,
    http1=False,
    http2=True,
):
    backend = BootstrapBackend(address, ip, not http1, source_port, family)
    try:
        async with httpcore.AsyncConnectionPool(
            ssl_context=context,
            http1=http1,
            http2=http2,
            local_address=source,
            network_backend=backend,
        ) as pool:
            async with pool.stream(
                method, url, headers=headers, content=body
            ) as response:
                content_type = next(
                    (
                        value.decode("latin-1")
                        for key, value in response.headers
                        if key.lower() == b"content-type"
                    ),
                    "",
                )
                _check_https_status(response.status, content_type)
                data = bytearray()
                async for chunk in response.aiter_stream():
                    _extend_https(data, chunk)
                return _https_response(query, data, parse_options)
    except httpcore.TimeoutException as exc:
        raise TimeoutError("DNS HTTP/2 exchange timed out") from exc
    except (httpcore.NetworkError, httpcore.ProtocolError) as exc:
        raise OSError("DNS HTTP/2 exchange failed") from exc
