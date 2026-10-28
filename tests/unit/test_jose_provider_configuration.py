from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from tba_provider_identity_jose.configuration import (
    configure_jose_provider,
    jose_provider_source,
    settings,
)
from tba_concrete_jose import verify_certificate_thumbprint_confirmation


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
    package = ROOT / "pkgs/20-providers/tba-provider-identity-jose/src/tba_provider_identity_jose"
    sources = list(package.rglob("*.py"))
    combined = "\n".join(path.read_text(encoding="utf-8") for path in sources)
    assert "tba_runtime_identity" not in combined
    assert "tba_protocol_oauth" not in combined
    assert "swarmauri" not in combined.lower()

    manifest = (package.parents[1] / "pyproject.toml").read_text(encoding="utf-8")
    assert "swarmauri" not in manifest.lower()


def test_certificate_thumbprint_confirmation_is_deterministic() -> None:
    payload = {"cnf": {"x5t#S256": "thumbprint"}}
    assert verify_certificate_thumbprint_confirmation(payload, "thumbprint")
    assert not verify_certificate_thumbprint_confirmation(payload, "different")
    assert not verify_certificate_thumbprint_confirmation({}, "thumbprint")
