"""Fail CI on incomplete package READMEs, stale branding, or mismatched badges."""

from __future__ import annotations

import argparse
import ast
from collections import Counter
import json
from pathlib import Path
import re

from readme_policy import REQUIRED_SECTIONS, packages, section_errors, split_sections
from render_readme_branding import END, START, header

ROOT = Path(__file__).resolve().parents[1]


def fragment(text: str) -> str:
    if (
        text.count(START) != 1
        or text.count(END) != 1
        or text.index(START) > text.index(END)
    ):
        raise ValueError("needs exactly one ordered managed branding fragment")
    return text.split(START, 1)[1].split(END, 1)[0].strip()


def verify(root: Path = ROOT) -> dict:
    failures, records = [], []
    section_counts: Counter = Counter()
    for package in packages(root):
        readme = package.folder / "README.md"
        if not readme.is_file():
            failures.append(f"{package.relative}: missing README.md")
            continue
        text = readme.read_text(encoding="utf-8")
        errors = section_errors(text)
        try:
            if fragment(text) != fragment(header(readme, text, root_path=root)):
                errors.append(
                    "branding fragment or badges differ from package metadata; run scripts/render_readme_branding.py"
                )
        except ValueError as error:
            errors.append(str(error))
        preamble, sections, _ = split_sections(text)
        # A package needs its own title and explanatory prose, not just badges.
        title = re.search(r"(?m)^#\s+(.+)$", preamble)
        if not title or package.name not in title[1]:
            errors.append("H1 title must identify this package")
        prose = re.sub(r"<!--[\s\S]*?-->", "", preamble)
        prose = re.sub(r"(?m)^#.*$", "", prose).strip()
        if len(prose) < 32:
            errors.append(
                "needs a package-specific introduction outside the branding fragment"
            )
        # Parse labelled Python examples without importing packages or executing
        # network calls, signing operations, or deployments during documentation CI.
        for title, body in sections:
            for example in re.finditer(r"(?ms)^```python\s*\n(.*?)^```\s*$", body):
                try:
                    ast.parse(example[1])
                except SyntaxError as error:
                    errors.append(f"{title}: invalid Python example: {error.msg}")
        section_counts.update(title for title, _ in sections)
        records.append(
            dict(
                name=package.name,
                path=package.relative,
                sections=[t for t, _ in sections],
                passed=not errors,
            )
        )
        failures.extend(f"{package.relative}: {error}" for error in errors)
    return dict(
        passed=not failures,
        package_count=len(records),
        required_sections=list(REQUIRED_SECTIONS),
        section_counts=dict(sorted(section_counts.items())),
        failures=failures,
        packages=records,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    report = verify()
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(
            json.dumps(report, sort_keys=True, separators=(",", ":")), encoding="utf-8"
        )
    print(json.dumps({k: v for k, v in report.items() if k != "packages"}, indent=2))
    return int(not report["passed"])


if __name__ == "__main__":
    raise SystemExit(main())
