# tba-tests-dns

Unit and loopback integration tests for DNS names, wire messages, record codecs,
resolvers, transports, zones, and the TXT adapter. Run from the repository root.

```bash
uv run --locked --extra test pytest pkgs/120-tests/tba-tests-dns/tests
```

The [peer suite](../tba-tests-interop-dns) covers BIND and Kerberos separately.
