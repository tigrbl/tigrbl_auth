"""Apply the repository's package metadata and Apache attribution standard.

Run with: uv run --no-project --with tomlkit python scripts/normalize_package_metadata.py
"""

from __future__ import annotations

import json
from pathlib import Path

import tomlkit

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = "https://github.com/tigrbl/tigrbl_auth"
NOTICE = """Tigrbl Auth (TBA)

Project: https://github.com/tigrbl/tigrbl_auth
Attribution: Jacob Stewart and the Tigrbl Auth contributors.

Distributed under the Apache License, Version 2.0.
See the accompanying LICENSE file for the license terms.
"""


def normalize_python(path: Path, authors: list[dict[str, str]]) -> None:
    document = tomlkit.parse(path.read_text(encoding="utf-8"))
    project = document["project"]
    project["license"] = "Apache-2.0"
    project["license-files"] = ["LICENSE", "NOTICE"]
    project["readme"] = "README.md"
    if not project.get("authors"):
        project["authors"] = authors
    if not project.get("keywords"):
        project["keywords"] = ["tigrbl", "tba", "identity"]
    classifiers = [
        value
        for value in project.get("classifiers", [])
        if not value.startswith("License ::")
    ]
    required = [
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ]
    required.extend(
        f"Programming Language :: Python :: 3.{minor}" for minor in range(10, 16)
    )
    if not any(value.startswith("Development Status ::") for value in classifiers):
        required.append("Development Status :: 3 - Alpha")
    if any(path.parent.glob("src/*/py.typed")):
        required.append("Typing :: Typed")
    for classifier in required:
        if classifier not in classifiers:
            classifiers.append(classifier)
    project["classifiers"] = tomlkit.array().multiline(True)
    project["classifiers"].extend(classifiers)
    urls = project.setdefault("urls", tomlkit.table())
    relative = path.parent.relative_to(ROOT).as_posix()
    source = REPOSITORY if relative == "." else f"{REPOSITORY}/tree/master/{relative}"
    urls.update(
        {
            "Homepage": f"{source}#readme",
            "Documentation": f"{source}#readme",
            "Repository": REPOSITORY,
            "Source": source,
            "Issues": f"{REPOSITORY}/issues",
        }
    )
    publishable = document.get("tool", {}).get("uv", {}).get("package", True)
    if relative != "." and publishable:
        urls["PyPI"] = f"https://pypi.org/project/{project['name']}/"
    elif not publishable:
        urls.pop("PyPI", None)
    backend = document.get("build-system", {}).get("build-backend")
    if backend == "poetry.core.masonry.api":
        document["build-system"]["requires"] = ["poetry-core>=2.2.0,<3.0.0"]
    elif backend == "setuptools.build_meta":
        document["build-system"]["requires"] = ["setuptools>=77.0.3"]
    path.write_text(tomlkit.dumps(document), encoding="utf-8")


def main() -> None:
    root_manifest = tomlkit.parse((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    authors = root_manifest["project"]["authors"].unwrap()
    license_text = (ROOT / "LICENSE").read_bytes()
    if not (ROOT / "NOTICE").exists():
        (ROOT / "NOTICE").write_text(NOTICE, encoding="utf-8")
    notice_text = (ROOT / "NOTICE").read_text(encoding="utf-8")
    normalize_python(ROOT / "pyproject.toml", authors)
    package_roots = set()
    manifests = sorted((ROOT / "pkgs").glob("[0-9]*/*/pyproject.toml"))
    for manifest in manifests:
        normalize_python(manifest, authors)
        package_roots.add(manifest.parent)
    for manifest in sorted((ROOT / "pkgs").glob("[0-9]*/*/package.json")):
        data = json.loads(manifest.read_text(encoding="utf-8"))
        relative = manifest.parent.relative_to(ROOT).as_posix()
        data["license"] = "Apache-2.0"
        data.setdefault("author", authors[0])
        data["repository"] = {
            "type": "git",
            "url": f"git+{REPOSITORY}.git",
            "directory": relative,
        }
        data["homepage"] = f"{REPOSITORY}/tree/master/{relative}#readme"
        data["bugs"] = {"url": f"{REPOSITORY}/issues"}
        if "files" in data:
            for filename in ("LICENSE", "NOTICE", "README.md"):
                if filename not in data["files"]:
                    data["files"].append(filename)
        manifest.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        lock_path = manifest.parent / "package-lock.json"
        if lock_path.is_file():
            lock = json.loads(lock_path.read_text(encoding="utf-8"))
            if "" in lock.get("packages", {}):
                lock["packages"][""]["license"] = "Apache-2.0"
                lock_path.write_text(
                    json.dumps(lock, indent=2) + "\n", encoding="utf-8"
                )
        package_roots.add(manifest.parent)
    for folder in sorted(package_roots):
        manifest = folder / "pyproject.toml"
        name = (
            tomlkit.parse(manifest.read_text())["project"]["name"]
            if manifest.exists()
            else json.loads((folder / "package.json").read_text())["name"]
        )
        (folder / "LICENSE").write_bytes(license_text)
        notice = folder / "NOTICE"
        if not notice.exists():
            notice.write_text(
                notice_text
                + f"\nDistribution: {name}\nSource: {REPOSITORY}/tree/master/{folder.relative_to(ROOT).as_posix()}\n",
                encoding="utf-8",
            )
        else:
            lines = notice.read_text(encoding="utf-8").splitlines()
            lines = [
                f"Distribution: {name}"
                if line.startswith("Distribution: ")
                else f"Source: {REPOSITORY}/tree/master/{folder.relative_to(ROOT).as_posix()}"
                if line.startswith("Source: ")
                else line
                for line in lines
            ]
            notice.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        f"Normalized metadata and legal files for {len(package_roots)} active packages"
    )


if __name__ == "__main__":
    main()
