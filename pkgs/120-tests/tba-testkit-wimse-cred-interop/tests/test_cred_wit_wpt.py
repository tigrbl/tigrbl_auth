import os
from pathlib import Path

import pytest
from tba_testkit_wimse_cred_interop.peer import CredPeer, start_cred
from tba_testkit_wimse_cred_interop.tokens import WorkloadTokens


@pytest.fixture(scope="module")
def tokens() -> WorkloadTokens:
    return WorkloadTokens()


@pytest.fixture(scope="module")
def cred(tmp_path_factory, tokens):
    checkout = os.getenv("CRED_SDK_CHECKOUT")
    if not checkout:
        pytest.fail("Set CRED_SDK_CHECKOUT to the built, pinned Cred checkout.")
    workdir = tmp_path_factory.mktemp("cred-wimse")
    with start_cred(Path(checkout).resolve(), workdir, tokens.trust_bundle) as peer:
        yield peer


def _accepted(cred: CredPeer, headers: dict[str, str]) -> None:
    status, body = cred.connections(headers)
    assert status == 200, body
    assert {entry["slug"] for entry in body["connections"]} == {"google"}


def _rejected(cred: CredPeer, headers: dict[str, str]) -> None:
    status, body = cred.connections(headers)
    assert status == 401, body
    assert body["error"] == "invalid_workload_identity"


def test_accepts_tigrbl_auth_token_pair(cred, tokens):
    _accepted(cred, tokens.request_headers(tokens.issue_wit(), cred.audience))


@pytest.mark.parametrize("variant", ["wrong_key", "expired"])
def test_rejects_invalid_wit(cred, tokens, variant):
    wit = tokens.issue_wit(**{variant: True})
    _rejected(cred, tokens.request_headers(wit, cred.audience))


@pytest.mark.parametrize("variant", ["wrong_key", "expired"])
def test_rejects_invalid_wpt(cred, tokens, variant):
    wit = tokens.issue_wit()
    _rejected(cred, tokens.request_headers(wit, cred.audience, **{variant: True}))


def test_rejects_wrong_audience(cred, tokens):
    _rejected(
        cred, tokens.request_headers(tokens.issue_wit(), f"{cred.audience}/wrong")
    )


def test_rejects_replay_but_accepts_fresh_proof(cred, tokens):
    wit = tokens.issue_wit()
    headers = tokens.request_headers(wit, cred.audience)
    _accepted(cred, headers)
    _rejected(cred, headers)
    _accepted(cred, tokens.request_headers(wit, cred.audience))
