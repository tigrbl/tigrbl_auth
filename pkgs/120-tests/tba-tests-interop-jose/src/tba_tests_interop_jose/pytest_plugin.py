"""Select checkout or installed-wheel JOSE peers for the interop tests."""

import os
from importlib import import_module, metadata
from pathlib import Path

import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.getgroup("TbA JOSE interoperability").addoption(
        "--jose-interop-mode",
        choices=("auto", "source", "installed"),
        default="auto",
        help="Load the Swarmauri checkout or require installed wheels for both peers.",
    )


def _check_wheel_import(distribution: str, module_name: str) -> None:
    dist = metadata.distribution(distribution)
    module = import_module(module_name)
    path = Path(module.__file__).resolve()
    package_init = module_name.replace(".", "/") + "/__init__.py"
    if not any(
        entry.as_posix() == package_init
        and Path(dist.locate_file(entry)).resolve() == path
        for entry in dist.files or ()
    ):
        pytest.fail(
            f"{module_name} did not load from the installed {distribution} wheel"
        )


@pytest.fixture
def swarmauri_jwe(pytestconfig: pytest.Config, monkeypatch: pytest.MonkeyPatch):
    mode = pytestconfig.getoption("--jose-interop-mode")
    checkout = os.environ.get("SWARMAURI_SDK_ROOT")
    if mode == "installed":
        for distribution, module in (
            ("swarmauri-core", "swarmauri_core"),
            ("swarmauri-crypto-jwe", "swarmauri_crypto_jwe"),
            ("tba-capability-protected-envelope", "tba_capability_protected_envelope"),
            ("tba-concrete-jose", "tba_concrete_jose"),
            ("tba-concrete-jwe", "tba_concrete_jwe"),
            ("tba-contracts-protected-envelope", "tba_contracts_protected_envelope"),
            ("tba-primitives-identity", "tba_primitives_identity"),
            ("tba-protocol-security-jwe", "tba_protocol_security_jwe"),
            ("tba-provider-jose-cryptography", "tba_provider_jose_cryptography"),
        ):
            _check_wheel_import(distribution, module)
    elif checkout:
        packages = Path(checkout).resolve(strict=True) / "pkgs"
        monkeypatch.syspath_prepend(str(packages / "core"))
        monkeypatch.syspath_prepend(
            str(packages / "standards" / "swarmauri_crypto_jwe")
        )
        for name in ("swarmauri_core", "swarmauri_crypto_jwe"):
            if (
                not Path(import_module(name).__file__)
                .resolve()
                .is_relative_to(packages)
            ):
                pytest.fail(f"{name} did not load from SWARMAURI_SDK_ROOT")
    elif mode == "source":
        pytest.fail("Set SWARMAURI_SDK_ROOT to the Swarmauri checkout")
    else:
        pytest.skip("Set SWARMAURI_SDK_ROOT or select --jose-interop-mode=installed")

    from swarmauri_core.crypto.types import JWAAlg
    from swarmauri_crypto_jwe import JweCrypto

    return JweCrypto(enable_x448=True), JWAAlg
