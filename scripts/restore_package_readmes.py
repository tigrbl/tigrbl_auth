"""Restore the extensive README outline while preserving package-specific guidance.

Historical narrative is recovered from before the branding rewrite. New
sections use checked-in manifests, public source, reverse dependencies and the
capability registry. This tool fills gaps; it does not overwrite authored usage.
"""

from __future__ import annotations

import argparse
import ast
from collections import defaultdict
import json
from pathlib import Path
import re
import subprocess

from readme_policy import Package, REQUIRED_SECTIONS, key, packages, split_sections

ROOT = Path(__file__).resolve().parents[1]
HISTORY = "733c127473bf0df07ed93606a5810aa70ac5f9f2^"
REPO = "https://github.com/tigrbl/tigrbl_auth"
BLOB = REPO + "/blob/master/"
LAYER_SCOPE = {
    "00-primitives": (
        "shared identity primitives",
        "protocol flows, provider selection, or application hosting",
    ),
    "01-storage": (
        "storage schema and table declarations",
        "protocol endpoints or deployment-specific provider selection",
    ),
    "02-contracts": (
        "shared types and structural ports",
        "environment-specific service implementations or HTTP routing",
    ),
    "03-codecs": (
        "representation encoding and decoding",
        "issuer trust policy, key lifecycle, or HTTP endpoints",
    ),
    "05-bases": (
        "reusable component bases",
        "deployment composition or implicit provider selection",
    ),
    "10-concrete": (
        "focused concrete types and algorithms",
        "application hosting or ownership of environment-specific providers",
    ),
    "20-providers": (
        "replaceable environment implementations",
        "capability orchestration, storage table ownership, or HTTP routing",
    ),
    "30-storage-runtime": (
        "storage-backed runtime adapters",
        "protocol wire definitions or standalone application hosting",
    ),
    "40-capabilities": (
        "use-case orchestration through explicit collaborators",
        "HTTP wire schemas, direct table ownership, or hidden provider selection",
    ),
    "50-protocols": (
        "protocol semantics and projections",
        "deployment hosting or ownership of persistence implementations",
    ),
    "55-profiles": (
        "focused protocol and credential profiles",
        "a universal deployment or implicit trust-policy selection",
    ),
    "60-runtime": (
        "runtime composition and operator entry points",
        "duplicating protocol grammars, table declarations, or provider implementations",
    ),
    "70-facade": (
        "curated public entry points",
        "moving implementation ownership out of focused packages",
    ),
    "75-clients": (
        "relying-party and client integration",
        "authority-side policy decisions or server-owned persistence",
    ),
    "80-routers": (
        "transport-facing route composition",
        "duplicating credential algorithms or storage ownership",
    ),
    "85-middleware": (
        "request middleware integration",
        "implicit key storage or a complete identity deployment",
    ),
    "90-backend-apps": (
        "deployable backend composition",
        "new protocol grammars or independent persistence implementations",
    ),
    "100-uix-core": (
        "shared browser UI foundations",
        "backend authorization decisions or server-side secret storage",
    ),
    "104-authenticator-uis": (
        "authenticator-facing UI integration",
        "replacing server-side verification and authorization",
    ),
    "105-ui": (
        "browser-facing interface composition",
        "establishing backend authorization or durable secret storage",
    ),
    "106-ui": (
        "operator and user interface prototypes",
        "claiming production backend security from a browser demonstration",
    ),
    "110-examples": (
        "executable integration examples",
        "a production service guarantee or release certification",
    ),
    "120-tests": (
        "test fixtures and executable verification",
        "production identity services or deployable policy defaults",
    ),
    "deprecated": (
        "maintained compatibility imports",
        "new implementation ownership or silently reversing deprecation",
    ),
}


