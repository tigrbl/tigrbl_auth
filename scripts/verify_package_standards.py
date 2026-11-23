"""Check package ownership, legal files, and package-specific README fragments."""

from __future__ import annotations

import argparse
from collections import Counter
from html.parser import HTMLParser
import json
from pathlib import Path
import tomllib
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
START = "<!-- BEGIN TBA README HEADER -->"
END = "<!-- END TBA README HEADER -->"
REPOSITORY = "https://github.com/tigrbl/tigrbl_auth"


class Fragment(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.images: list[dict[str, str]] = []
        self.links: list[str] = []
        self.stack: list[str] = []
        self.errors: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag not in {"p", "a", "img", "strong"}:
            self.errors.append(f"unsupported branding tag {tag}")
        if tag == "img":
            if not values.get("src") or not values.get("alt"):
                self.errors.append("brand image needs src and alt")
            self.images.append(values)
        else:
            self.stack.append(tag)
        if tag == "a":
            self.links.append(values.get("href", ""))

    def handle_endtag(self, tag: str) -> None:
        if tag == "img":
            return
        if not self.stack or self.stack.pop() != tag:
            self.errors.append(f"unbalanced branding tag {tag}")


def verify(root: Path = ROOT) -> dict:
    failures: list[str] = []
    counters: list[str] = []
    totals: Counter = Counter()
    license_text = (root / "LICENSE").read_bytes()
    if not (root / "NOTICE").is_file():
        failures.append("root NOTICE is missing")
    brand = root / "docs/assets/tba-brand.png"
    if not brand.is_file() or not brand.read_bytes().startswith(b"\x89PNG\r\n\x1a\n"):
        failures.append("shared brand asset is not a PNG")
    manifests = sorted(
        {
            *root.glob("pkgs/[0-9]*/*/pyproject.toml"),
            *root.glob("pkgs/[0-9]*/*/package.json"),
        }
    )
    manifests.extend(
        root / "pkgs/deprecated" / name / "pyproject.toml"
        for name in (
            "tba-testkit-identity",
            "tba-testkit-workload-credential-conformance",
        )
        if (root / "pkgs/deprecated" / name / "pyproject.toml").is_file()
    )
    for path in manifests:
        folder = path.parent
        relative = folder.relative_to(root).as_posix()
        python = path.suffix == ".toml"
        document = (
            tomllib.loads(path.read_text(encoding="utf-8"))
            if python
            else json.loads(path.read_text())
        )
        project = document["project"] if python else document
        name = project["name"]
        publishable = python and document.get("tool", {}).get("uv", {}).get(
            "package", True
        )
        totals["python" if python else "node"] += 1
        totals["publishable_python"] += bool(publishable)
        errors: list[str] = []
        for filename in ("README.md", "LICENSE", "NOTICE"):
            if not (folder / filename).is_file():
                errors.append(f"missing {filename}")
        if (folder / "LICENSE").is_file() and (
            folder / "LICENSE"
        ).read_bytes() != license_text:
            errors.append("LICENSE differs from the repository Apache license")
        if (folder / "NOTICE").is_file() and f"Distribution: {name}\n" not in (
            folder / "NOTICE"
        ).read_text():
            errors.append("NOTICE attribution does not identify this distribution")
        if project.get("license") != "Apache-2.0":
            errors.append("license must use SPDX Apache-2.0")
        if python:
            if project.get("license-files") != ["LICENSE", "NOTICE"]:
                errors.append("license-files must declare LICENSE and NOTICE")
            if not project.get("authors"):
                errors.append("missing author metadata")
            if not project.get("description") or project.get("readme") != "README.md":
                errors.append("missing description or README metadata")
            urls = project.get("urls", {})
            if urls.get("Source") != f"{REPOSITORY}/tree/master/{relative}":
                errors.append("Source URL does not identify this package")
            if publishable and urls.get("PyPI") != f"https://pypi.org/project/{name}/":
                errors.append("PyPI URL does not identify this package")
            if any(c.startswith("License ::") for c in project.get("classifiers", [])):
                errors.append("deprecated license classifier remains")
        if python and document.get("tool", {}).get("readme_standards"):
            from readme_standards.check import check_package
            from readme_standards.render import region_spans

            errors.extend(str(issue) for issue in check_package(folder))
            if (folder / "README.md").is_file():
                text = (folder / "README.md").read_text(encoding="utf-8")
                for region, start, end in region_spans(text):
                    if region == "branding":
                        fragment = Fragment()
                        fragment.feed(text[start:end])
                        errors.extend(fragment.errors)
                        if fragment.stack:
                            errors.append("branding fragment has unclosed tags")
                        counters.extend(image["src"] for image in fragment.images
                                        if image.get("alt", "").startswith("README hits:"))
            failures.extend(f"{relative}: {error}" for error in errors)
            continue
        if (folder / "README.md").is_file():
            text = (folder / "README.md").read_text(encoding="utf-8")
            if text.count(START) != 1 or text.count(END) != 1:
                errors.append("README needs exactly one managed branding fragment")
            else:
                fragment = Fragment()
                fragment.feed(text.split(START, 1)[1].split(END, 1)[0])
                errors.extend(fragment.errors)
                if fragment.stack:
                    errors.append("branding fragment has unclosed tags")
                brands = [
                    i for i in fragment.images if i.get("alt") == "TBA · Tigrbl Auth"
                ]
                if (
                    len(brands) != 1
                    or brands[0].get("src")
                    != "https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png"
                ):
                    errors.append("README needs the valid shared TBA brand fragment")
                hits = [
                    i
                    for i in fragment.images
                    if i.get("alt", "").startswith("README hits for ")
                ]
                expected = f"/github.com/tigrbl/tigrbl_auth/blob/master/{relative}/README.md.svg"
                if (
                    len(hits) != 1
                    or unquote(urlsplit(hits[0].get("src", "")).path) != expected
                ):
                    errors.append(
                        "README hit counter must identify this package's README"
                    )
                else:
                    counters.append(hits[0]["src"])
                downloads = [
                    i
                    for i in fragment.images
                    if i.get("alt", "").startswith("Monthly PyPI downloads for ")
                ]
                if publishable:
                    if (
                        len(downloads) != 1
                        or downloads[0].get("src")
                        != f"https://static.pepy.tech/badge/{name}/month"
                    ):
                        errors.append(
                            "monthly download counter must identify this PyPI project"
                        )
                elif not any(
                    i.get("alt") == "Downloads: source checkout"
                    for i in fragment.images
                ):
                    errors.append(
                        "source-only package needs its own source download link"
                    )
            if not {"## Quick start", "## Verification"} <= set(text.splitlines()):
                errors.append("README needs quick start and verification sections")
        failures.extend(f"{relative}: {error}" for error in errors)
    if len(counters) != len(set(counters)):
        failures.append("multiple packages share a README hit counter")
    return {"passed": not failures, "counts": dict(totals), "failures": failures}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    report = verify()
    output = json.dumps(report, indent=2) + "\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output, encoding="utf-8")
    print(output, end="")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
