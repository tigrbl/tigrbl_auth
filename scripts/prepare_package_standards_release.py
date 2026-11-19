"""Prepare immutable metadata-only versions and matching internal pins."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

from packaging.requirements import InvalidRequirement, Requirement
from packaging.utils import canonicalize_name
from packaging.version import Version
import rfc8785
import tomlkit

from bump_pyproject_version import bump_version

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--published-versions", required=True, type=Path)
    parser.add_argument("--plan", required=True, type=Path)
    args = parser.parse_args()
    if args.plan.exists():
        raise SystemExit(
            "Release plan already exists; resume it instead of bumping again"
        )
    published = {r["name"]: r for r in json.loads(args.published_versions.read_text())}
    manifests = sorted((ROOT / "pkgs").glob("[0-9]*/*/pyproject.toml"))
    documents = {p: tomlkit.parse(p.read_text(encoding="utf-8")) for p in manifests}
    rows = []
    for path, data in documents.items():
        if data.get("tool", {}).get("uv", {}).get("package", True) is False:
            continue
        project = data["project"]
        name, current = str(project["name"]), str(project["version"])
        latest = published[name]["latest"]
        baseline = max(Version(current), Version(latest))
        target = bump_version(str(baseline), "patch")
        roots = sorted(
            p.name
            for p in (path.parent / "src").iterdir()
            if p.is_dir()
            and not p.name.endswith(".egg-info")
            and p.name != "__pycache__"
        )
        rows.append(
            dict(
                name=name,
                source_version=current,
                published_version=latest,
                version=target,
                path=path.parent.relative_to(ROOT).as_posix(),
                import_root=roots[0],
                compatibility_alias=False,
            )
        )
        project["version"] = target
    targets = {canonicalize_name(r["name"]): r["version"] for r in rows}

    def pin(value):
        if not isinstance(value, str):
            return value
        try:
            requirement = Requirement(value)
        except InvalidRequirement:
            return value
        version = targets.get(canonicalize_name(requirement.name))
        if not version or requirement.url or not requirement.specifier:
            return value
        exact = any(s.operator in {"==", "==="} for s in requirement.specifier)
        if not exact and requirement.specifier.contains(version, prereleases=True):
            return value
        extras = (
            "[" + ",".join(sorted(requirement.extras)) + "]"
            if requirement.extras
            else ""
        )
        marker = f"; {requirement.marker}" if requirement.marker else ""
        return f"{requirement.name}{extras}=={version}{marker}"

    root_path = ROOT / "pyproject.toml"
    documents[root_path] = tomlkit.parse(root_path.read_text(encoding="utf-8"))
    for path, data in documents.items():
        project = data["project"]
        if "dependencies" in project:
            project["dependencies"] = [pin(v) for v in project["dependencies"]]
        for extra, values in project.get("optional-dependencies", {}).items():
            project["optional-dependencies"][extra] = [pin(v) for v in values]
        for group, values in data.get("dependency-groups", {}).items():
            data["dependency-groups"][group] = [pin(v) for v in values]
        path.write_text(tomlkit.dumps(data), encoding="utf-8")
    for readme in [
        ROOT / "README.md",
        *ROOT.glob("pkgs/[0-9]*/*/README.md"),
    ]:
        if not readme.is_file():
            continue
        text = readme.read_text(encoding="utf-8")
        for row in rows:
            expression = re.compile(
                re.escape(row["name"])
                + r"(?P<extras>\[[^\]\n]+\])?==[0-9]+\.[0-9]+\.[0-9]+(?:\.dev[0-9]+)?"
            )
            text = expression.sub(
                lambda m, r=row: r["name"] + (m["extras"] or "") + "==" + r["version"],
                text,
            )
        readme.write_text(text, encoding="utf-8")
    plan = dict(
        status="candidate",
        scope="Python metadata and legal/README updates",
        packages=rows,
        source_only_node_packages=48,
        workspace_only_python_harnesses=4,
        published_test_package_migration="c12980ae00260c356ced82f57fa92238a2b9f02a",
        policy="Increment each package above its latest published version; preserve existing deprecations; update internal exact pins together.",
    )
    args.plan.parent.mkdir(parents=True, exist_ok=True)
    args.plan.write_bytes(rfc8785.dumps(plan))
    print(f"Prepared {len(rows)} immutable Python updates")


if __name__ == "__main__":
    main()
