"""Shared loopback transport and observable resource endpoints."""

import json
from http.client import HTTPSConnection
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import socket

from .resource import WriteLedger


class FixtureServer(ThreadingHTTPServer):
    def __init__(self, port, context, ledger=None):
        self.ledger = WriteLedger() if ledger is None else ledger
        self.tls_context = context
        super().__init__(("127.0.0.1", port), ResourceHandler)

    def get_request(self):
        connection, address = super().get_request()
        try:
            connection.settimeout(5)
            return self.tls_context.wrap_socket(connection, server_side=True), address
        except OSError:
            connection.close()
            raise


class ResourceHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def reply(self, code, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def request_resource(self, path, *, write):
        if self.path != path:
            self.reply(404, {"decision": "not-found"})
            return
        try:
            identity = self.server.authenticate(self, path)
        except ValueError as error:
            self.reply(self.server.denial_status, {"decision": "deny", "reason": str(error)})
            return
        if write:
            self.server.ledger.commit(identity)
            self.reply(201, {"decision": "allow", "identity": identity})
        else:
            self.reply(200, {"decision": "allow", "writes": self.server.ledger.snapshot()})

    def do_POST(self):
        self.request_resource("/writes", write=True)

    def do_GET(self):
        self.request_resource("/effects", write=False)


class FixtureConnection(HTTPSConnection):
    """Separate the TCP address from the TLS server name."""

    def __init__(self, host, port, dns_name, context):
        super().__init__(host, port, context=context, timeout=5)
        self.dns_name = dns_name

    def connect(self):
        raw = socket.create_connection((self.host, self.port), self.timeout)
        try:
            self.sock = self._context.wrap_socket(raw, server_hostname=self.dns_name)
        except BaseException:
            raw.close()
            raise


def call_resource(connection, *, readback=False, headers=None):
    try:
        connection.request("GET" if readback else "POST", "/effects" if readback else "/writes",
                           headers={} if headers is None else headers)
        response = connection.getresponse()
        body = response.read()
        payload = (json.loads(body) if response.headers.get_content_type() == "application/json"
                   else {"body": body.decode("utf-8", errors="replace")})
        return {"http_status": response.status, "response": payload}
    finally:
        connection.close()
