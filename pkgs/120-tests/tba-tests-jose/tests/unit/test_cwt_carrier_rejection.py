import pytest
from tba_protocol_cwt.profile import CwtProfile


def test_cwt_profile_rejects_unselected_cose_carrier() -> None:
    profile = CwtProfile("signed-cwt", frozenset({1, 2, 4}), frozenset({"Sign1"}))
    with pytest.raises(ValueError, match="COSE message type not allowed"):
        profile.validate({1: "issuer", 2: "subject", 4: 200}, "Mac0")
