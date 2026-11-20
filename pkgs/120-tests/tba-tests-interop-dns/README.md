# tba-tests-interop-dns

Run the GSS-TSIG interoperability probe against BIND 9.20.31 and an MIT Kerberos
KDC. The container generates fixture credentials and exchanges DNS packets on
its loopback interface. The probe installs the production wheels from a
read-only mount.

Run from the repository root.

```bash
uv build --wheel --out-dir dist/dns pkgs/00-primitives/tba-primitives-dns-name
uv build --wheel --out-dir dist/dns pkgs/03-codecs/tba-codec-dns
uv build --wheel --out-dir dist/dns pkgs/10-concrete/tba-concrete-dns-zone
uv build --wheel --out-dir dist/dns pkgs/20-providers/tba-provider-dns-resolver
uv build --wheel --out-dir dist/dns pkgs/50-protocols/tba-protocol-dns
docker build -t tba-dns-gss-interop:local pkgs/120-tests/tba-tests-interop-dns
docker run --rm --network none --mount "type=bind,source=${PWD}/dist/dns,target=/wheels,readonly" tba-dns-gss-interop:local
```

The probe checks authenticated TKEY negotiation, a signed UPDATE and reply,
policy denial, and rejection of a tampered message.
