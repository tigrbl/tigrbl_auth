import asyncio
from uuid import uuid4

import pytest

from tba_protocol_oidc.standards import rp_initiated_logout as rp_logout


@pytest.mark.parametrize(
    ("requested", "accepted"),
    [
        ("https://rp.example/", True),
        ("https://rp.example", False),
        ("https://rp.example:443/", False),
        ("https://rp.example/?state=untrusted", False),
    ],
)
def test_logout_redirect_matches_registered_uri_exactly(requested, accepted):
    result = rp_logout.validate_post_logout_redirect_uri(
        client_id=uuid4(),
        post_logout_redirect_uri=requested,
        registration_metadata={"post_logout_redirect_uris": ["https://rp.example/"]},
    )
    if accepted:
        assert asyncio.run(result) == requested
    else:
        with pytest.raises(rp_logout.HTTPException) as error:
            asyncio.run(result)
        assert error.value.status_code == 400
        assert error.value.detail["error"] == "invalid_request"
