import pytest

from tigrbl_auth.security.certification import (
    CertificationError,
    assert_issuer_consistency,
    deterministic_issuer,
)


def test_issuer_confusion_t0_contract_exports_deterministic_derivation() -> None:
    assert callable(deterministic_issuer)


def test_issuer_confusion_t1_derives_realm_and_tenant_issuers() -> None:
    issuer = deterministic_issuer(
        "https://auth.example.test/",
        realm_slug="acme",
        tenant_slug="northwind",
    )

    assert issuer == "https://auth.example.test/realms/acme/tenants/northwind"
    assert_issuer_consistency(
        expected_issuer=issuer,
        metadata_issuer=issuer,
        token_issuer=issuer,
        jwks_uri=f"{issuer}/.well-known/jwks.json",
        allowed_jwks_uri=f"{issuer}/.well-known/jwks.json",
    )


def test_issuer_confusion_t2_rejects_alias_and_host_header_style_mismatch() -> None:
    expected = deterministic_issuer("https://auth.example.test", realm_slug="acme")

    with pytest.raises(CertificationError, match="metadata issuer mismatch"):
        assert_issuer_consistency(
            expected_issuer=expected,
            metadata_issuer="https://evil.example.test/realms/acme",
        )

    with pytest.raises(CertificationError, match="base_issuer"):
        deterministic_issuer("http://evil.example.test", realm_slug="acme")
