import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FORBIDDEN_FRAGMENTS = ("".join(("pha", "se")), "".join(("st", "ep")))
FORBIDDEN_PATTERN = re.compile(
    rf"(?i)(?:{FORBIDDEN_FRAGMENTS[0]}|{FORBIDDEN_FRAGMENTS[1]})[_-]?\d+"
)
RETAINED_BOUNDARY_BUNDLES = (
    "asgi-application",
    "bootstrap-migration",
    "cli-operator-surface",
    "import-export-portability",
    "key-lifecycle-jwks",
    "release-bundle-signing",
    "runner-hypercorn",
    "runner-tigrcorn",
    "runner-uvicorn",
)
GENERATOR_OWNED_BUNDLE_FILES = (
    "README.md",
    "execution.log",
    "manifest.yaml",
    "mapping.yaml",
    "environment.yaml",
    "hashes.yaml",
    "signatures.yaml",
)


def test_ssot_test_rows_use_capability_scoped_names() -> None:
    registry = json.loads((ROOT / ".ssot" / "registry.json").read_text())

    offenders = []
    for row in registry["tests"]:
        for field in ("id", "title", "path"):
            value = str(row.get(field, ""))
            if FORBIDDEN_PATTERN.search(value):
                offenders.append(f"{row['id']}:{field}={value}")

    assert offenders == []


def test_active_test_sources_use_capability_scoped_names() -> None:
    offenders = []
    for path in (ROOT / "tests").rglob("*.py"):
        if "__pycache__" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if FORBIDDEN_PATTERN.search(path.as_posix()) or FORBIDDEN_PATTERN.search(text):
            offenders.append(path.relative_to(ROOT).as_posix())

    assert offenders == []


def test_active_tier3_evidence_reports_use_capability_scoped_names() -> None:
    offenders = []
    tier3_root = ROOT / "compliance" / "evidence" / "tier3"
    for path in tier3_root.rglob("*"):
        if path.is_file() and FORBIDDEN_PATTERN.search(path.relative_to(ROOT).as_posix()):
            offenders.append(path.relative_to(ROOT).as_posix())

    assert offenders == []


def test_active_tier3_evidence_metadata_uses_capability_scoped_names() -> None:
    offenders = []
    tier3_root = ROOT / "compliance" / "evidence" / "tier3"
    metadata_globs = (
        "*/contracts/*.json",
        "*/manifest.yaml",
        "*/mapping.yaml",
        "*/hashes.yaml",
        "*/signatures.yaml",
    )
    for glob in metadata_globs:
        for path in tier3_root.glob(glob):
            text = path.read_text(encoding="utf-8", errors="ignore")
            if FORBIDDEN_PATTERN.search(text):
                offenders.append(path.relative_to(ROOT).as_posix())

    assert offenders == []


def test_retained_boundary_bundle_metadata_uses_capability_scoped_names() -> None:
    offenders = []
    tier3_root = ROOT / "compliance" / "evidence" / "tier3"
    forbidden = re.compile(
        rf"(?i)(?:checkpoint|source_checkpoint|{FORBIDDEN_FRAGMENTS[0]}\d+|{FORBIDDEN_FRAGMENTS[1]}\d+)"
    )

    for bundle in RETAINED_BOUNDARY_BUNDLES:
        bundle_root = tier3_root / bundle
        for name in GENERATOR_OWNED_BUNDLE_FILES:
            path = bundle_root / name
            text = path.read_text(encoding="utf-8", errors="ignore")
            if forbidden.search(text):
                offenders.append(path.relative_to(ROOT).as_posix())

    assert offenders == []


def test_active_runtime_status_values_use_capability_scoped_names() -> None:
    offenders = []
    for path in (ROOT / "tigrbl_auth").rglob("*.py"):
        if "__pycache__" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for match in re.finditer(r"runtime_status\s*=\s*[\"']([^\"']+)[\"']|STATUS:\s*Final\[str\]\s*=\s*[\"']([^\"']+)[\"']", text):
            value = match.group(1) or match.group(2) or ""
            if FORBIDDEN_PATTERN.search(value):
                offenders.append(f"{path.relative_to(ROOT).as_posix()}:{value}")

    assert offenders == []


def test_current_document_authority_projection_uses_capability_scoped_names() -> None:
    offenders = []
    paths = (
        ROOT / "compliance" / "targets" / "document-authority.yaml",
        ROOT / "docs" / "compliance" / "AUTHORITATIVE_CURRENT_DOCS.json",
        ROOT / "docs" / "compliance" / "AUTHORITATIVE_CURRENT_DOCS.md",
        ROOT / "docs" / "compliance" / "PACKAGE_REVIEW_GAP_ANALYSIS.json",
        ROOT / "docs" / "compliance" / "PACKAGE_REVIEW_GAP_ANALYSIS.md",
        ROOT / "docs" / "compliance" / "non_rfc_status_report.json",
        ROOT / "docs" / "compliance" / "non_rfc_status_report.md",
    )
    for path in paths:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if FORBIDDEN_PATTERN.search(path.relative_to(ROOT).as_posix()) or FORBIDDEN_PATTERN.search(text):
            offenders.append(path.relative_to(ROOT).as_posix())

    assert offenders == []


def test_active_repository_state_uses_capability_scoped_names() -> None:
    offenders = []
    paths = (
        ROOT / "compliance" / "claims" / "repository-state.yaml",
        ROOT / "compliance" / "evidence" / "manifest.yaml",
    )
    for path in paths:
        text = path.read_text(encoding="utf-8", errors="ignore")
        if FORBIDDEN_PATTERN.search(text):
            offenders.append(path.relative_to(ROOT).as_posix())

    assert offenders == []
