"""DNS over HTTPS exchanges and reusable HTTP sessions."""

import asyncio
import base64
import http.client
import socket
import ssl
from dataclasses import replace
from urllib.parse import urlsplit, urlunsplit

from tba_codec_dns.wire import Message, WireError

from ._http3_tls import client_identity, context_trust
from ._quic import _restore_id, _verified_quic_connection, _zero_id_request
from ._socket_transport import (
    _check_tls_peer_ip,
    _require_verified_context,
    check_response,
    deadline_after,
    remaining,
)


def _deadline(timeout):
    return None if timeout is None else deadline_after(timeout)


def _remaining(deadline):
    return None if deadline is None else remaining(deadline)


def https_query(
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
) -> Message:
    if session is not None:
        _check_http_session_options(
            http_version,
            context,
            ca_file,
            ca_data,
            bootstrap_address,
            certificate_ip,
            token,
        )
        return _https_with_session(query, url, timeout, post, http_version, session)
    if token and http_version != 3:
        raise ValueError("HTTPS tokens require HTTP/3")
    context = _https_context(http_version, context, ca_file, ca_data, certificate_ip)
    if http_version == 3:
        return asyncio.run(
            https3_query(
                query,
                url,
                timeout=timeout,
                post=post,
                ca_file=ca_file,
                ca_data=ca_data,
                bootstrap_address=bootstrap_address,
                certificate_ip=certificate_ip,
                token=token,
                context=context,
            )
        )
    if http_version == 2:
        return asyncio.run(
            _https2_query(
                query,
                url,
                timeout=timeout,
                post=post,
                context=context,
                bootstrap_address=bootstrap_address,
                certificate_ip=certificate_ip,
            )
        )
    return _https1_query(
        query,
        url,
        timeout=timeout,
        post=post,
        context=context,
        bootstrap_address=bootstrap_address,
        certificate_ip=certificate_ip,
    )


def _check_http_session_options(version, *options) -> None:
    if version not in (1, 2):
        raise ValueError("caller-owned HTTP sessions support HTTP/1.1 and HTTP/2")
    if any(options):
        raise ValueError("configure TLS and routing on the caller-owned HTTP session")


def _https_with_session(query, url, timeout, post, version, session):
    import httpx

    if not isinstance(session, httpx.Client):
        raise TypeError("synchronous DoH requires an httpx.Client session")
    deadline = _deadline(timeout)
    target, method, path, headers, body = _https_request(query, url, post)
    try:
        with session.stream(
            method,
            f"https://{target.netloc}{path}",
            headers=headers,
            content=body,
            timeout=_remaining(deadline),
            follow_redirects=False,
        ) as response:
            _check_session_response(response, version)
            data = bytearray()
            for chunk in response.iter_raw():
                _remaining(deadline)
                _extend_https(data, chunk)
            return _https_response(query, data)
    except httpx.TimeoutException as exc:
        raise TimeoutError("DNS HTTPS session timed out") from exc
    except httpx.HTTPError as exc:
        raise OSError("DNS HTTPS session failed") from exc


async def _async_https_with_session(query, url, timeout, post, version, session):
    import httpx

    if not isinstance(session, httpx.AsyncClient):
        raise TypeError("asynchronous DoH requires an httpx.AsyncClient session")
    deadline = _deadline(timeout)
    target, method, path, headers, body = _https_request(query, url, post)

    async def exchange():
        try:
            async with session.stream(
                method,
                f"https://{target.netloc}{path}",
                headers=headers,
                content=body,
                timeout=_remaining(deadline),
                follow_redirects=False,
            ) as response:
                _check_session_response(response, version)
                data = bytearray()
                async for chunk in response.aiter_raw():
                    _extend_https(data, chunk)
                return _https_response(query, data)
        except httpx.TimeoutException as exc:
            raise TimeoutError("DNS HTTPS session timed out") from exc
        except httpx.HTTPError as exc:
            raise OSError("DNS HTTPS session failed") from exc

    return await _wait_http_exchange(exchange, deadline)


def _check_session_response(response, version) -> None:
    _check_https_status(response.status_code, response.headers.get("Content-Type", ""))
    if version == 2 and response.http_version != "HTTP/2":
        raise WireError("the DNS HTTPS session did not negotiate HTTP/2")


def _https_context(http_version, context, ca_file, ca_data, certificate_ip):
    if http_version not in (1, 2, 3):
        raise ValueError("DNS HTTPS version must be 1, 2, or 3")
    if http_version == 3:
        if context is not None and (ca_file is not None or ca_data is not None):
            raise ValueError("specify CA material or an SSLContext")
        return context
    if context is not None and (ca_file is not None or ca_data is not None):
        raise ValueError("specify CA material or an SSLContext")
    if (
        ca_file is not None
        or ca_data is not None
        or (certificate_ip is not None and context is None)
    ):
        data = ca_data
        if data is not None and data.lstrip().startswith(
            b"-----BEGIN CERTIFICATE-----"
        ):
            data = data.decode("ascii")
        context = ssl.create_default_context(cafile=ca_file, cadata=data)
    if certificate_ip is not None:
        _require_verified_context(context)
    return context


