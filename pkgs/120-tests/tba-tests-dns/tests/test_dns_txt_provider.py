"""Compatibility TXT adapter behavior."""

import pickle
from importlib import import_module
from unittest.mock import Mock

import pytest
from tba_codec_dns.wire import WireError
from tba_contracts_dns import TxtResult, TxtStatus
from tba_provider_dns_resolver.client import NXDOMAIN, NoAnswer, NoNameservers
from tba_provider_dns_txt import DnsTxtResolver


@pytest.mark.parametrize(
    ("package", "modules"),
    (
        ("tba_primitives_dns_name", "name names reversename e164"),
        (
            "tba_codec_dns",
            "wire rdata rdataset rrset node edns svcb record_formats tkey presentation",
        ),
        (
            "tba_provider_dns_resolver",
            "async_transport client system_resolver transport tsig",
        ),
    ),
)
def test_legacy_imports_share_the_canonical_modules(package, modules):
    for module in modules.split():
        assert import_module(f"tba_provider_dns_txt.{module}") is import_module(
            f"{package}.{module}"
        )


def test_legacy_class_paths_still_unpickle():
    # A trusted protocol-zero reference records the historic module path.
    message = pickle.loads(b"ctba_provider_dns_txt.wire\nMessage\n.")
    assert message is import_module("tba_codec_dns.wire").Message


def test_dns_joins_segments_only_within_each_txt_record():
    transport = Mock()
    transport.resolve.return_value = [Mock(strings=(b"a", b"b")), Mock(strings=(b"c",))]
    result = DnsTxtResolver(timeout=1, resolver=transport).lookup_txt("example.com")
    assert result == TxtResult(TxtStatus.FOUND, (b"ab", b"c"))
    transport.resolve.assert_called_once_with(
        "example.com.", "TXT", search=False, lifetime=1
    )


@pytest.mark.parametrize(
    ("error", "status"),
    [
        (NXDOMAIN, TxtStatus.ABSENT),
        (NoAnswer, TxtStatus.ABSENT),
        (TimeoutError, TxtStatus.TEMPORARY_FAILURE),
        (NoNameservers, TxtStatus.TEMPORARY_FAILURE),
        (WireError, TxtStatus.TEMPORARY_FAILURE),
    ],
)
def test_dns_distinguishes_missing_and_temporary_failure(error, status):
    transport = Mock()
    transport.resolve.side_effect = error
    assert DnsTxtResolver(resolver=transport).lookup_txt("example.com").status is status
