from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from tigrbl_identity_jose.configuration import (
    configure_jose_provider,
    jose_provider_source,
    settings,
)
from tigrbl_jose_concrete import verify_certificate_thumbprint_confirmation


ROOT = Path(__file__).resolve().parents[2]


def test_provider_configuration_is_injected_without_runtime_import() -> None:
    original = jose_provider_source()
    source = SimpleNamespace(enable_rfc7515=False)
    try:
        configure_jose_provider(source)
        assert settings.enable_rfc7515 is False
        source.enable_rfc7515 = True
        assert settings.enable_rfc7515 is True
    finally:
        configure_jose_provider(original)


def test_provider_and_rfc_modules_do_not_import_higher_layers() -> None:
    package = ROOT / "pkgs/20-providers/tigrbl-identity-jose/src/tigrbl_identity_jose"
    sources = [package / "jwt_runtime.py", *(package / "standards").glob("*.py")]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in sources)
    assert "tigrbl_identity_runtime" not in combined
    assert "tigrbl_auth_protocol_oauth" not in combined


def test_certificate_thumbprint_confirmation_is_deterministic() -> None:
    payload = {"cnf": {"x5t#S256": "thumbprint"}}
    assert verify_certificate_thumbprint_confirmation(payload, "thumbprint")
    assert not verify_certificate_thumbprint_confirmation(payload, "different")
    assert not verify_certificate_thumbprint_confirmation({}, "thumbprint")