class _BootstrapHttpsConnection(http.client.HTTPSConnection):
    def __init__(self, host, port, deadline, context, address, certificate_ip):
        super().__init__(host, port, timeout=_remaining(deadline), context=context)
        self._deadline = deadline
        self._address = address
        self._certificate_ip = certificate_ip

    def connect(self):
        sock = socket.create_connection(
            (self._address or self.host, self.port), timeout=_remaining(self._deadline)
        )
        try:
            sock.settimeout(_remaining(self._deadline))
            self.sock = self._context.wrap_socket(sock, server_hostname=self.host)
            if self._certificate_ip is not None:
                _check_tls_peer_ip(self.sock.getpeercert(), self._certificate_ip)
        except BaseException:
            self.close()
            sock.close()
            raise


def _https1_query(
    query: Message,
    url: str,
    *,
    timeout: float,
    post: bool,
    context: ssl.SSLContext | None,
    bootstrap_address: str | None = None,
    certificate_ip: str | None = None,
    parse_options=None,
) -> Message:
    deadline = _deadline(timeout)
    target, method, request_uri, headers, body = _https_request(query, url, post)
    connection = _BootstrapHttpsConnection(
        target.hostname,
        target.port,
        deadline,
        context,
        bootstrap_address,
        certificate_ip,
    )
    try:
        connection.request(method, request_uri, body, headers)
        if connection.sock is not None:
            connection.sock.settimeout(_remaining(deadline))
        active_socket = connection.sock
        response = connection.getresponse()
        with response:
            _check_https_status(
                response.status, response.headers.get("Content-Type", "")
            )
            data = bytearray()
            while not response.isclosed():
                timeout_left = _remaining(deadline)
                if active_socket is not None:
                    active_socket.settimeout(timeout_left)
                chunk = response.read1(65536 - len(data))
                if not chunk:
                    break
                _extend_https(data, chunk)
        return _https_response(query, data, parse_options)
    finally:
        connection.close()


def _https_request(query: Message, url: str, post: bool):
    target = urlsplit(url)
    if (
        target.scheme != "https"
        or not target.hostname
        or target.username is not None
        or target.fragment
    ):
        raise ValueError(
            "DoH requires an HTTPS endpoint without credentials or a fragment"
        )
    packet = _zero_id_request(query).to_wire()
    headers = {"Accept": "application/dns-message"}
    params = target.query
    if post:
        headers["Content-Type"] = "application/dns-message"
        body = packet
    else:
        parameter = "dns=" + base64.urlsafe_b64encode(packet).decode("ascii").rstrip(
            "="
        )
        params = "&".join(filter(None, (params, parameter)))
        body = None
    request_uri = urlunsplit(("", "", target.path or "/", params, ""))
    return target, "POST" if post else "GET", request_uri, headers, body


def _extend_https(data: bytearray, chunk: bytes) -> None:
    if len(data) + len(chunk) > 65535:
        raise WireError("DNS HTTPS response exceeds the DNS message limit")
    data.extend(chunk)


def _check_https_status(status: int, content_type: str) -> None:
    if (
        status != 200
        or content_type.split(";", 1)[0].strip().lower() != "application/dns-message"
    ):
        raise WireError(f"unexpected DNS HTTPS response ({status})")


def _https_response(query: Message, data: bytearray, parse_options=None) -> Message:
    result = Message.from_wire(bytes(data), **(parse_options or {}))
    check_response(replace(query, id=0), result)
    return _restore_id(result, query.id)


async def _https2_query(
    query: Message,
    url: str,
    *,
    timeout: float,
    post: bool,
    context: ssl.SSLContext | None,
    bootstrap_address: str | None = None,
    certificate_ip: str | None = None,
    parse_options=None,
) -> Message:
    import httpx

    deadline = _deadline(timeout)
    target, method, path, headers, body = _https_request(query, url, post)

    async def exchange() -> Message:
        if bootstrap_address is not None or certificate_ip is not None:
            from ._https2 import bootstrap_query

            return await bootstrap_query(
                query,
                f"https://{target.netloc}{path}",
                method,
                headers,
                body,
                context,
                bootstrap_address,
                certificate_ip,
                parse_options,
            )
        try:
            async with httpx.AsyncClient(
                http2=True,
                http1=False,
                verify=True if context is None else context,
                timeout=_remaining(deadline),
                trust_env=False,
            ) as client:
                async with client.stream(
                    method,
                    f"https://{target.netloc}{path}",
                    headers=headers,
                    content=body,
                ) as response:
                    _check_https_status(
                        response.status_code, response.headers.get("Content-Type", "")
                    )
                    data = bytearray()
                    async for chunk in response.aiter_raw():
                        _extend_https(data, chunk)
                    return _https_response(query, data, parse_options)
        except httpx.HTTPError as exc:
            raise OSError("DNS HTTP/2 exchange failed") from exc

    return await _wait_http_exchange(exchange, deadline)


