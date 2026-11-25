from __future__ import annotations

import json
from pathlib import Path

import pytest

from tba_protocol_oidc_relying_party import (
    RPError,
    authorization_options,
    resolve_end_session_endpoint,
    validate_logout_return,
)


def _vectors():
    root = Path(__file__).resolve().parents[5]
    return json.loads(
        (root / "tests/fixtures/oidc-rp-session-vectors.json").read_text()
    )


@pytest.mark.parametrize("vector", _vectors()["intents"])
def test_authorization_intent(vector):
    args = vector["intent"], vector.get("acrValues")
    if vector.get("error"):
        with pytest.raises(RPError):
            authorization_options(*args)
    else:
        assert authorization_options(*args) == vector["expected"]


@pytest.mark.parametrize("vector", _vectors()["logout"])
def test_logout_return(vector):
    assert (
        validate_logout_return(
            vector["url"], vector.get("registered", "https://rp.example/out"), "browser"
        )
        is vector["accepted"]
    )


@pytest.mark.parametrize("vector", _vectors()["discovery"])
def test_session_endpoint(vector):
    issuer = "https://authority.example"
    metadata = {
        "issuer": vector.get("metadataIssuer", issuer),
        "end_session_endpoint": vector.get("endpoint"),
    }
    if vector.get("error"):
        with pytest.raises(RPError):
            resolve_end_session_endpoint(metadata, issuer)
    else:
        assert resolve_end_session_endpoint(metadata, issuer) == vector.get("expected")
