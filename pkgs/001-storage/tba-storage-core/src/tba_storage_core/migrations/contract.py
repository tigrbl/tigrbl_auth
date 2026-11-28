from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


REVISION_PATTERN = re.compile(r"^revision\s*=\s*[\"']([^\"']+)[\"']", re.MULTILINE)


@dataclass(frozen=True, slots=True)
class MigrationRevision:
    revision: str
    path: str
    ordinal: int


@dataclass(frozen=True, slots=True)
class MigrationContract:
    revisions: tuple[MigrationRevision, ...]
    required_collections: tuple[str, ...]

    @property
    def is_ordered(self) -> bool:
        return tuple(item.ordinal for item in self.revisions) == tuple(sorted(item.ordinal for item in self.revisions))

    @property
    def latest_revision(self) -> str | None:
        return self.revisions[-1].revision if self.revisions else None

    def assert_complete(self) -> None:
        if not self.revisions:
            raise ValueError("migration contract requires at least one revision")
        if not self.is_ordered:
            raise ValueError("migration revisions must be ordered")
        if len({item.revision for item in self.revisions}) != len(self.revisions):
            raise ValueError("migration revisions must be unique")


def collect_migration_revisions(versions_dir: Path) -> tuple[MigrationRevision, ...]:
    revisions: list[MigrationRevision] = []
    for path in sorted(versions_dir.glob("*.py")):
        if path.name == "__init__.py":
            continue
        text = path.read_text(encoding="utf-8")
        match = REVISION_PATTERN.search(text)
        if match is None:
            continue
        ordinal_text = path.name.split("_", 1)[0]
        ordinal = int(ordinal_text) if ordinal_text.isdigit() else len(revisions) + 1
        revisions.append(MigrationRevision(revision=match.group(1), path=path.as_posix(), ordinal=ordinal))
    return tuple(revisions)


def build_migration_contract(
    *,
    versions_dir: Path,
    required_collections: Iterable[str],
) -> MigrationContract:
    contract = MigrationContract(
        revisions=collect_migration_revisions(versions_dir),
        required_collections=tuple(sorted(set(required_collections))),
    )
    contract.assert_complete()
    return contract


__all__ = [
    "MigrationContract",
    "MigrationRevision",
    "build_migration_contract",
    "collect_migration_revisions",
]
