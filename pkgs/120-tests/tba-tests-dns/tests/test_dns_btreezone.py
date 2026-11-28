"""B-tree zone conformance checked against canonical ordering and flat zones."""

from io import StringIO
from random import Random

import pytest
from tba_codec_dns import rdata, rdataset, rrset
from tba_primitives_dns_name.name import from_text
from tba_concrete_dns_zone.btreezone import NodeFlags, Zone
from tba_concrete_dns_zone.zone import DeleteNotExact, from_file
from tba_concrete_dns_zone.zone import Zone as FlatZone

_ZONE = """$ORIGIN example.
$TTL 300
@ SOA ns hostmaster 1 3600 600 86400 60
@ NS ns
ns A 192.0.2.53
child NS ns.child
ns.child A 192.0.2.51
grand.child NS ns.grand.child
ns.grand.child A 192.0.2.52
x.branch A 192.0.2.1
z.branch A 192.0.2.2
"""


def test_btree_bounds_and_delegations_follow_the_committed_version():
    zone = Zone.from_text(_ZONE)
    initial = zone.version()
    assert initial.get_node("@").flags == NodeFlags.ORIGIN
    assert initial.get_node("child").is_delegation()
    assert initial.get_node("grand.child").is_glue()
    assert initial.get_delegation("x.grand.child") == (from_text("child", None), True)
    empty_nonterminal = initial.bounds("y.branch")
    assert empty_nonterminal.left == from_text("x.branch", None)
    assert empty_nonterminal.right == from_text("z.branch", None)
    assert empty_nonterminal.closest_encloser == from_text("branch", None)
    assert not empty_nonterminal.is_equal
    assert initial.bounds("child").is_delegation
    with zone.writer() as writer:
        writer.delete("child", "NS")
        assert writer.get_node("grand.child").is_delegation()
    assert zone.get_node("grand.child").is_delegation()
    assert initial.get_node("grand.child").is_glue()
    assert zone.version().get_delegation("ns.grand.child") == (
        from_text("grand.child", None),
        True,
    )


def test_btree_shares_pages_and_rebalances_against_flat_zone():
    rng = Random(794)
    sequence = list(range(1200))
    rng.shuffle(sequence)
    structured = Zone("example.", versions=3, relativize=False)
    flat = FlatZone("example.")
    address = rdataset.from_text("IN", "A", 300, "192.0.2.1")
    with structured.writer() as left, flat.writer() as right:
        for i in sequence:
            name = f"h{i:04d}"
            left.replace(name, address)
            right.replace(name, address)
    old = structured.version()
    assert tuple(structured) == tuple(flat)
    assert structured.to_text() == flat.to_text()
    with structured.writer() as change:
        change.delete("h0000")
    updated = structured.version()
    assert old._index._root is not updated._index._root
    assert old._index._root.children[-1] is updated._index._root.children[-1]
    assert old.get_node("h0000") is not None
    assert updated.bounds("h0000").right == from_text("h0001.example.")
    with structured.writer() as left, flat.writer() as right:
        right.delete("h0000")
        for i in sequence:
            if i % 57:
                left.delete(f"h{i:04d}")
                right.delete(f"h{i:04d}")
    assert tuple(structured) == tuple(flat)
    assert structured.to_text() == flat.to_text()
    with structured.writer() as writer:
        for name in tuple(writer.iterate_names()):
            writer.delete(name)
    assert not tuple(structured)
    assert old.get_node("h1199") is not None


def test_btree_optimistic_transactions_historical_readers_and_pruning():
    zone = Zone.from_text(_ZONE)
    zone.set_max_versions(3)
    first = zone.version()
    with zone.reader() as old:
        with zone.writer() as writer:
            writer.update_serial()
        assert old.get("@", "SOA")[0].serial == 1
    with zone.reader(serial=1) as old:
        assert old.get("@", "SOA")[0].serial == 1
    with zone.reader(id=first.id) as old:
        assert old.get("@", "SOA")[0].serial == 1
    with pytest.raises(RuntimeError, match="changed during"):
        with zone.transaction() as losing:
            losing.delete("child")
            with zone.transaction() as winning:
                winning.update_serial()
    assert zone.get_node("child").is_delegation()
    with pytest.raises(ValueError, match="abort"):
        with zone.writer(replacement=True):
            raise ValueError("abort")
    assert zone.get_soa().serial == 3
    zone.set_pruning_policy(lambda _, version: version.id == first.id)
    with pytest.raises(KeyError), zone.reader(id=first.id):
        pytest.fail("pruned historical version still accessible")


def test_transactions_accept_rrsets_and_delete_only_exact_values():
    zone = Zone("example.")
    one, two, missing = (
        rdata.from_text("IN", "A", value)
        for value in ("192.0.2.1", "192.0.2.2", "192.0.2.3")
    )
    with zone.writer() as writer:
        writer.add(rrset.from_rdata("host.example.", 60, one))
        writer.add("host", 120, two)
        assert tuple(writer.get("host", "A")) == (one, two)
        assert writer.get("host", "A").ttl == 60
        with pytest.raises(DeleteNotExact):
            writer.delete_exact("host", rdataset.from_rdata(0, one, missing))
        assert tuple(writer.get("host", "A")) == (one, two)
        writer.delete_exact("host", one)
        assert tuple(writer.get("host", "A")) == (two,)
        writer.replace("host", 120, one)
    assert tuple(zone.get_rdataset("host", "A")) == (one,)


def test_zone_master_ttl_precedence_with_a_file_object():
    text = (
        "@ 120 SOA ns admin 1 1800 600 86400 45\n"
        "@ NS ns\n"
        "ns 60 A 192.0.2.1\n"
        "other A 192.0.2.2\n"
        "$TTL 30\n"
        "last 10 A 192.0.2.3\n"
        "final A 192.0.2.4"
    )
    origin = from_text("example.")
    zone = from_file(StringIO(text), origin, zone_factory=Zone, relativize=False)
    assert zone.get("@", "NS").ttl == 120
    assert zone.get("other", "A").ttl == 60
    assert zone.get("final", "A").ttl == 30
    assert from_text("other.example.") in tuple(zone)
    assert zone.origin_information() == (origin, False, origin)
    legacy = from_file(StringIO(text), origin, rfc2308_ttl=False)
    assert legacy.get("@", "NS").ttl == 45
