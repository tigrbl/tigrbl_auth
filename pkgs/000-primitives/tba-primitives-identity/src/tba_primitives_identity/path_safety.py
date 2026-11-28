from __future__ import annotations

import re
from pathlib import Path
from typing import Any

_WINDOWS_ABSOLUTE_PATH = re.compile(r"\b[A-Za-z]:[\\/][^\s`'\"\]\)},]+")


def _as_posix(value: str) -> str:
    return value.replace("\\", "/")


def safe_display_path(
    path: Path | str, repo_root: Path, *, external_label: str = "<local-path>"
) -> str:
    """Return a stable repo-safe path for user-facing reports and committed artifacts."""

    candidate = Path(path)
    resolved_repo = repo_root.resolve()
    try:
        return candidate.resolve().relative_to(resolved_repo).as_posix()
    except Exception:
        pass

    raw = _as_posix(str(path))
    parts = [part for part in raw.split("/") if part]
    for marker, label in (
        (".pytest-tmp", "<repo>"),
        ("dist", "<repo>"),
        ("operator-state", "<operator-state>"),
        ("operator-plane", "<operator-state>"),
    ):
        if marker in parts:
            index = parts.index(marker)
            return "/".join([label, *parts[index:]])
    return f"{external_label}/{candidate.name or 'path'}"


def _redact_windows_path(match: re.Match[str]) -> str:
    raw = _as_posix(match.group(0))
    parts = [part for part in raw.split("/") if part]
    for marker, label in (
        (".pytest-tmp", "<repo>"),
        ("dist", "<repo>"),
        ("operator-state", "<operator-state>"),
        ("operator-plane", "<operator-state>"),
    ):
        if marker in parts:
            index = parts.index(marker)
            return "/".join([label, *parts[index:]])
    return "<local-path>"


def sanitize_local_paths(value: Any, repo_root: Path) -> Any:
    """Recursively redact local absolute paths from generated repo artifacts."""

    if isinstance(value, dict):
        return {
            key: sanitize_local_paths(item, repo_root) for key, item in value.items()
        }
    if isinstance(value, list):
        return [sanitize_local_paths(item, repo_root) for item in value]
    if isinstance(value, tuple):
        return tuple(sanitize_local_paths(item, repo_root) for item in value)
    if not isinstance(value, str):
        return value

    resolved_repo = repo_root.resolve()
    candidates = {
        str(resolved_repo),
        _as_posix(str(resolved_repo)),
    }
    text = value
    for candidate in sorted(candidates, key=len, reverse=True):
        if candidate:
            text = text.replace(candidate, "<repo>")
    text = _as_posix(text)
    return _WINDOWS_ABSOLUTE_PATH.sub(_redact_windows_path, text)
