"""Read-only dataset and node views for committed zone versions."""

from types import MappingProxyType

from tba_codec_dns.node import Node
from tba_codec_dns.rdataset import Rdataset


class ImmutableRdataset(Rdataset):
    def __init__(self, dataset):
        object.__setattr__(self, "rdclass", dataset.rdclass)
        object.__setattr__(self, "rdtype", dataset.rdtype)
        object.__setattr__(self, "covers", dataset.covers)
        object.__setattr__(self, "ttl", dataset.ttl)
        object.__setattr__(self, "_values", MappingProxyType(dict.fromkeys(dataset)))

    def __setattr__(self, name, value):
        raise TypeError("DNS version dataset is immutable")

    def __delattr__(self, name):
        raise TypeError("DNS version dataset is immutable")

    def _reject_edit(self, *args, **kwargs):
        raise TypeError("DNS version dataset is immutable")

    add = discard = update_ttl = update = _reject_edit


class VersionedNode(Node):
    """Mutable working node for a DNS zone version."""


class ImmutableVersionedNode(VersionedNode):
    def __init__(self, rdatasets=()):
        datasets = {
            (d.rdclass, d.rdtype, d.covers): ImmutableRdataset(d) for d in rdatasets
        }
        object.__setattr__(self, "_sets", MappingProxyType(datasets))

    def __setattr__(self, name, value):
        raise TypeError("DNS version node is immutable")

    def __delattr__(self, name):
        raise TypeError("DNS version node is immutable")

    def find_rdataset(self, rdclass, rdtype, covers=0, create=False):
        if create:
            raise TypeError("DNS version node is immutable")
        return super().find_rdataset(rdclass, rdtype, covers)

    def delete_rdataset(self, *args, **kwargs):
        raise TypeError("DNS version node is immutable")

    def replace_rdataset(self, dataset):
        raise TypeError("DNS version node is immutable")
