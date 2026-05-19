from __future__ import annotations

import difflib
import json
from pathlib import Path
from typing import Any

from ._operator_store import ArtifactResult, OperationContext, display_path, validate_checksum, write_structured


def _profile_dir(repo_root: Path, profile: str | None) -> Path:
    chosen = (profile or "baseline").strip() or "baseline"
    path = repo_root / "specs" / "discovery" / "profiles" / chosen
    if path.exists():
        return path
    return repo_root / "specs" / "discovery" / "profiles" / "baseline"


def show_discovery(repo_root: Path, *, profile: str | None = None) -> dict[str, Any]:
    directory = _profile_dir(repo_root, profile)
    documents: dict[str, Any] = {}
    for path in sorted(directory.glob("*.json")):
        documents[path.name] = json.loads(path.read_text(encoding="utf-8"))
    return {"profile": directory.name, "documents": documents}


def validate_discovery(repo_root: Path, *, profile: str | None = None) -> dict[str, Any]:
    payload = show_discovery(repo_root, profile=profile)
    docs = payload["documents"]
    return {
        "profile": payload["profile"],
        "document_count": len(docs),
        "documents": sorted(docs.keys()),
        "valid": bool(docs),
    }


def publish_discovery(context: OperationContext, *, output_dir: Path | None = None) -> ArtifactResult:
    directory = _profile_dir(context.repo_root, context.profile)
    output_dir = output_dir or (context.repo_root / "dist" / "discovery" / directory.name)
    output_dir.mkdir(parents=True, exist_ok=True)
    docs = {}
    for path in sorted(directory.glob("*.json")):
        target = output_dir / path.name
        target.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
        docs[path.name] = validate_checksum(target)
    manifest = output_dir / "manifest.json"
    write_structured(manifest, {"profile": directory.name, "documents": docs})
    return ArtifactResult(command=context.command, resource=context.resource, status="published", path=display_path(output_dir, context.repo_root), checksum=validate_checksum(manifest), summary={"profile": directory.name, "documents": len(docs)})


def diff_discovery(repo_root: Path, *, left_profile: str | None = None, right_profile: str | None = None) -> dict[str, Any]:
    left = show_discovery(repo_root, profile=left_profile)
    right = show_discovery(repo_root, profile=right_profile)
    left_docs = left["documents"]
    right_docs = right["documents"]
    keys = sorted(set(left_docs) | set(right_docs))
    diffs: dict[str, Any] = {}
    for key in keys:
        left_text = json.dumps(left_docs.get(key), indent=2, sort_keys=True).splitlines()
        right_text = json.dumps(right_docs.get(key), indent=2, sort_keys=True).splitlines()
        if left_text != right_text:
            diffs[key] = list(difflib.unified_diff(left_text, right_text, fromfile=f"{left['profile']}/{key}", tofile=f"{right['profile']}/{key}", lineterm=""))
    return {"left_profile": left["profile"], "right_profile": right["profile"], "document_count": len(keys), "changed": sorted(diffs.keys()), "diffs": diffs}


__all__ = [
    "diff_discovery",
    "publish_discovery",
    "show_discovery",
    "validate_discovery",
]
