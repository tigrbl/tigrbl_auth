from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python < 3.11 fallback
    import tomli as tomllib


_ENTRYPOINT_WORKFLOWS = (
    "pr.yml",
    "main.yml",
    "release-candidate.yml",
    "release.yml",
    "recertify.yml",
)
_REUSABLE_INSTALL_WORKFLOWS = ("_certification-matrix.yml",)
_REUSABLE_RELEASE_WORKFLOWS = (
    "_contracts.yml",
    "_certification-matrix.yml",
    "_evidence.yml",
    "_release-bundle.yml",
)
_LEGACY_INSTALL_WORKFLOWS = ("ci-install-profiles.yml",)
_LEGACY_RELEASE_WORKFLOWS = ("ci-release-gates.yml",)
_NON_INDEPENDENT_EVIDENCE_MARKERS = (
    "fixture",
    "self",
    "package-generated",
    "checkpoint-staged-external-root",
    "repository-fixture",
)


def _repo_root_from(anchor: Path | None = None) -> Path:
    if anchor is not None:
        return anchor.resolve()
    return Path(__file__).resolve().parents[1]


def load_pyproject_manifest(repo_root: Path | None = None) -> dict[str, Any]:
    root = _repo_root_from(repo_root)
    pyproject = root / "pyproject.toml"
    if not pyproject.exists():
        return {}
    return tomllib.loads(pyproject.read_text(encoding="utf-8"))


def package_version(repo_root: Path | None = None) -> str:
    manifest = load_pyproject_manifest(repo_root)
    project = manifest.get("project", {}) if isinstance(manifest, dict) else {}
    version = str(project.get("version", "")).strip()
    return version or "0.0.0"


def workflow_inventory(repo_root: Path) -> dict[str, str]:
    root = _repo_root_from(repo_root)
    workflow_dir = root / ".github" / "workflows"
    inventory: dict[str, str] = {}
    for path in sorted(workflow_dir.glob("*.yml")) if workflow_dir.exists() else []:
        inventory[path.name] = path.read_text(encoding="utf-8")
    return inventory


def workflow_paths(repo_root: Path) -> list[str]:
    return [f".github/workflows/{name}" for name in workflow_inventory(repo_root)]


def workflow_role_text(repo_root: Path, role: str) -> str:
    inventory = workflow_inventory(repo_root)
    paths = workflow_role_paths(repo_root, role)
    return "\n".join(inventory[Path(path).name] for path in paths)


def workflow_role_paths(repo_root: Path, role: str) -> list[str]:
    inventory = workflow_inventory(repo_root)
    if role == "install-matrix":
        ordered = (
            *_LEGACY_INSTALL_WORKFLOWS,
            *_REUSABLE_INSTALL_WORKFLOWS,
            "main.yml",
            "recertify.yml",
            "release-candidate.yml",
            "release.yml",
        )
    elif role == "release-gates":
        ordered = (
            *_LEGACY_RELEASE_WORKFLOWS,
            *_REUSABLE_RELEASE_WORKFLOWS,
            *_ENTRYPOINT_WORKFLOWS,
        )
    else:
        ordered = tuple(inventory)
    return [f".github/workflows/{name}" for name in ordered if name in inventory]


def has_install_matrix_workflow(repo_root: Path) -> bool:
    inventory = workflow_inventory(repo_root)
    if any(name in inventory for name in _LEGACY_INSTALL_WORKFLOWS):
        return True
    reusable_present = all(name in inventory for name in _REUSABLE_INSTALL_WORKFLOWS)
    if not reusable_present:
        return False
    reusable_ref = "./.github/workflows/_certification-matrix.yml"
    return any(reusable_ref in inventory.get(name, "") for name in _ENTRYPOINT_WORKFLOWS if name in inventory)


def has_release_gate_workflow(repo_root: Path) -> bool:
    inventory = workflow_inventory(repo_root)
    if any(name in inventory for name in _LEGACY_RELEASE_WORKFLOWS):
        return True
    required = set(_REUSABLE_RELEASE_WORKFLOWS)
    if not required <= set(inventory):
        return False
    return any(
        any(f"./.github/workflows/{workflow}" in inventory.get(name, "") for workflow in _REUSABLE_RELEASE_WORKFLOWS)
        for name in _ENTRYPOINT_WORKFLOWS
        if name in inventory
    )


def evaluate_tier4_bundle(bundle_root: Path, manifest: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    failures: list[str] = []
    required_artifacts = ("manifest.yaml", "mapping.yaml", "execution.log", "peer-profile.yaml", "peer-artifacts", "reproduction.md")
    for name in required_artifacts:
        if not (bundle_root / name).exists():
            failures.append(f"missing required artifact: {bundle_root.name}/{name}")

    status = str(manifest.get("status", "")).strip()
    peer_profile = str(manifest.get("peer_profile", "")).strip()
    evidence_source = str(manifest.get("evidence_source", "")).strip()
    peer_identity = manifest.get("peer_identity") or {}
    peer_runtime = manifest.get("peer_runtime") or {}
    independence = manifest.get("independence_attestation") or {}
    validation_failures = [str(item) for item in (manifest.get("validation_failures") or [])]
    peer_operator = str(peer_identity.get("peer_operator", "")).strip()
    peer_version = str(peer_identity.get("peer_version", "") or peer_runtime.get("counterpart_version", "")).strip()
    attestation_class = str(independence.get("attestation_class", "")).strip()
    source_revision = str(manifest.get("source_revision", "")).strip()
    image_ref = str(peer_runtime.get("image_ref", "")).strip()
    image_digest = str(peer_runtime.get("image_digest", "")).strip()
    has_reproduction = (bundle_root / "reproduction.md").exists()
    lowered_operator = peer_operator.lower()
    lowered_source = evidence_source.lower()

    if status not in {"external-preserved-passed", "external-validated-passed", "promotion-eligible"}:
        failures.append(f"non-qualifying bundle status: {status or 'missing'}")
    if not peer_profile:
        failures.append("missing peer_profile")
    if attestation_class not in {"external-independent", "independent-external", "tier4-independent"}:
        failures.append(f"non-independent attestation class: {attestation_class or 'missing'}")
    if not peer_operator:
        failures.append("missing peer_identity.peer_operator")
    elif any(marker in lowered_operator for marker in _NON_INDEPENDENT_EVIDENCE_MARKERS):
        failures.append("peer operator is not independent")
    if not peer_version:
        failures.append("missing peer version metadata")
    if not evidence_source:
        failures.append("missing evidence_source")
    elif any(marker in lowered_source for marker in _NON_INDEPENDENT_EVIDENCE_MARKERS):
        failures.append("evidence source is not independent")
    if not source_revision:
        failures.append("missing source_revision")
    if not image_ref:
        failures.append("missing peer_runtime.image_ref")
    if not image_digest:
        failures.append("missing peer_runtime.image_digest")
    elif not image_digest.startswith("sha256:"):
        failures.append("peer_runtime.image_digest must be immutable")
    if not has_reproduction:
        failures.append("missing reproduction material")
    if validation_failures:
        failures.append("bundle manifest contains validation failures")

    details = {
        "status": status,
        "peer_profile": peer_profile,
        "attestation_class": attestation_class,
        "peer_operator": peer_operator,
        "peer_version": peer_version,
        "evidence_source": evidence_source,
        "source_revision": source_revision,
        "image_ref": image_ref,
        "image_digest": image_digest,
        "has_reproduction": has_reproduction,
        "validation_failure_count": len(validation_failures),
    }
    return not failures, failures, details