def source_facts(package: Package) -> dict:
    roots = sorted((package.folder / "src").glob("*/__init__.py"))
    entry = roots[0] if roots else None
    exports, operations, inputs = [], [], []
    if entry:
        tree = ast.parse(entry.read_text(encoding="utf-8"))
        for node in tree.body:
            if isinstance(node, (ast.Assign, ast.AnnAssign)):
                targets = (
                    node.targets if isinstance(node, ast.Assign) else [node.target]
                )
                if any(isinstance(t, ast.Name) and t.id == "__all__" for t in targets):
                    try:
                        exports = list(ast.literal_eval(node.value))
                    except (ValueError, TypeError):
                        pass
        if not exports:
            exports = [
                node.name
                for node in tree.body
                if isinstance(
                    node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)
                )
                and not node.name.startswith("_")
            ]
        for path in sorted(entry.parent.rglob("*.py")):
            try:
                module = ast.parse(path.read_text(encoding="utf-8"))
            except SyntaxError:
                continue
            for node in module.body:
                if isinstance(node, ast.ClassDef) and node.name in exports:
                    for method in node.body:
                        if isinstance(method, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            if method.name == "__init__":
                                names = [
                                    a.arg
                                    for a in [
                                        *method.args.posonlyargs,
                                        *method.args.args,
                                        *method.args.kwonlyargs,
                                    ]
                                    if a.arg not in {"self", "cls"}
                                ]
                                if names:
                                    inputs.append((node.name, names, path))
                            elif not method.name.startswith("_"):
                                operations.append((node.name + "." + method.name, path))
                elif (
                    isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                    and node.name in exports
                ):
                    operations.append((node.name, path))
                    names = [a.arg for a in node.args.kwonlyargs]
                    if names:
                        inputs.append((node.name, names, path))
    return dict(
        entry=entry,
        module=entry.parent.name if entry else None,
        exports=exports,
        operations=operations,
        inputs=inputs,
    )


def histories(inventory: list[Package]) -> dict[str, str]:
    queries = [f"{HISTORY}:{p.relative}/README.md" for p in inventory]
    process = subprocess.run(
        ["git", "cat-file", "--batch"],
        input=("\n".join(queries) + "\n").encode(),
        capture_output=True,
        check=True,
        cwd=ROOT,
    )
    data, position, result = process.stdout, 0, {}
    for package in inventory:
        end = data.index(b"\n", position)
        header = data[position:end].decode()
        position = end + 1
        if header.endswith(" missing"):
            continue
        size = int(header.rsplit(" ", 1)[1])
        result[package.name] = (
            data[position : position + size].decode("utf-8").replace("\r\n", "\n")
        )
        position += size + 1
    return result


def first_code(text: str, language: str) -> str | None:
    match = re.search(r"(?ms)^```" + language + r"\s*\n(.*?)^```\s*$", text)
    return match[1].strip() if match else None


def requirements(package: Package) -> set[str]:
    values = package.project.get("dependencies", [])
    if not package.python:
        return set(values)
    return {re.split(r"[\s\[<>=!~;]", value, maxsplit=1)[0] for value in values}


def link(package: Package) -> str:
    return f"[{package.name}]({BLOB}{package.relative}/README.md)"


def section_content(
    package: Package,
    facts: dict,
    existing: str,
    local: list[Package],
    consumers: list[Package],
    capability: dict | None,
) -> dict[str, str]:
    name, relative, layer = package.name, package.relative, package.layer
    scope, excluded = LAYER_SCOPE[layer]
    description = package.project.get("description")
    if not description:
        stripped = re.sub(r"<!--[\s\S]*?-->", "", existing)
        description = next(
            (
                line.strip()
                for line in stripped.splitlines()
                if line.strip() and not line.startswith(("#", "<", "[", "```"))
            ),
            f"The {name} interface package",
        )
    description = description.rstrip(".")
    module = facts["module"]
    entry = facts["entry"]
    entry_link = (
        f"[public entry point]({BLOB}{entry.relative_to(ROOT).as_posix()})"
        if entry
        else f"[package manifest]({BLOB}{relative}/{'pyproject.toml' if package.python else 'package.json'})"
    )
    public = ", ".join(f"`{v}`" for v in facts["exports"][:12])
    if package.publishable:
        installation = f"Install the selected PyPI release of `{name}`:\n\n```bash\nuv pip install {name}\n```\n\nTo work on the current checkout before a prepared release is published:\n\n```bash\nuv pip install ./{relative}\n```"
    elif package.python:
        installation = f"`{name}` is a workspace-only harness (`tool.uv.package = false`), so install the repository development environment rather than a nonexistent wheel:\n\n```bash\nuv sync --group dev\n```\n\nRun the package's verification commands from the repository root."
    else:
        installation = f"Install `{name}` from this checkout; registry publication is separate from this source-only workflow:\n\n```bash\nnpm --prefix {relative} install\n```\n\nUse the package's declared npm scripts from the repository root."
    if package.python:
        example = first_code(existing, "python")
        if not example and module:
            example = f"import {module}\n\nprint({module}.__name__)"
        if example:
            usage = f"The following public-entry-point example belongs to `{name}`. {description}. Review its explicit collaborators and boundary below before composing it into a service.\n\n```python\n{example}\n```"
        else:
            usage = f"Use `{name}` through its repository test harness rather than as a production runtime import:\n\n```bash\nuv run pytest {relative}\n```\n\nIts fixtures and checks support the integration workflow documented in Quick start."
    else:
        scripts = package.project.get("scripts", {})
        selected = next(
            (s for s in ("dev", "build", "start", "test") if s in scripts), None
        )
        command = (
            f"npm --prefix {relative} run {selected}"
            if selected
            else f"npm --prefix {relative} run"
        )
        usage = f"Use the checked-in `{name}` package through its declared npm scripts:\n\n```bash\n{command}\n```\n\n{description}. The manifest is the authority for available scripts and entry points."
    injected = []
    if capability:
        deps = capability["dependencies"]
        injected = [
            f"- `{value}`"
            for group in ("providers", "durability", "capabilities")
            for value in deps.get(group, [])
        ]
    if not injected:
        injected = [
            f"- `{owner}` construction inputs: "
            + ", ".join(f"`{n}`" for n in names)
            + f". [Definition]({BLOB}{path.relative_to(ROOT).as_posix()})."
            for owner, names, path in facts["inputs"][:8]
        ]
    if injected:
        injection = (
            "Explicit construction inputs and collaborators for `"
            + name
            + "`:\n\n"
            + "\n".join(injected)
            + "\n\nConfiguration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them."
        )
    else:
        injection = f"The {entry_link} for `{name}` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.\n\nManifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract."
    ops = [
        f"- `{operation}` — [source]({BLOB}{path.relative_to(ROOT).as_posix()})."
        for operation, path in facts["operations"][:12]
    ]
    operations = f"`{name}` exposes {scope}. " + (
        "Public operations found in its source:\n\n" + "\n".join(ops)
        if ops
        else f"Inspect the {entry_link} for the exported types and composition surface."
    )
    operations += "\n\nA successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion."
    protocols = [p for p in consumers if p.layer == "50-protocols"]
    if capability:
        protocols = sorted(
            {
                p.name: p
                for p in protocols
                + [
                    p
                    for p in consumers
                    if p.name in capability.get("protocol_packages", [])
                ]
            }.values(),
            key=lambda p: p.name,
        )
    protocol_body = (
        (
            f"The following layer-50 manifests directly depend on `{name}`:\n\n"
            + "\n".join("- " + link(p) for p in protocols)
        )
        if protocols
        else f"No active layer-50 manifest declares a direct runtime dependency on `{name}`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration."
    )
    other_consumers = [p for p in consumers if p not in protocols]
    if other_consumers:
        protocol_body += (
            "\n\nOther direct consumers include "
            + ", ".join(link(p) for p in other_consumers[:8])
            + "."
        )
    related = []
    if local:
        related.append(
            "Declared local runtime dependencies:\n\n"
            + "\n".join("- " + link(p) for p in local)
        )
    if consumers:
        related.append(
            "Direct downstream consumers:\n\n"
            + "\n".join("- " + link(p) for p in consumers[:12])
        )
        if len(consumers) > 12:
            related.append(
                f"{len(consumers)} packages directly declare this dependency; the [package index]({BLOB}index.toml) records the complete graph."
            )
    if not related:
        related.append(
            f"`{name}` declares no local runtime dependency and has no direct consumer in the active manifest graph. Browse the [{layer} layer]({REPO}/tree/master/pkgs/{layer}) for adjacent package responsibilities; adjacency does not imply a dependency."
        )
    boundary = f"`{name}` belongs to `{layer}` and owns {scope}: {description}.\n\nIts implementation surface is the {entry_link}."
    if public:
        boundary += f" Public exports include {public}."
    boundary += f"\n\nKeep {excluded} in their owning packages. The [package index]({BLOB}index.toml) records layer placement and local dependency edges."
    project_links = f"- [Package source]({REPO}/tree/master/{relative})\n- [Package manifest]({BLOB}{relative}/{'pyproject.toml' if package.python else 'package.json'})\n- [LICENSE]({BLOB}{relative}/LICENSE) and [NOTICE]({BLOB}{relative}/NOTICE)\n- [Report an issue]({REPO}/issues)\n- [Package index]({BLOB}index.toml)\n- [Canonical SSOT registry]({BLOB}.ssot/registry.json)"
    if package.publishable:
        project_links += f"\n- [PyPI project](https://pypi.org/project/{name}/)"
    governance = f"`{name}` follows the [canonical SSOT registry]({BLOB}.ssot/registry.json) and [package index]({BLOB}index.toml). Keep its `{layer}` ownership, public imports, declared dependencies, examples, and release metadata aligned.\n\nChanges must pass the [README standards gate]({BLOB}.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries."
    if layer == "deprecated":
        governance += "\n\nThis maintained alias retains its deprecation policy and compatibility imports; new implementation work belongs to its active replacement."
    summary = (
        f"- Package: `{name}`\n- Layer: `{layer}`\n- Responsibility: {description}.\n- Public surface: {entry_link}.\n- Distribution: "
        + (
            "Python package on PyPI."
            if package.publishable
            else "repository development harness."
            if package.python
            else "source checkout; npm publication is separate."
        )
    )
    return dict(
        zip(
            REQUIRED_SECTIONS,
            [
                summary,
                f"Choose `{name}` for this responsibility: {description}. Its `{layer}` placement keeps {scope} separate from {excluded}.",
                installation,
                installation,
                usage,
                boundary,
                injection,
                operations,
                protocol_body,
                f"`{name}` does not take ownership of {excluded}.\n\nIts exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.",
                "\n\n".join(related),
                project_links,
                governance,
                f"Run the README and package-standard checks from the repository root:\n\n```bash\nuv run --no-project python scripts/verify_readme_standards.py\nuv run --no-project python scripts/verify_package_standards.py\n```\n\nThese checks validate documentation structure, metadata, and branding for `{name}`. Behavioral and integration assertions require the package's own tests and their recorded evidence.",
            ],
            strict=True,
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    inventory = packages(ROOT)
    by_name = {p.name: p for p in inventory}
    known_names = set(by_name) | {
        p.parent.name for p in ROOT.glob("pkgs/deprecated/*/pyproject.toml")
    }
    reverse = defaultdict(list)
    for package in inventory:
        for dependency in requirements(package):
            if dependency in by_name:
                reverse[dependency].append(package)
    old = histories(inventory)
    capability_data = json.loads(
        (ROOT / "pkgs/40-capabilities/capability-families.json").read_text()
    )
    capabilities = {r["package"]: r for r in capability_data["capabilities"]}
    report = dict(history=HISTORY, packages=[])
    safe_history = {
        key(t)
        for t in (
            "AEO Summary",
            "When to use it",
            "Package Boundary",
            "Related Packages",
            "Governance",
            "Non-goals",
        )
    }
    for package in inventory:
        readme = package.folder / "README.md"
        original = readme.read_text(encoding="utf-8")
        preamble, current, errors = split_sections(original)
        if errors:
            raise ValueError(f"{readme}: {errors}")
        first_title = re.search(r"(?m)^# (.+)$", preamble)
        if first_title and package.name not in first_title[1]:
            preamble = (
                preamble[: first_title.start()]
                + f"# {first_title[1]} (`{package.name}`)"
                + preamble[first_title.end() :]
            )
        sections = {}
        extras = []
        for title, body in current:
            normalized = key(title)
            if normalized in sections:
                raise ValueError(f"Duplicate section in {readme}: {title}")
            sections[normalized] = body
            if normalized not in {key(t) for t in REQUIRED_SECTIONS}:
                extras.append((title, body))
        historical = dict(
            (key(t), b) for t, b in split_sections(old.get(package.name, ""))[1]
        )
        recovered = []
        for title, body in historical.items():
            mentioned = set(re.findall(r"\btba-[a-z0-9-]+", body))
            if (
                title in safe_history
                and title not in sections
                and mentioned <= known_names
                and not re.search(r"```|tba-identity-", body)
            ):
                sections[title] = body
                recovered.append(title)
        facts = (
            source_facts(package)
            if package.python
            else dict(module=None, entry=None, exports=[], operations=[], inputs=[])
        )
        generated = section_content(
            package,
            facts,
            original,
            [by_name[n] for n in sorted(requirements(package)) if n in by_name],
            sorted(reverse[package.name], key=lambda p: p.name),
            capabilities.get(package.name),
        )
        added = []
        for title in REQUIRED_SECTIONS:
            if key(title) not in sections:
                sections[key(title)] = generated[title]
                added.append(title)
        operations = sections[key("Operations and readiness")]
        if len(re.sub(r"[`#>*_\s-]", "", operations)) < 24 or not re.search(
            r"readiness|ready|smoke|before deployment", operations, re.IGNORECASE
        ):
            sections[key("Operations and readiness")] += (
                f"\n\nFor `{package.name}`, these operation names identify the callable surface, not a readiness guarantee. Validate its explicit collaborators and behavioral checks in Verification before deployment."
            )
        if (
            package.publishable
            and package.relative not in sections[key("Installation")]
        ):
            sections[key("Installation")] += (
                f"\n\nInstall the current `{package.name}` source checkout when working ahead of a PyPI release:\n\n```bash\nuv pip install ./{package.relative}\n```"
            )
        # Preserve authored examples and specialist sections; repair stale registry
        # execution claims introduced when old quickstarts were version-bumped.
        for title in ("Quick start", "Verification"):
            body = sections[key(title)]
            body = body.replace(
                "This command uses the published package in an isolated Python 3.12 environment.",
                "This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.",
            )
            body = body.replace(
                "The quick start was run with the pinned distribution from PyPI and its declared dependencies.",
                "A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI.",
            )
            sections[key(title)] = body
        for title in ("Governance", "Project Links"):
            if (
                "index.toml" not in sections[key(title)]
                or ".ssot/registry.json" not in sections[key(title)]
            ):
                sections[key(title)] += "\n\n" + generated[title]
        sections[key("Protocol consumers")] = sections[
            key("Protocol consumers")
        ].replace("\n\nOther direct consumers include .", "")
        for title in ("Installation", "Usage", "Quick start"):
            if not re.search(r"(?m)^```[\w+-]+", sections[key(title)]):
                sections[key(title)] += "\n\n" + generated[title]
        chunks = [preamble]
        for title in REQUIRED_SECTIONS:
            chunks.append(f"## {title}\n\n{sections[key(title)]}")
            if title == "Usage":
                chunks.extend(f"## {t}\n\n{b}" for t, b in extras)
        text = "\n\n".join(chunks).rstrip() + "\n"
        readme.write_text(text, encoding="utf-8")
        report["packages"].append(
            dict(
                name=package.name,
                path=package.relative,
                recovered_sections=recovered,
                added_sections=added,
                preserved_extra_sections=[t for t, _ in extras],
                changed=text != original,
            )
        )
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(
        json.dumps(report, sort_keys=True, separators=(",", ":")), encoding="utf-8"
    )
    print(
        f"Restored {len(inventory)} package READMEs; recovered historical sections for {sum(bool(p['recovered_sections']) for p in report['packages'])} packages"
    )


if __name__ == "__main__":
    main()
