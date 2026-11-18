"""Shared package inventory and Markdown structure for README repair and CI."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
import tomllib

REQUIRED_SECTIONS = (
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
)
COMPATIBILITY = ("tba-testkit-identity", "tba-testkit-workload-credential-conformance")


@dataclass
class Package:
    root: Path
    folder: Path
    document: dict
    python: bool

    @property
    def project(self) -> dict:
        return self.document["project"] if self.python else self.document

    @property
    def name(self) -> str:
        return self.project["name"]

    @property
    def relative(self) -> str:
        return self.folder.relative_to(self.root).as_posix()

    @property
    def layer(self) -> str:
        return self.folder.parent.name

    @property
    def publishable(self) -> bool:
        return self.python and self.document.get("tool", {}).get("uv", {}).get(
            "package", True
        )


def packages(root: Path) -> list[Package]:
    folders = {
        p.parent
        for pattern in ("pkgs/[0-9]*/*/pyproject.toml", "pkgs/[0-9]*/*/package.json")
        for p in root.glob(pattern)
    }
    folders.update(
        root / "pkgs/deprecated" / name
        for name in COMPATIBILITY
        if (root / "pkgs/deprecated" / name / "pyproject.toml").is_file()
    )
    result = []
    for folder in sorted(folders):
        python = (folder / "pyproject.toml").is_file()
        path = folder / ("pyproject.toml" if python else "package.json")
        document = (
            tomllib.loads(path.read_text(encoding="utf-8"))
            if python
            else json.loads(path.read_text(encoding="utf-8"))
        )
        result.append(Package(root, folder, document, python))
    return result


def key(title: str) -> str:
    value = re.sub(r"\s+", " ", title.strip().strip("#").strip()).casefold()
    return {
        "facade boundary": "package boundary",
        "project links": "project links",
    }.get(value, value)


def split_sections(text: str) -> tuple[str, list[tuple[str, str]], list[str]]:
    """Split actual H2 sections; fenced examples cannot impersonate headings."""
    lines = text.splitlines(keepends=True)
    starts = []
    fence = None
    errors = []
    for index, line in enumerate(lines):
        opening = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line.rstrip())
        if fence:
            if (
                opening
                and opening[1][0] == fence[0]
                and len(opening[1]) >= fence[1]
                and not opening[2].strip()
            ):
                fence = None
            continue
        if opening:
            fence = (opening[1][0], len(opening[1]))
            continue
        heading = re.match(r"^ {0,3}##[ \t]+(.+?)[ \t]*#*[ \t]*$", line.rstrip())
        if heading:
            starts.append((index, heading[1]))
    if fence:
        errors.append("unclosed Markdown code fence")
    preamble = "".join(lines[: starts[0][0]]) if starts else text
    sections = []
    for number, (index, title) in enumerate(starts):
        end = starts[number + 1][0] if number + 1 < len(starts) else len(lines)
        sections.append((title, "".join(lines[index + 1 : end]).strip()))
    return preamble.rstrip(), sections, errors


def section_errors(text: str) -> list[str]:
    _, sections, errors = split_sections(text)
    by_key: dict[str, list[str]] = {}
    for title, body in sections:
        by_key.setdefault(key(title), []).append(body)
    for title in REQUIRED_SECTIONS:
        bodies = by_key.get(key(title), [])
        if len(bodies) != 1:
            errors.append(
                f"{title}: expected exactly one H2 section, found {len(bodies)}"
            )
            continue
        body = re.sub(r"<!--[\s\S]*?-->", "", bodies[0]).strip()
        visible = re.sub(r"[`#>*_\s-]", "", body)
        if len(visible) < 24 or re.fullmatch(
            r"(?is)(?:todo|tbd|n/?a|coming soon|placeholder)[.!\s]*", body
        ):
            errors.append(
                f"{title}: needs substantive content, not an empty heading or placeholder"
            )
        if re.search(r"(?im)^\s*(?:TODO|TBD|Lorem ipsum)(?:\b|:)", body):
            errors.append(f"{title}: unresolved documentation placeholder")
    for title in ("Installation", "Usage", "Quick start"):
        bodies = by_key.get(key(title), [])
        if len(bodies) == 1 and not re.search(
            r"(?m)^ {0,3}(?:`{3,}|~{3,})[\w+-]+", bodies[0]
        ):
            errors.append(f"{title}: needs a labelled command or code example")
    return errors
