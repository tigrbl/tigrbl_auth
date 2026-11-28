"""HTTP/3 DNS request streams on a shared QUIC connection."""

import asyncio
from dataclasses import dataclass, field

from aioquic.asyncio import QuicConnectionProtocol
from aioquic.h3.connection import H3Connection
from aioquic.h3.events import DataReceived, HeadersReceived
from aioquic.quic.events import ConnectionTerminated, StreamReset
from tba_codec_dns.wire import WireError

from ._doh import _extend_https, _https_request_fields


@dataclass
class Exchange:
    stream_id: int
    result: asyncio.Future
    headers: list | None = None
    data: bytearray = field(default_factory=bytearray)


def request_fields(packet, url, post):
    target, method, path, headers, body = _https_request_fields(packet, url, post)
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
    return fields, body


class H3Peer(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.http = H3Connection(self._quic)
        self.exchanges = {}

    def send_dns(self, url, packet, post):
        fields, body = request_fields(packet, url, post)
        stream_id = self._quic.get_next_available_stream_id()
        exchange = Exchange(stream_id, asyncio.get_running_loop().create_future())
        self.exchanges[stream_id] = exchange
        try:
            self.http.send_headers(stream_id, fields, end_stream=body is None)
            if body is not None:
                self.http.send_data(stream_id, body, end_stream=True)
            self.transmit()
        except BaseException:
            self.close_exchange(exchange)
            raise
        return exchange

    def close_exchange(self, exchange):
        self.exchanges.pop(exchange.stream_id, None)
        if not exchange.result.done():
            exchange.result.cancel()
            if not self._closed.is_set():
                self._quic.stop_stream(exchange.stream_id, error_code=0x10C)
                self.transmit()
        elif not exchange.result.cancelled():
            exchange.result.exception()

    def quic_event_received(self, event):
        if isinstance(event, ConnectionTerminated):
            for exchange in self.exchanges.values():
                if not exchange.result.done():
                    exchange.result.set_exception(
                        OSError("DNS HTTP/3 connection closed early")
                    )
            return
        if isinstance(event, StreamReset):
            exchange = self.exchanges.get(event.stream_id)
            if exchange is not None and not exchange.result.done():
                exchange.result.set_exception(OSError("DNS HTTP/3 stream closed early"))
        for item in self.http.handle_event(event):
            if not isinstance(item, (DataReceived, HeadersReceived)):
                continue
            exchange = self.exchanges.get(item.stream_id)
            if exchange is None or exchange.result.done():
                continue
            try:
                if isinstance(item, HeadersReceived) and exchange.headers is None:
                    status = int(dict(item.headers).get(b":status", b"0"))
                    if not 100 <= status < 200:
                        exchange.headers = item.headers
                if isinstance(item, DataReceived):
                    _extend_https(exchange.data, item.data)
                if item.stream_ended:
                    if exchange.headers is None:
                        raise WireError("missing DNS HTTP/3 response headers")
                    exchange.result.set_result(bytes(exchange.data))
            except ValueError as exc:
                exchange.result.set_exception(exc)
