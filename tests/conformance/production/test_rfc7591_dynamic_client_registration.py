from tigrbl_auth import rfc7591


def test_rfc7591_protocol_owner_is_published() -> None:
    assert rfc7591.RFC7591_SPEC_URL == "https://www.rfc-editor.org/rfc/rfc7591"
    assert rfc7591.OWNER.public_surface == ("/register",)
