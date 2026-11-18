"""Regression coverage for the minimum README content and managed badge gate."""

from pathlib import Path
import re
import shutil
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from readme_policy import REQUIRED_SECTIONS, key, section_errors, split_sections
from verify_readme_standards import verify


def test_policy_cannot_drop_the_required_documentation_topics():
    assert set(REQUIRED_SECTIONS) == {
        "AEO Summary",
        "When to use it",
        "Installation",
        "Quick start",
        "Usage",
        "Package Boundary",
        "Injected dependencies",
        "Operations and readiness",
        "Protocol consumers",
        "Non-goals",
        "Related Packages",
        "Project Links",
        "Governance",
        "Verification",
    }


def test_push_pull_request_quality_and_release_workflows_keep_the_gate():
    workflows = ROOT / ".github/workflows"
    dedicated = (workflows / "readme-standards.yml").read_text(encoding="utf-8")
    assert "  pull_request:" in dedicated and "  push:" in dedicated
    assert "paths:" not in dedicated
    for name in (
        "readme-standards.yml",
        "_quality.yml",
        "monorepo-package-release.yml",
    ):
        assert "scripts/verify_readme_standards.py" in (workflows / name).read_text(
            encoding="utf-8"
        )


@pytest.fixture
def package_fixture(tmp_path):
    relative = Path("pkgs/02-contracts/tba-contracts-dns")
    shutil.copytree(ROOT / relative, tmp_path / relative)
    return tmp_path, tmp_path / relative / "README.md"


def without_section(text, title, replacement=None):
    preamble, sections, _ = split_sections(text)
    result = [preamble]
    for heading, body in sections:
        if key(heading) == key(title):
            if replacement is not None:
                result.append(f"## {heading}\n\n{replacement}")
        else:
            result.append(f"## {heading}\n\n{body}")
    return "\n\n".join(result) + "\n"


def test_complete_package_passes(package_fixture):
    root, _ = package_fixture
    assert verify(root)["passed"]


@pytest.mark.parametrize("title", REQUIRED_SECTIONS)
def test_each_required_section_is_enforced(package_fixture, title):
    root, readme = package_fixture
    readme.write_text(without_section(readme.read_text(), title), encoding="utf-8")
    assert any(title in failure for failure in verify(root)["failures"])


@pytest.mark.parametrize(
    "body", ["", "TODO", "TBD", "N/A", "<!-- description will go here -->"]
)
def test_empty_and_placeholder_sections_do_not_pass(package_fixture, body):
    root, readme = package_fixture
    readme.write_text(
        without_section(readme.read_text(), "Governance", body), encoding="utf-8"
    )
    assert any("Governance" in failure for failure in verify(root)["failures"])


def test_heading_inside_an_example_cannot_satisfy_policy(package_fixture):
    _, readme = package_fixture
    text = without_section(readme.read_text(), "Governance")
    text += "\n```markdown\n## Governance\nThis is a fenced example, not documentation.\n```\n"
    assert any("Governance" in failure for failure in section_errors(text))


def test_subheading_cannot_replace_a_required_section(package_fixture):
    _, readme = package_fixture
    text = readme.read_text().replace("## Governance\n", "### Governance\n")
    assert any("Governance" in failure for failure in section_errors(text))


def test_duplicate_required_section_is_rejected(package_fixture):
    _, readme = package_fixture
    text = (
        readme.read_text()
        + "\n## governance\n\nAnother substantive but duplicate governance explanation.\n"
    )
    assert any(
        "Governance" in failure and "found 2" in failure
        for failure in section_errors(text)
    )


def test_unclosed_fence_is_rejected(package_fixture):
    _, readme = package_fixture
    assert "unclosed Markdown code fence" in section_errors(
        readme.read_text() + "\n```python\nx = 1\n"
    )


@pytest.mark.parametrize(
    "alt",
    [
        "Layer:",
        "SSOT:",
        "License:",
        "Notice:",
        "Checkout:",
        "Python:",
        "PyPI version for",
        "Monthly PyPI downloads for",
        "README hits for",
        "Evidence:",
    ],
)
def test_all_required_badges_are_enforced(package_fixture, alt):
    root, readme = package_fixture
    text = readme.read_text()
    modified, count = re.subn(
        r'<a[^>]*><img alt="' + re.escape(alt) + r"[^>]*></a>", "", text, count=1
    )
    assert count == 1
    readme.write_text(modified, encoding="utf-8")
    assert any("badges differ" in failure for failure in verify(root)["failures"])


def test_wrong_layer_badge_fails_even_with_correct_section_headings(package_fixture):
    root, readme = package_fixture
    readme.write_text(
        readme.read_text().replace(
            'alt="Layer: 02 contracts"', 'alt="Layer: 40 capabilities"'
        ),
        encoding="utf-8",
    )
    assert any("badges differ" in failure for failure in verify(root)["failures"])


def test_broken_python_usage_example_is_rejected(package_fixture):
    root, readme = package_fixture
    readme.write_text(
        without_section(
            readme.read_text(),
            "Usage",
            "Use this package through its declared public entry point.\n\n```python\ndef broken(:\n```",
        ),
        encoding="utf-8",
    )
    assert any(
        "invalid Python example" in failure for failure in verify(root)["failures"]
    )


def test_specialist_sections_and_fenced_comments_survive_structure_parsing():
    text = "# Example\n\n## Usage\n\n```bash\n# a comment\n## not a heading\n```\n\n## Wire codec\n\nProtocol-specific encoding details.\n"
    _, sections, errors = split_sections(text)
    assert not errors
    assert [title for title, _ in sections] == ["Usage", "Wire codec"]


def test_missing_readme_is_reported(package_fixture):
    root, readme = package_fixture
    readme.unlink()
    assert any("missing README" in failure for failure in verify(root)["failures"])
