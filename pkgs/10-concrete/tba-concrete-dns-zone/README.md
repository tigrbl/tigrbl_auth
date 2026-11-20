# tba-concrete-dns-zone

DNS master files, in-memory zones, transactions, and immutable versions.

Use `BTreeZone` for copy-on-write versions in canonical name order.

```python
from tba_concrete_dns_zone.btreezone import Zone as BTreeZone

zone = BTreeZone.from_text(
    "$ORIGIN example.com.\n"
    "$TTL 300\n"
    "@ SOA ns admin 1 1800 600 86400 60\n"
    "@ NS ns\n"
    "ns A 192.0.2.53\n"
)

before = zone.version()
with zone.writer() as transaction:
    transaction.update_serial()

assert before.bounds("ns").is_equal
assert zone.get_soa().serial == 2
```

B-tree versions expose delegation and glue flags, name bounds, and the closest
encloser. Set a version retention limit to look up historical snapshots by ID
or SOA serial. Transaction hooks can reject an edit before it commits, and
zone subclasses can supply their own version factories.
