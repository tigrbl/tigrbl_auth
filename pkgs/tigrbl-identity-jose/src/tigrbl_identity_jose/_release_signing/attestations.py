from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from .models import LoadedSigner
from .utils import STATEMENT_TYPE_ARTIFACT, STATEMENT_TYPE_BUNDLE, STATEMENT_VERSION, sha256_file


def build_contract_set_manifest(bundle_root: Path) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    for path in sorted((bundle_root / "specs").rglob("*")):
        if not path.is_file():
            continue
        rel = str(path.relative_to(bundle_root)).replace("\\", "/")
        entries.append({
            "path": rel,
            "sha256": sha256_file(path),
            "bytes": path.stat().st_size,
        })
    return {
        "schema_version": STATEMENT_VERSION,
        "kind": "contract-set",
        "contract_count": len(entries),
        "contracts": entries,
    }


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_attestation(path: Path, attestation: dict[str, Any]) -> None:
    _write_json(path, attestation)


def _artifact_subject(
    *,
    label: str,
    artifact_path: str,
    artifact_sha256: str,
    package: str,
    version: str,
    profile: str,
    artifact_kind: str,
    media_type: str,
) -> dict[str, Any]:
    return {
        "package": package,
        "version": version,
        "profile": profile,
        "artifact_label": label,
        "artifact_kind": artifact_kind,
        "artifact_path": artifact_path,
        "artifact_sha256": artifact_sha256,
        "media_type": media_type,
    }


def write_artifact_attestation(
    bundle_root: Path,
    *,
    signer: LoadedSigner,
    label: str,
    artifact_rel_path: str,
    package: str,
    version: str,
    profile: str,
    artifact_kind: str,
    media_type: str,
) -> dict[str, Any]:
    artifact_path = bundle_root / artifact_rel_path
    subject = _artifact_subject(
        label=label,
        artifact_path=artifact_rel_path,
        artifact_sha256=sha256_file(artifact_path),
        package=package,
        version=version,
        profile=profile,
        artifact_kind=artifact_kind,
        media_type=media_type,
    )
    statement = signer.sign_statement(STATEMENT_TYPE_ARTIFACT, subject)
    attestation_path = bundle_root / "attestations" / f"{label}.attestation.json"
    write_attestation(attestation_path, statement)
    return {
        "label": label,
        "artifact_path": artifact_rel_path,
        "artifact_sha256": subject["artifact_sha256"],
        "attestation_path": str(attestation_path.relative_to(bundle_root)).replace("\\", "/"),
    }


def write_bundle_attestation(
    bundle_root: Path,
    *,
    signer: LoadedSigner,
    package: str,
    version: str,
    profile: str,
    signed_artifacts: Iterable[dict[str, Any]],
) -> dict[str, Any]:
    subject = {
        "package": package,
        "version": version,
        "profile": profile,
        "bundle_root": str(bundle_root.name),
        "signed_artifacts": list(signed_artifacts),
    }
    statement = signer.sign_statement(STATEMENT_TYPE_BUNDLE, subject)
    attestation_path = bundle_root / "attestations" / "release-attestation.json"
    write_attestation(attestation_path, statement)
    return {
        "attestation_path": str(attestation_path.relative_to(bundle_root)).replace("\\", "/"),
        "statement": statement,
    }
