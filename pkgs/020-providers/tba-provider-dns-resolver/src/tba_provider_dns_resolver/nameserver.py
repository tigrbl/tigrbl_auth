"""Transport-specific DNS nameservers."""

import asyncio
from urllib.parse import urlsplit

from . import asyncquery


class Nameserver:
    def kind(self) -> str:
        raise NotImplementedError

    def is_always_max_size(self) -> bool:
        return False

    def answer_nameserver(self) -> str:
        raise NotImplementedError

    def answer_port(self) -> int:
        raise NotImplementedError

    def query(
        self,
        request,
        timeout,
        source=None,
        source_port=0,
        max_size=False,
        one_rr_per_rrset=False,
        ignore_trailing=False,
    ):
        return asyncio.run(
            self.async_query(
                request,
                timeout,
                source,
                source_port,
                max_size,
                None,
                one_rr_per_rrset,
                ignore_trailing,
            )
        )

    async def async_query(
        self,
        request,
        timeout,
        source=None,
        source_port=0,
        max_size=False,
        backend=None,
        one_rr_per_rrset=False,
        ignore_trailing=False,
    ):
        exchange, options = self._exchange(max_size, backend)
        return await exchange(
            request,
            self.answer_nameserver(),
            timeout=timeout,
            port=self.answer_port(),
            source=source,
            source_port=source_port,
            one_rr_per_rrset=one_rr_per_rrset,
            ignore_trailing=ignore_trailing,
            **options,
        )

    def _exchange(self, max_size, backend):
        raise NotImplementedError


class AddressAndPortNameserver(Nameserver):
    def __init__(self, address, port):
        self.address = address
        self.port = port

    def answer_nameserver(self):
        return self.address

    def answer_port(self):
        return self.port

    def __str__(self):
        return f"{self.kind()}:{self.address}@{self.port}"


class Do53Nameserver(AddressAndPortNameserver):
    def __init__(self, address, port=53):
        super().__init__(address, port)

    def kind(self):
        return "Do53"

    def _exchange(self, max_size, backend):
        if max_size:
            return asyncquery.tcp, {"backend": backend}
        return asyncquery.udp, {
            "backend": backend,
            "raise_on_truncation": True,
            "ignore_unexpected": True,
            "ignore_errors": True,
        }


class DoTNameserver(AddressAndPortNameserver):
    def __init__(self, address, port=853, hostname=None, verify=True):
        super().__init__(address, port)
        self.hostname = hostname
        self.verify = verify

    def kind(self):
        return "DoT"

    def _exchange(self, max_size, backend):
        return asyncquery.tls, {
            "backend": backend,
            "server_hostname": self.hostname,
            "verify": self.verify,
        }


class DoQNameserver(AddressAndPortNameserver):
    def __init__(self, address, port=853, verify=True, server_hostname=None):
        super().__init__(address, port)
        self.verify = verify
        self.server_hostname = server_hostname

    def kind(self):
        return "DoQ"

    def _exchange(self, max_size, backend):
        return asyncquery.quic, {
            "backend": backend,
            "server_hostname": self.server_hostname,
            "verify": self.verify,
        }


class DoHNameserver(Nameserver):
    def __init__(
        self,
        url,
        bootstrap_address=None,
        verify=True,
        want_get=False,
        http_version=asyncquery.HTTPVersion.DEFAULT,
    ):
        self.url = url
        self.bootstrap_address = bootstrap_address
        self.verify = verify
        self.want_get = want_get
        self.http_version = http_version

    def kind(self):
        return "DoH"

    def is_always_max_size(self):
        return True

    def answer_nameserver(self):
        return self.url

    def answer_port(self):
        return urlsplit(self.url).port or 443

    def __str__(self):
        return self.url

    def _exchange(self, max_size, backend):
        return asyncquery.https, {
            "bootstrap_address": self.bootstrap_address,
            "verify": self.verify,
            "post": not self.want_get,
            "http_version": self.http_version,
        }
