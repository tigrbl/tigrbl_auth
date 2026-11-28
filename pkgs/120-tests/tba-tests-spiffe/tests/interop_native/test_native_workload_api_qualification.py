"""Verify credential delivery and the fixture's transport boundary."""

from pathlib import Path

import pytest

grpc = pytest.importorskip("grpc")
pytest.importorskip("google.protobuf")

from support.native_workload_api import ENROLLED, HEADER, IDENTITY, native_workload_api


def test_registered_workload_gets_fresh_x509_svid(tmp_path):
    with native_workload_api() as api:
        first = api.fetch(enrolled=True)
        second = api.fetch(enrolled=True)
        assert first.fingerprint != second.fingerprint
        assert first.bundle == second.bundle
        caller, receiver = first.issue_pair(tmp_path, (IDENTITY,), "spiffe://example.org/workload-1")
        assert caller.trust_anchor == receiver.trust_anchor
        assert Path(caller.private_key).read_bytes() != Path(receiver.private_key).read_bytes()


def test_enrollment_cannot_be_supplied_by_the_caller():
    with native_workload_api() as api:
        assert api.fetch(enrolled=False, metadata=(HEADER, ("tls-san", ENROLLED))) is None


def test_workload_header_is_required():
    with native_workload_api() as api:
        with pytest.raises(ValueError, match="FetchX509SVID: INVALID_ARGUMENT"):
            api.fetch(enrolled=True, metadata=())
