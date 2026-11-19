"""Reject missing legal material and counters accidentally shared by packages."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import shutil

import pytest

ROOT = Path(__file__).resolve().parents[5]
SPEC = importlib.util.spec_from_file_location(
    "package_standards", ROOT / "scripts/verify_package_standards.py"
)
standards = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(standards)


@pytest.fixture
def package_fixture(tmp_path):
    for name in ("LICENSE", "NOTICE"):
        shutil.copyfile(ROOT / name, tmp_path / name)
    brand = tmp_path / "docs/assets/tba-brand.png"
    brand.parent.mkdir(parents=True)
    brand.write_bytes(b"\x89PNG\r\n\x1a\n")
    relative = Path("pkgs/002-contracts/tba-contracts-dns")
    shutil.copytree(ROOT / relative, tmp_path / relative)
    return tmp_path, tmp_path / relative


def test_valid_package_has_its_own_counters_and_legal_files(package_fixture):
    root, _ = package_fixture
    result = standards.verify(root)
    assert result["passed"], result["failures"]


def test_notice_must_be_in_the_package(package_fixture):
    root, package = package_fixture
    (package / "NOTICE").unlink()
    assert any(
        "missing NOTICE" in failure for failure in standards.verify(root)["failures"]
    )


def test_notice_must_attribute_the_correct_distribution(package_fixture):
    root, package = package_fixture
    (package / "NOTICE").write_text("Distribution: another-package\n")
    assert any(
        "NOTICE attribution" in failure
        for failure in standards.verify(root)["failures"]
    )


def test_download_badge_cannot_count_another_project(package_fixture):
    root, package = package_fixture
    readme = package / "README.md"
    readme.write_text(
        readme.read_text().replace(
            "static.pepy.tech/badge/tba-contracts-dns/month",
            "static.pepy.tech/badge/tba-auth/month",
        )
    )
    assert any(
        "download counter" in failure for failure in standards.verify(root)["failures"]
    )


def test_hit_badge_cannot_count_another_readme(package_fixture):
    root, package = package_fixture
    readme = package / "README.md"
    readme.write_text(
        readme.read_text().replace(
            "002-contracts/tba-contracts-dns/README.md.svg",
            "070-facade/tba-auth/README.md.svg",
        )
    )
    assert any(
        "hit counter" in failure for failure in standards.verify(root)["failures"]
    )


def test_brand_fragment_must_have_balanced_html(package_fixture):
    root, package = package_fixture
    readme = package / "README.md"
    readme.write_text(readme.read_text().replace("</p>", "", 1))
    assert any("branding" in failure for failure in standards.verify(root)["failures"])


def test_license_must_be_the_exact_apache_text(package_fixture):
    root, package = package_fixture
    (package / "LICENSE").write_text("Apache-2.0")
    assert any(
        "LICENSE differs" in failure for failure in standards.verify(root)["failures"]
    )


def test_shared_brand_image_must_be_valid(package_fixture):
    root, _ = package_fixture
    (root / "docs/assets/tba-brand.png").write_text("not an image")
    assert any("not a PNG" in failure for failure in standards.verify(root)["failures"])
