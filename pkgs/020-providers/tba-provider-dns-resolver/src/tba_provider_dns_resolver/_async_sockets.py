"""Socket adapters shared by the native DNS async backends."""

import asyncio
import socket

from tba_codec_dns.wire import WireError


class Socket:
    def __init__(self, family: int, type: int):
        self.family = family
        self.type = type

    async def close(self):
        raise NotImplementedError

    async def getpeername(self):
        raise NotImplementedError

    async def getsockname(self):
        raise NotImplementedError

    async def getpeercert(self, timeout=None):
        raise NotImplementedError

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        await self.close()


class DatagramSocket(Socket):
    async def sendto(self, what, destination, timeout=None):
        raise NotImplementedError

    async def recvfrom(self, size, timeout=None):
        raise NotImplementedError


class StreamSocket(Socket):
    async def sendall(self, what, timeout=None):
        raise NotImplementedError

    async def recv(self, size, timeout=None):
        raise NotImplementedError


class _DatagramProtocol(asyncio.DatagramProtocol):
    def __init__(self):
        self.incoming = asyncio.Queue()
        self.closed = asyncio.Event()

    def datagram_received(self, data, addr):
        self.incoming.put_nowait((data, addr))

    def error_received(self, exc):
        self.incoming.put_nowait(exc)

    def connection_lost(self, exc):
        self.incoming.put_nowait(exc or OSError("DNS datagram socket closed"))
        self.closed.set()


class AsyncioDatagram(DatagramSocket):
    def __init__(self, family, type, transport, protocol):
        super().__init__(family, type)
        self._transport = transport
        self._incoming = protocol.incoming
        self._closed = protocol.closed

    async def close(self):
        self._transport.close()
        await self._closed.wait()

    async def getpeername(self):
        return self._transport.get_extra_info("peername")

    async def getsockname(self):
        return self._transport.get_extra_info("sockname")

    async def sendto(self, what, destination, timeout=None):
        self._transport.sendto(what, destination)
        return len(what)

    async def recvfrom(self, size, timeout=None):
        event = await asyncio.wait_for(self._incoming.get(), timeout)
        if isinstance(event, BaseException):
            raise event
        data, address = event
        return data[:size], address


class AsyncioStream(StreamSocket):
    def __init__(self, family, type, reader, writer):
        super().__init__(family, type)
        self._reader = reader
        self._writer = writer

    async def close(self):
        self._writer.close()

    async def getpeername(self):
        return self._writer.get_extra_info("peername")

    async def getsockname(self):
        return self._writer.get_extra_info("sockname")

    async def getpeercert(self, timeout=None):
        context = self._writer.get_extra_info("ssl_object")
        return context.getpeercert() if context is not None else None

    async def sendall(self, what, timeout=None):
        self._writer.write(what)
        await asyncio.wait_for(self._writer.drain(), timeout)

    async def recv(self, size, timeout=None):
        return await asyncio.wait_for(self._reader.read(size), timeout)


class TrioDatagram(DatagramSocket):
    def __init__(self, wrapped, wait_for):
        super().__init__(wrapped.family, wrapped.type)
        self._socket = wrapped
        self._wait_for = wait_for

    async def close(self):
        self._socket.close()

    async def getpeername(self):
        try:
            return self._socket.getpeername()
        except OSError:
            return None

    async def getsockname(self):
        return self._socket.getsockname()

    async def sendto(self, what, destination, timeout=None):
        operation = (
            self._socket.send(what)
            if destination is None
            else self._socket.sendto(what, destination)
        )
        return await self._wait_for(operation, timeout)

    async def recvfrom(self, size, timeout=None):
        return await self._wait_for(self._socket.recvfrom(size), timeout)


class TrioStream(StreamSocket):
    def __init__(self, wrapped, stream, wait_for):
        super().__init__(wrapped.family, wrapped.type)
        self._socket = wrapped
        self._stream = stream
        self._wait_for = wait_for

    async def close(self):
        import trio

        await trio.aclose_forcefully(self._stream)

    async def getpeername(self):
        return self._socket.getpeername()

    async def getsockname(self):
        return self._socket.getsockname()

    async def getpeercert(self, timeout=None):
        handshake = getattr(self._stream, "do_handshake", None)
        if handshake is None:
            return None
        await self._wait_for(handshake(), timeout)
        return self._stream.getpeercert()

    async def sendall(self, what, timeout=None):
        await self._wait_for(self._stream.send_all(what), timeout)

    async def recv(self, size, timeout=None):
        return await self._wait_for(self._stream.receive_some(size), timeout)


async def open_asyncio(
    af, socktype, proto, source, destination, timeout, ssl_context, hostname
):
    if socktype == socket.SOCK_DGRAM:
        if source is None and destination is None:
            source = ("::", 0) if af == socket.AF_INET6 else ("0.0.0.0", 0)
        transport, protocol = await asyncio.wait_for(
            asyncio.get_running_loop().create_datagram_endpoint(
                _DatagramProtocol,
                family=af,
                proto=proto,
                local_addr=source,
                remote_addr=destination,
            ),
            timeout,
        )
        return AsyncioDatagram(af, socktype, transport, protocol)
    if socktype != socket.SOCK_STREAM or destination is None:
        raise ValueError("a DNS stream socket requires a destination")
    sock = socket.socket(af, socktype, proto)
    try:
        sock.setblocking(False)
        if source is not None:
            sock.bind(source)
        await asyncio.wait_for(
            asyncio.get_running_loop().sock_connect(sock, destination), timeout
        )
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(
                sock=sock, ssl=ssl_context, server_hostname=hostname
            ),
            timeout,
        )
    except BaseException:
        sock.close()
        raise
    return AsyncioStream(af, socktype, reader, writer)


async def open_trio(
    af, socktype, proto, source, destination, timeout, ssl_context, hostname, wait_for
):
    import trio

    sock = trio.socket.socket(af, socktype, proto)
    try:
        if source is not None:
            await wait_for(sock.bind(source), timeout)
        if destination is not None:
            await wait_for(sock.connect(destination), timeout)
        if socktype == socket.SOCK_DGRAM:
            return TrioDatagram(sock, wait_for)
        if socktype != socket.SOCK_STREAM or destination is None:
            raise ValueError("a DNS stream socket requires a destination")
        stream = trio.SocketStream(sock)
        if ssl_context is not None:
            stream = trio.SSLStream(
                stream, ssl_context, server_hostname=hostname, https_compatible=True
            )
            await wait_for(stream.do_handshake(), timeout)
        return TrioStream(sock, stream, wait_for)
    except BaseException:
        sock.close()
        raise


async def read_exactly(sock, size, timeout):
    data = bytearray()
    while len(data) < size:
        chunk = await sock.recv(size - len(data), timeout())
        if not chunk:
            raise WireError("incomplete DNS stream frame")
        data.extend(chunk)
    return bytes(data)
