"""Refresh or check the shared header in the root and active TBA package READMEs."""

from __future__ import annotations

import argparse
import json
import tomllib
from html import escape
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
REPO = "https://github.com/tigrbl/tigrbl_auth"
BLOB = f"{REPO}/blob/master"
BRAND = "docs/assets/tba-brand.png"
RAW = "https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master"
START = "<!-- BEGIN TBA README HEADER -->"
END = "<!-- END TBA README HEADER -->"


def image_link(alt: str, image: str, target: str) -> str:
    return (
        f'<a href="{escape(target)}">'
        f'<img alt="{escape(alt)}" src="{escape(image)}"></a>'
    )


def badge(label: str, value: str, color: str, target: str) -> str:
    def segment(text: str) -> str:
        return quote(text.replace("-", "--").replace("_", "__"), safe="")

    url = f"https://img.shields.io/badge/{segment(label)}-{segment(value)}-{color}"
    return image_link(f"{label}: {value}", url, target)


def header(readme: Path, original: str, root_path: Path | None = None) -> str:
    repository_root = root_path or ROOT
    folder = readme.parent
    root = folder == repository_root
    python = (folder / "pyproject.toml").is_file()
    manifest = "pyproject.toml" if python else "package.json"
    path = folder / manifest
    manifest_url = f"{BLOB}/{path.relative_to(repository_root).as_posix()}"
    publishable = False
    if python:
        document = tomllib.loads(path.read_text(encoding="utf-8"))
        if document.get("tool", {}).get("readme_standards"):
            from readme_standards.config import load_package
            from readme_standards.render import render

            return render(original, load_package(folder))
        meta = document["project"]
        publishable = document.get("tool", {}).get("uv", {}).get("package", True)
        requirement = meta.get("requires-python")
    else:
        meta = json.loads(path.read_text(encoding="utf-8"))
        requirement = meta.get("engines", {}).get("node", "not declared")

    metadata = [
        badge(
            "Workspace" if root else "Checkout", meta["version"], "1f6feb", manifest_url
        )
    ]
    if requirement:
        metadata.append(
            badge("Python" if python else "Node", requirement, "3776ab", manifest_url)
        )
    license_id = meta.get("license")
    legal_base = ""
    if python and publishable and not root:
        release_tag = quote(f"{meta['name']}=={meta['version']}", safe="")
        legal_base = f"{REPO}/blob/{release_tag}/{folder.relative_to(repository_root).as_posix()}/"
    if isinstance(license_id, str):
        metadata.append(badge("License", license_id, "525252", f"{legal_base}LICENSE"))
        metadata.append(badge("Notice", "attribution", "525252", f"{legal_base}NOTICE"))
    if not root:
        layer_name = folder.parent.name
        layer = layer_name.replace("-", " ")
        metadata.append(
            badge("Layer", layer, "0a7f5a", f"{REPO}/tree/master/pkgs/{layer_name}")
        )
    if meta.get("private"):
        metadata.append(badge("Distribution", "private source", "6e7781", manifest_url))

    metrics = []
    if python and (root or publishable):
        package = "tba-auth" if root else meta["name"]
        registry = f"https://pypi.org/project/{package}/"
        metadata.append(
            image_link(
                f"PyPI version for {package}",
                f"https://img.shields.io/pypi/v/{package}?label={package}%20PyPI",
                registry,
            )
        )
        metrics.append(
            image_link(
                f"Monthly PyPI downloads for {package}",
                f"https://static.pepy.tech/badge/{package}/month",
                f"https://pepy.tech/project/{package}",
            )
        )
    else:
        source_url = (
            f"{REPO}/tree/master/{folder.relative_to(repository_root).as_posix()}"
        )
        metrics.append(badge("Downloads", "source checkout", "0969da", source_url))
    if not python:
        metrics.append(
            badge(
                "Direct dependencies",
                str(len(meta.get("dependencies", {}))),
                "0969da",
                manifest_url,
            )
        )

    readme_path = readme.relative_to(repository_root).as_posix()
    counter_key = f"github.com/tigrbl/tigrbl_auth/blob/master/{readme_path}"
    counter_url = f"https://hits.sh/{quote(counter_key, safe='/')}.svg?label=hits"
    metrics.append(
        image_link(
            f"README hits for {meta['name']}", counter_url, f"{BLOB}/{readme_path}"
        )
    )

    if root:
        workflow = f"{REPO}/actions/workflows/master.yml"
        evidence = [
            image_link(
                "Workspace CI on master",
                f"{workflow}/badge.svg?branch=master",
                workflow,
            ),
            badge("SSOT", "registry", "2f6f4e", f"{BLOB}/.ssot/registry.json"),
            badge(
                "Certification",
                "status report",
                "8250df",
                f"{BLOB}/CERTIFICATION_STATUS.md",
            ),
        ]
    else:
        readme_url = f"{BLOB}/{readme.relative_to(repository_root).as_posix()}"
        evidence_status = "verification"
        if "<!-- TBA QUICK START: browser-verified -->" in original:
            evidence_status = "browser verified"
        elif "<!-- TBA QUICK START: backend-only -->" in original:
            evidence_status = "backend only"
        elif "<!-- TBA QUICK START: blocked -->" in original:
            evidence_status = "quick start blocked"
        evidence = [
            badge("SSOT", "governed", "2f6f4e", f"{BLOB}/.ssot/registry.json"),
            badge("Evidence", evidence_status, "8250df", f"{readme_url}#verification"),
        ]

    brand_url = BRAND if root else f"{RAW}/{BRAND}"
    width = 360 if root else 240
    return "\n".join(
        [
            START,
            '<p align="center">',
            f'<a href="{REPO}#readme"><img src="{brand_url}" alt="TBA · Tigrbl Auth" width="{width}"></a>',
            "</p>",
            '<p align="center">',
            *metadata,
            "</p>",
            '<p align="center">',
            *metrics,
            *evidence,
            "</p>",
            END,
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true", help="Report stale headers without writing."
    )
    args = parser.parse_args()
    if not (ROOT / BRAND).is_file():
        parser.error(f"shared brand asset is missing: {BRAND}")

    packages = ROOT / "pkgs"
    package_readmes = {
        path.with_name("README.md")
        for manifest in ("pyproject.toml", "package.json")
        for path in packages.glob(f"[0-9]*/*/{manifest}")
    }
    package_readmes.update(
        ROOT / "pkgs/deprecated" / name / "README.md"
        for name in (
            "tba-testkit-identity",
            "tba-testkit-workload-credential-conformance",
        )
        if (ROOT / "pkgs/deprecated" / name / "pyproject.toml").is_file()
    )
    stale = []
    readmes = [ROOT / "README.md", *sorted(package_readmes)]
    for readme in readmes:
        if not readme.is_file():
            parser.error(f"README is missing: {readme.relative_to(ROOT)}")
        original = readme.read_text(encoding="utf-8")
        manifest = readme.parent / "pyproject.toml"
        if manifest.is_file() and tomllib.loads(manifest.read_text("utf-8")).get(
            "tool", {}
        ).get("readme_standards"):
            updated = header(readme, original)
            if updated != original:
                stale.append(readme.relative_to(ROOT))
                if not args.check:
                    readme.write_text(updated, encoding="utf-8")
            continue
        before, start, after = original.partition(START)
        _, end, rest = after.partition(END)
        if not (start and end) or START in after or END in rest or END in before:
            parser.error(f"missing or malformed header: {readme.relative_to(ROOT)}")
        if readme in package_readmes:
            headings = set(rest.splitlines())
            if not {"## Quick start", "## Verification"} <= headings:
                parser.error(
                    f"quick start or verification is missing: {readme.relative_to(ROOT)}"
                )
        updated = before + header(readme, original) + rest
        if updated != original:
            stale.append(readme.relative_to(ROOT))
            if not args.check:
                readme.write_text(updated, encoding="utf-8")
    if args.check and stale:
        print("Stale README headers. Run python scripts/render_readme_branding.py.")
        print(*stale, sep="\n")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
