# tba-provider-dns-resolver

In-house synchronous and asynchronous DNS resolution, UDP and TCP query
transports, DoT, DoH, and DoQ.

```python
from tba_provider_dns_resolver import Resolver

answer = Resolver().resolve_answer("example.com.", "MX")
for record in answer.records:
    print(record.type, record.ttl)
```

The optional extras provide DoH over HTTP/2 (`http2`), DoQ and HTTP/3
(`quic`), and Trio support (`trio`).
The low-level HTTPS API runs HTTP/2 on asyncio and Trio and HTTP/3 on asyncio.
Discovered encrypted resolvers check the bootstrap address in the certificate
on the connection carrying the query. TCP and TLS queries can reuse connected
caller-owned sockets, and UDP also accepts a caller-owned datagram socket.
Use `transport.quic_session()` to send multiple DoQ queries on a single
verified connection. DoQ and HTTP/3 accept caller-supplied QUIC address tokens.

`AsyncResolver` autodetects asyncio or Trio. Its lookup methods also accept a
`backend=` implementing `asyncbackend.Backend`. For HTTP/1.1 and HTTP/2, pass
a configured `httpx.Client` or `httpx.AsyncClient` as `session=` to reuse the
caller's connection pool. The caller owns the session's lifetime and trust
settings.

Use `asyncquery.https(source=..., source_port=...)` to bind a new HTTP/1.1
or HTTP/2 connection to a local address and port. A borrowed client retains
its own connection configuration.

For native HTTP/3, pass a client `SSLContext` as `verify=`. The QUIC
transport uses its exportable CA certificates, hostname setting, compatible
TLS 1.3 cipher suites, and certificate verification flags. For revocation
checks, attach the CRL material explicitly because Python exposes CA
certificates from an `SSLContext` but does not expose loaded CRLs.

```python
import ssl

from tba_provider_dns_resolver import asyncquery

trust = ssl.create_default_context(cafile="ca.pem")
trust.verify_flags |= ssl.VERIFY_CRL_CHECK_CHAIN
asyncquery.configure_http3_crls(trust, "issuer-crls.pem")
answer = await asyncquery.https(query, endpoint, verify=trust, http_version=3)
```

For mutual TLS across HTTP versions, use `asyncquery.HTTP3SSLContext`.
Its `load_cert_chain()` method configures the same identity for TCP TLS
and native HTTP/3. Supply PEM files in leaf-first order. An encrypted
private key accepts a password or a password callback.

```python
trust = asyncquery.HTTP3SSLContext()
trust.load_verify_locations(cafile="ca.pem")
trust.load_cert_chain("client-chain.pem", "client-key.pem")
answer = await asyncquery.https(query, endpoint, verify=trust, http_version=3)
```

For an existing standard `ssl.SSLContext`, use
`asyncquery.configure_http3_client_identity()` with the original PEM files.
Python does not expose a private key previously loaded into a standard context.
The QUIC client verifies the server before sending its client certificate.

Use [tba-concrete-dns-zone](../../10-concrete/tba-concrete-dns-zone) for local
zones and [tba-protocol-dns](../../50-protocols/tba-protocol-dns) for discovery,
transfers, updates, and authentication. The [DNS tests](../../120-tests/tba-tests-dns)
cover the resolver and transports.
