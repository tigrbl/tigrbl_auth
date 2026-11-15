"""Run the pinned Cred and TbA request signers and verifiers over HTTPS."""

import os

import pytest

from support.cred_endpoint import CredHttpSignatureAdapter, build_cred_bridge
from tba_test_interop_wimse.matrix import generate_matrix


@pytest.fixture(scope="module")
def adapter(tmp_path_factory):
    checkout = os.getenv("TBA_WIMSE_CRED_CHECKOUT")
    if not checkout:
        pytest.skip("Set TBA_WIMSE_CRED_CHECKOUT to the pinned Cred SDK checkout")
    directory = tmp_path_factory.mktemp("cred-signatures")
    return CredHttpSignatureAdapter(directory, build_cred_bridge(checkout, directory / "bridge"))


@pytest.mark.parametrize("direction", ("forward", "reverse"), ids=("tba-to-cred", "cred-to-tba"))
@pytest.mark.parametrize("variant", ("valid-peer", "local-token", "token-binding-mismatch"))
def test_cred_http_signature(adapter, direction, variant):
    case, = (case for case in generate_matrix()["scenarios"]
             if case["variant"] == variant and adapter.supports(case))
    with adapter.isolated(case, {"direction": direction}) as fixture:
        observed = fixture.observe()
    if variant == "token-binding-mismatch":
        assert (observed.decision, observed.effects) == ("deny", 0)
        reason = ("bad_signature: signature invalid" if direction == "forward"
                  else "HTTP signature verification failed")
        assert observed.reason == reason
    else:
        assert (observed.decision, observed.effects) == ("allow", 1)
