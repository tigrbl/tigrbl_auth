"""Repository integration regressions for the published shared README policy."""

from pathlib import Path
import shutil
import sys
import pytest

if sys.version_info < (3, 11):
    pytest.skip("readme-standards requires Python 3.11+", allow_module_level=True)

from readme_standards.document import parse
from readme_standards.policy import SECTIONS

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "scripts"))
from verify_readme_standards import verify


def test_policy_keeps_all_required_topics_and_hierarchy():
    assert len(SECTIONS) == 55
    assert {
        "Overview",
        "Features",
        "Prerequisites",
        "Quick Start",
        "Package Boundary",
        "Injected Dependencies",
        "Protocol Consumers",
        "Governance",
        "Verification",
        "Certification Status",
        "License",
        "Notices",
    } <= {s.title for s in SECTIONS}
    assert next(s for s in SECTIONS if s.id == "uv").parent == "installation"
    assert next(s for s in SECTIONS if s.id == "uv").level == 4


def test_push_pull_request_quality_and_release_workflows_keep_the_gate():
    workflows = ROOT / ".github/workflows"
    dedicated = (workflows / "readme-standards.yml").read_text(encoding="utf-8")
    assert "  workflow_call:" in dedicated and "  push:" in dedicated
    callers = [
        path.read_text("utf-8")
        for name in ("pr.yml", "readme-pr.yml")
        if (path := workflows / name).is_file()
    ]
    assert any(
        "  pull_request:" in caller
        and "readme-standards.yml@" in caller
        and "paths:" not in caller
        for caller in callers
    )
    assert "paths:" not in dedicated
    assert "--readme-all" in dedicated
    for name in (
        "readme-standards.yml",
        "_quality.yml",
        "monorepo-package-release.yml",
    ):
        source = (workflows / name).read_text("utf-8")
        assert "scripts/verify_readme_standards.py" in source
        assert "readme-standards==0.1.3" in source


@pytest.fixture
def package_fixture(tmp_path):
    relative = Path("pkgs/002-contracts/tba-contracts-dns")
    shutil.copytree(ROOT / relative, tmp_path / relative)
    shutil.copytree(ROOT / "tools/readme", tmp_path / "tools/readme")
    return tmp_path, tmp_path / relative / "README.md"


def test_complete_package_passes(package_fixture):
    root, _ = package_fixture
    result = verify(root)
    assert result["passed"], result["failures"]


@pytest.mark.parametrize("section", SECTIONS, ids=lambda section: section.id)
def test_every_required_section_is_enforced(package_fixture, section):
    root, readme = package_fixture
    text = readme.read_text("utf-8")
    text = text.replace("#" * section.level + " " + section.title + "\n", "", 1)
    readme.write_text(text, encoding="utf-8")
    assert any(
        "heading.missing" in failure and section.title in failure
        for failure in verify(root)["failures"]
    )


@pytest.mark.parametrize("body", ["", "TODO: document the boundary", "N/A"])
def test_empty_placeholder_or_unexplained_applicability_fails(package_fixture, body):
    root, readme = package_fixture
    text = readme.read_text("utf-8")
    start = text.index("### Summary\n") + len("### Summary\n")
    end = text.index("### Why This Package")
    readme.write_text(
        text[:start] + "\n" + body + "\n\n" + text[end:], encoding="utf-8"
    )
    assert any("content." in failure for failure in verify(root)["failures"])


def test_heading_inside_code_cannot_satisfy_missing_section(package_fixture):
    root, readme = package_fixture
    text = readme.read_text("utf-8").replace("### Non-Goals\n", "", 1)
    text += "\n```markdown\n### Non-Goals\n```\n"
    readme.write_text(text, encoding="utf-8")
    assert any(
        "heading.missing" in failure and "Non-Goals" in failure
        for failure in verify(root)["failures"]
    )


def test_wrong_parent_and_order_fail(package_fixture):
    root, readme = package_fixture
    text = readme.read_text("utf-8").replace("#### uv", "### uv", 1)
    readme.write_text(text, encoding="utf-8")
    assert any(
        "heading.level" in failure or "heading.parent" in failure
        for failure in verify(root)["failures"]
    )


def test_missing_readme_is_reported(package_fixture):
    root, readme = package_fixture
    readme.unlink()
    assert any("missing README" in failure for failure in verify(root)["failures"])


def test_invalid_maintained_python_example_fails(package_fixture):
    root, readme = package_fixture
    (readme.parent / "docs/readme/quick_start.py").write_text(
        "def broken(\n", encoding="utf-8"
    )
    assert any("example.syntax" in failure for failure in verify(root)["failures"])


def test_package_name_is_the_only_variable_heading(package_fixture):
    _, readme = package_fixture
    headings, _ = parse(readme.read_text("utf-8"))
    assert headings[0].title == "tba-contracts-dns"
    assert [(h.level, h.title) for h in headings[1:]] == [
        (s.level, s.title) for s in SECTIONS
    ]
