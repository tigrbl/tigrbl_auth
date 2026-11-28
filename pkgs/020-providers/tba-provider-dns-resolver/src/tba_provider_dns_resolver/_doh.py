"""DNS over HTTPS exchanges and reusable HTTP sessions."""

import asyncio
import base64
import http.client
import ipaddress
import socket
import ssl
from dataclasses import replace
from enum import IntEnum
from importlib.util import find_spec
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


class NoDOH(WireError):
    """The requested DNS-over-HTTPS transport is unavailable."""


class HTTPVersion(IntEnum):
    DEFAULT = 0
    HTTP_1 = 1
    H1 = 1
    HTTP_2 = 2
    H2 = 2
    HTTP_3 = 3
    H3 = 3


def _https_transport(version, client, have_doh):
    """Select HTTP/3 or load the available HTTP/1.1 and HTTP/2 client."""
    if version == HTTPVersion.H3 or (
        version == HTTPVersion.DEFAULT and hasattr(client, "make_stream")
    ):
        use_h3 = True
    else:
        httpx = None
        if have_doh:
            try:
                import httpx
            except ImportError:
                pass
        if httpx is not None:
            use_h2 = version != HTTPVersion.H1
            if use_h2 and client is None and find_spec("h2") is None:
                if version == HTTPVersion.H2:
                    raise NoDOH("HTTP/2 requires the http2 extra")
                use_h2 = False
            return False, httpx, use_h2
        use_h3 = version == HTTPVersion.DEFAULT and client is None
    if not use_h3:
        raise NoDOH("HTTP/1.1 and HTTP/2 require the http2 extra")
    if client is None and find_spec("aioquic") is None:
        raise NoDOH("HTTP/3 requires the quic extra")
    return True, None, False


def _literal_address(hostname):
    try:
        ipaddress.ip_address(hostname)
    except ValueError:
        return None
    return hostname


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
    local_address=None,
    local_port=0,
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
            local_address,
            local_port,
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
                local_address=local_address,
                local_port=local_port,
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
                local_address=local_address,
                local_port=local_port,
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
        local_address=local_address,
        local_port=local_port,
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
    def __init__(self, host, port, deadline, context, address, certificate_ip, source):
        super().__init__(
            host,
            port,
            timeout=_remaining(deadline),
            context=context,
            source_address=source,
        )
        self._deadline = deadline
        self._address = address
        self._certificate_ip = certificate_ip

    def connect(self):
        sock = socket.create_connection(
            (self._address or self.host, self.port),
            timeout=_remaining(self._deadline),
            source_address=self.source_address,
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
    local_address=None,
    local_port=0,
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
        (local_address or "", local_port) if local_address or local_port else None,
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


def _https_request(query: Message, url: str, post: bool, *, zero_id=True):
    packet = (_zero_id_request(query) if zero_id else query).to_wire()
    return _https_request_fields(packet, url, post)


def _https_request_fields(packet: bytes, url: str, post: bool):
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


def _https3_request(query, url, post, parse_options):
    packet = _zero_id_request(query).to_wire()
    if query.tsig_key is not None:
        sent = Message.from_wire(packet)
        if sent.had_tsig:
            parse_options = dict(parse_options or ())
            parse_options.setdefault("keyring", query.tsig_key)
            parse_options["request_mac"] = sent.mac
    target, _, _, _, _ = _https_request_fields(packet, url, post)
    return target, packet, parse_options


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


def _https_response(
    query: Message, data: bytearray, parse_options=None, *, zero_id=True
) -> Message:
    result = Message.from_wire(bytes(data), **(parse_options or {}))
    check_response(replace(query, id=0) if zero_id else query, result)
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
    local_address=None,
    local_port=0,
) -> Message:
    import httpx

    deadline = _deadline(timeout)
    target, method, path, headers, body = _https_request(query, url, post)

    async def exchange() -> Message:
        if (
            bootstrap_address is not None
            or certificate_ip is not None
            or local_address
            or local_port
        ):
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
                source=local_address,
                source_port=local_port,
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
    check_status=_check_https_status,
) -> Message:
    from aioquic.h3.connection import H3_ALPN

    from ._quic_h3 import H3Peer

    peer_policy = None
    identity = None
    cipher_suites = None
    if context is not None:
        _https_context(3, context, ca_file, ca_data, certificate_ip)
        verify, ca_data, peer_policy, cipher_suites = context_trust(context)
        identity = client_identity(context)
    deadline = _deadline(timeout)
    target, packet, parse_options = _https3_request(query, url, post, parse_options)

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
            protocol=H3Peer,
            verify=verify,
            peer_policy=peer_policy,
            client_identity=identity,
            cipher_suites=cipher_suites,
            local_address=local_address,
            local_port=local_port,
        ) as peer:
            stream = peer.send_dns(url, packet, post)
            try:
                data = await asyncio.shield(stream.result)
                fields = dict(stream.headers)
                check_status(
                    int(fields.get(b":status", b"0")),
                    fields.get(b"content-type", b"").decode("ascii"),
                )
                return _https_response(query, data, parse_options)
            finally:
                peer.close_exchange(stream)

    return await asyncio.wait_for(exchange(), timeout=_remaining(deadline))
