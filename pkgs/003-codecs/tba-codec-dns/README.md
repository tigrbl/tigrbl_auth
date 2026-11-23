# tba-codec-dns

Use `wire` for complete DNS messages and `rdata` for individual resource record
payloads. The package also provides RRsets, EDNS options, and DNS presentation
formats.

```python
from tba_codec_dns import rdata, wire

query = wire.make_query("example.com.", "MX")
assert wire.Message.from_wire(query.to_wire()) == query

record = rdata.from_text("IN", "MX", "10 mail.example.com.")
assert rdata.from_wire("IN", "MX", record.to_wire()) == record
```

Use `rdata.get_rdata_class()` for type-specific constructors and field access.
DNS messages support opt-in TSIG signing and parser verification with a key or
keyring. Pass `continue_on_error=True` to collect recoverable errors with
their byte offsets, or use `Message.rrsets()` for grouped records.

```python
from tba_codec_dns.tsig import TsigKey

key = TsigKey((b"key", b"example"), b"example shared secret")
outgoing = query.use_tsig(key).to_wire()
incoming = wire.from_wire(outgoing, keyring=key)
assert incoming.had_tsig
```

Omitting the wire parser's keyring retains the parse-only behavior of existing
callers. Supply a key or keyring when the caller requires authentication.

Verify with the codec cases in [the DNS test suite](../../120-tests/tba-tests-dns).