async def _wait_http_exchange(exchange, deadline: float):
    if deadline is None:
        return await exchange()
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        import trio

        try:
            with trio.fail_after(_remaining(deadline)):
                return await exchange()
        except trio.TooSlowError as exc:
            raise TimeoutError("DNS HTTPS exchange timed out") from exc
    return await asyncio.wait_for(exchange(), timeout=_remaining(deadline))


async def https3_query(
    query: Message,
    url: str,
    *,
    timeout: float = 3,
    post: bool = True,
    ca_file: str | None = None,
    ca_data: bytes | None = None,
    bootstrap_address: str | None = None,
    certificate_ip: str | None = None,
    token: bytes = b"",
    parse_options=None,
    verify=True,
    context=None,
    local_address=None,
    local_port=0,
) -> Message:
    from aioquic.asyncio import QuicConnectionProtocol
    from aioquic.h3.connection import H3_ALPN, H3Connection
    from aioquic.h3.events import DataReceived, HeadersReceived
    from aioquic.quic.events import ConnectionTerminated, StreamReset

    peer_policy = None
    identity = None
    cipher_suites = None
    if context is not None:
        _https_context(3, context, ca_file, ca_data, certificate_ip)
        verify, ca_data, peer_policy, cipher_suites = context_trust(context)
        identity = client_identity(context)
    deadline = _deadline(timeout)
    target, method, path, headers, body = _https_request(query, url, post)

    class Exchange(QuicConnectionProtocol):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.http = H3Connection(self._quic)
            self.result = asyncio.get_running_loop().create_future()
            self.data = bytearray()
            self.stream_id = None
            self.got_headers = False

        async def query(self) -> Message:
            self.stream_id = self._quic.get_next_available_stream_id()
            fields = [
                (b":method", method.encode("ascii")),
                (b":scheme", b"https"),
                (b":authority", target.netloc.encode("ascii")),
                (b":path", path.encode("ascii")),
                *(
                    (name.lower().encode("ascii"), value.encode("ascii"))
                    for name, value in headers.items()
                ),
            ]
            if body is not None:
                fields.append((b"content-length", str(len(body)).encode("ascii")))
            self.http.send_headers(self.stream_id, fields, end_stream=body is None)
            if body is not None:
                self.http.send_data(self.stream_id, body, end_stream=True)
            self.transmit()
            return await self.result

        def quic_event_received(self, event) -> None:
            if self.result.done() or self.stream_id is None:
                return
            if isinstance(event, ConnectionTerminated) or (
                isinstance(event, StreamReset) and event.stream_id == self.stream_id
            ):
                self.result.set_exception(OSError("DNS HTTP/3 stream closed early"))
                return
            try:
                for item in self.http.handle_event(event):
                    if item.stream_id != self.stream_id:
                        continue
                    if isinstance(item, HeadersReceived) and not self.got_headers:
                        fields = dict(item.headers)
                        status = int(fields.get(b":status", b"0"))
                        if 100 <= status < 200:
                            continue
                        _check_https_status(
                            status, fields.get(b"content-type", b"").decode("ascii")
                        )
                        self.got_headers = True
                    if isinstance(item, DataReceived):
                        _extend_https(self.data, item.data)
                    if (
                        isinstance(item, (DataReceived, HeadersReceived))
                        and item.stream_ended
                    ):
                        if not self.got_headers:
                            raise WireError("missing DNS HTTP/3 response headers")
                        self.result.set_result(
                            _https_response(query, self.data, parse_options)
                        )
                        return
            except ValueError as exc:
                self.result.set_exception(exc)

    async def exchange() -> Message:
        async with _verified_quic_connection(
            bootstrap_address or target.hostname,
            target.port or 443,
            H3_ALPN,
            server_name=target.hostname,
            ca_file=ca_file,
            ca_data=ca_data,
            certificate_ip=certificate_ip,
            token=token,
            protocol=Exchange,
            verify=verify,
            peer_policy=peer_policy,
            client_identity=identity,
            cipher_suites=cipher_suites,
            local_address=local_address,
            local_port=local_port,
        ) as peer:
            return await peer.query()

    return await asyncio.wait_for(exchange(), timeout=_remaining(deadline))
