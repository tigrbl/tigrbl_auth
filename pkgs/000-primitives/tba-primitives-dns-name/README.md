# tba-primitives-dns-name

DNS names with explicit absolute and relative forms, IDNA conversion, canonical
DNS ordering, and reverse address and ENUM names.

```python
from tba_primitives_dns_name.name import from_text

origin = from_text("example.com.")
name = from_text("mail", origin=origin)
assert name.to_text() == "mail.example.com."
```

Verify with the name cases in [the DNS test suite](../../120-tests/tba-tests-dns).
