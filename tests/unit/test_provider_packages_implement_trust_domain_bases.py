from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROVIDERS = ROOT / "pkgs" / "30-providers"


def test_pqc_provider_inherits_signing_domain_base() -> None:
    from tigrbl_security_signing_pqc import PQCSigningProvider
    from tigrbl_security_trust_domain_bases import SigningDomainBase

    assert issubclass(PQCSigningProvider, SigningDomainBase)
    assert "ML-DSA-65" in PQCSigningProvider().supports().algs


def test_provider_packages_expose_trust_domain_base_implementers() -> None:
    packages = [path for path in PROVIDERS.iterdir() if (path / "pyproject.toml").exists()]
    assert packages

    offenders: list[str] = []
    for package in packages:
        implementers: list[str] = []
        for path in (package / "src").rglob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if not isinstance(node, ast.ClassDef):
                    continue
                base_names = {
                    getattr(base, "id", getattr(base, "attr", ""))
                    for base in node.bases
                }
                if any(name.endswith("DomainBase") for name in base_names):
                    implementers.append(f"{path.relative_to(package)}::{node.name}")
        if not implementers:
            offenders.append(package.name)

    assert offenders == []
