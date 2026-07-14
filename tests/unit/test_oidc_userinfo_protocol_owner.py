from tigrbl_auth_protocol_oidc.standards.core import (
    OIDC_CORE_COMPONENTS,
    USERINFO_OWNER,
    describe_userinfo,
)
from tigrbl_auth_protocol_oidc.standards.userinfo import (
    OIDC_USERINFO_SPEC_URL,
    USERINFO_SCOPE_CLAIMS,
)


def test_userinfo_protocol_owner_is_descriptive_and_versioned() -> None:
    description = describe_userinfo()

    assert "userinfo" in OIDC_CORE_COMPONENTS
    assert USERINFO_OWNER.public_surface == ("/userinfo",)
    assert description["specification_uri"] == OIDC_USERINFO_SPEC_URL
    assert description["methods"] == ("GET",)
    assert description["bearer_token_required"] is True
    assert USERINFO_SCOPE_CLAIMS["openid"] == ("sub",)


def test_userinfo_protocol_owner_does_not_mount_runtime_carrier() -> None:
    import tigrbl_auth_protocol_oidc.standards.userinfo as userinfo

    assert not hasattr(userinfo, "router")
    assert not hasattr(userinfo, "include_oidc_userinfo")
