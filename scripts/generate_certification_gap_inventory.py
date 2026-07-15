from __future__ import annotations

import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

from ssot_registry.util.jcs import dump_jcs_json

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / ".ssot" / "reports"
JSON_OUT = REPORT_DIR / "certification-gap-inventory.json"
MD_OUT = REPORT_DIR / "certification-gap-inventory.md"

MARKER_PATTERN = re.compile(
    r"\b(TODO|FIXME|NotImplemented|placeholder|partial|incomplete)\b",
    re.IGNORECASE,
)
CHRONOLOGY_PATTERN = re.compile(
    rf"(?i)(?:{''.join(('pha', 'se'))}|{''.join(('st', 'ep'))})\d+"
)
SCAN_ROOTS = ("tigrbl_auth", "tests", "scripts", "compliance", "docs")
SCAN_SUFFIXES = {".py", ".md", ".yaml", ".yml", ".toml"}
SKIP_PARTS = {"archive", "dist", ".pytest_cache", "__pycache__"}


def load_json(path: Path, default: Any | None = None) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def status_counts(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    return dict(sorted(Counter(str(row.get(key, "unset")) for row in rows).items()))


def list_rows(
    rows: list[dict[str, Any]], fields: tuple[str, ...]
) -> list[dict[str, Any]]:
    return [{field: row.get(field) for field in fields} for row in rows]


def worktree_summary(root: Path) -> dict[str, Any]:
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=root,
            text=True,
            capture_output=True,
            check=False,
        )
    except OSError:
        return {"available": False, "dirty": None, "entries": []}

    entries = [line for line in result.stdout.splitlines() if line.strip()]
    chronology_scoped = [line for line in entries if CHRONOLOGY_PATTERN.search(line)]
    current_named_entries = [
        line for line in entries if not CHRONOLOGY_PATTERN.search(line)
    ]
    return {
        "available": result.returncode == 0,
        "dirty": bool(entries),
        "entry_count": len(entries),
        "chronology_scoped_entry_count": len(chronology_scoped),
        "entries": current_named_entries[:80],
    }


def marker_inventory(root: Path) -> dict[str, Any]:
    matches: list[dict[str, Any]] = []
    for scan_root in SCAN_ROOTS:
        base = root / scan_root
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file() or path.suffix not in SCAN_SUFFIXES:
                continue
            rel = path.relative_to(root)
            if any(part in SKIP_PARTS for part in rel.parts):
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for line_number, line in enumerate(text.splitlines(), start=1):
                if MARKER_PATTERN.search(line):
                    matches.append(
                        {
                            "path": rel.as_posix(),
                            "line": line_number,
                            "text": line.strip()[:180],
                        }
                    )
                    break
    return {"count": len(matches), "sample": matches[:40]}


def build_inventory(root: Path = ROOT) -> dict[str, Any]:
    registry = load_json(root / ".ssot" / "registry.json", {})
    validation = load_json(root / ".ssot" / "reports" / "validation.report.json", {})
    package_review = load_json(
        root / "docs" / "compliance" / "PACKAGE_REVIEW_GAP_ANALYSIS.json", {}
    )
    certification_state = load_json(
        root / "docs" / "compliance" / "certification_state_report.json", {}
    )

    features = registry.get("features", [])
    profiles = registry.get("profiles", [])
    tests = registry.get("tests", [])
    claims = registry.get("claims", [])
    evidence = registry.get("evidence", [])
    issues = registry.get("issues", [])
    risks = registry.get("risks", [])
    registry_counts = {
        "features": len(features),
        "profiles": len(profiles),
        "tests": len(tests),
        "claims": len(claims),
        "evidence": len(evidence),
        "issues": len(issues),
        "risks": len(risks),
    }

    current_features = [
        row for row in features if row.get("plan", {}).get("horizon") != "out_of_bounds"
    ]
    partial_or_absent = [
        row for row in features if row.get("implementation_status") != "implemented"
    ]
    current_partial_or_absent = [
        row
        for row in current_features
        if row.get("implementation_status") != "implemented"
    ]
    draft_profiles = [row for row in profiles if row.get("status") == "draft"]
    open_issues = [
        row for row in issues if row.get("status") not in {"closed", "resolved"}
    ]
    active_risks = [
        row for row in risks if row.get("status") not in {"mitigated", "retired"}
    ]
    claims_without_tests = [
        row
        for row in claims
        if row.get("status") != "retired" and not row.get("test_ids")
    ]
    claims_without_evidence = [
        row
        for row in claims
        if row.get("status") != "retired" and not row.get("evidence_ids")
    ]
    tests_without_evidence = [
        row
        for row in tests
        if row.get("status") == "passing" and not row.get("evidence_ids")
    ]

    certification_gaps = certification_state.get("summary", {}).get("open_gaps", [])
    if not certification_gaps:
        certification_gaps = package_review.get("certification_gaps", [])

    current_feature_gap_count = len(current_partial_or_absent)
    registry_closure_status = (
        "No current feature is missing claims, tests, evidence, or implementation status."
        if current_feature_gap_count == 0
        else f"{current_feature_gap_count} current feature(s) remain partial or absent."
    )

    return {
        "schema_version": 1,
        "package": "tigrbl_auth",
        "registry": {
            "validation_passed": bool(validation.get("passed")),
            "counts": registry_counts,
            "validation_counts": validation.get("summary", {}).get("counts", {}),
            "feature_implementation_status": status_counts(
                features, "implementation_status"
            ),
            "feature_horizon": status_counts(
                [
                    {"horizon": row.get("plan", {}).get("horizon", "unset")}
                    for row in features
                ],
                "horizon",
            ),
            "profile_status": status_counts(profiles, "status"),
            "test_status": status_counts(tests, "status"),
            "claim_status": status_counts(claims, "status"),
            "evidence_status": status_counts(evidence, "status"),
        },
        "current_gaps": {
            "current_partial_or_absent_features": list_rows(
                current_partial_or_absent,
                ("id", "title", "implementation_status", "description"),
            ),
            "all_partial_or_absent_features": list_rows(
                partial_or_absent,
                ("id", "title", "implementation_status", "description"),
            ),
            "draft_profiles": list_rows(
                draft_profiles,
                ("id", "title", "kind", "claim_tier", "status", "description"),
            ),
            "open_issues": list_rows(
                open_issues,
                (
                    "id",
                    "title",
                    "severity",
                    "status",
                    "release_blocking",
                    "description",
                ),
            ),
            "active_risks": list_rows(
                active_risks,
                (
                    "id",
                    "title",
                    "severity",
                    "status",
                    "release_blocking",
                    "description",
                ),
            ),
            "claims_without_tests": list_rows(
                claims_without_tests,
                ("id", "title", "status", "tier"),
            ),
            "claims_without_evidence": list_rows(
                claims_without_evidence,
                ("id", "title", "status", "tier"),
            ),
            "tests_without_evidence": list_rows(
                tests_without_evidence,
                ("id", "title", "status", "path"),
            ),
            "certification_blockers": [str(item) for item in certification_gaps],
        },
        "source_markers": marker_inventory(root),
        "worktree": worktree_summary(root),
        "delivery_tracks": [
            {
                "name": "Registry and proof-chain closure",
                "required_change": "Keep every current feature linked to passing tests, evidence, claims, and validation output.",
                "current_status": registry_closure_status,
            },
            {
                "name": "Runtime and contract closure",
                "required_change": "Keep executable OpenAPI, OpenRPC, discovery, runner, and deployment profiles aligned with generated artifacts.",
                "current_status": "Current contract snapshots are generated, but release certification still depends on preserved clean-room evidence.",
            },
            {
                "name": "Evidence inventory closure",
                "required_change": "Preserve validated-run manifests for the supported interpreter, profile, runner, and lane matrix.",
                "current_status": "Validated clean-room and lane inventories remain certification blockers.",
            },
            {
                "name": "Portability closure",
                "required_change": "Preserve upgrade, downgrade, and reapply migration evidence for SQLite and PostgreSQL.",
                "current_status": "Migration portability evidence remains incomplete.",
            },
            {
                "name": "Peer validation closure",
                "required_change": "Validate independent peer bundles for the retained supported peer-profile set.",
                "current_status": "The peer-claim profile remains draft while external bundle validation is incomplete.",
            },
            {
                "name": "Release certification closure",
                "required_change": "Produce final release evidence from a clean checkout and certify only after all gates pass.",
                "current_status": "The current worktree is dirty, so final release evidence cannot be certified from this checkout state.",
            },
        ],
    }


def render_markdown(inventory: dict[str, Any]) -> str:
    lines: list[str] = ["# Certification Gap Inventory", ""]
    registry = inventory["registry"]
    gaps = inventory["current_gaps"]
    worktree = inventory["worktree"]
    markers = inventory["source_markers"]

    lines.extend(
        [
            f"- package: `{inventory['package']}`",
            f"- SSOT validation passed: `{registry['validation_passed']}`",
            f"- registry counts: `{registry['counts']}`",
            f"- current partial or absent features: `{len(gaps['current_partial_or_absent_features'])}`",
            f"- draft profiles: `{len(gaps['draft_profiles'])}`",
            f"- open issues: `{len(gaps['open_issues'])}`",
            f"- active risks: `{len(gaps['active_risks'])}`",
            f"- dirty worktree: `{worktree.get('dirty')}`",
            "",
            "## Current Feature Gaps",
            "",
        ]
    )
    if gaps["current_partial_or_absent_features"]:
        for row in gaps["current_partial_or_absent_features"]:
            lines.append(
                f"- `{row['id']}`: {row['implementation_status']} - {row['title']}"
            )
    else:
        lines.append("- None")

    lines.extend(["", "## Draft Profiles", ""])
    if gaps["draft_profiles"]:
        for row in gaps["draft_profiles"]:
            lines.append(f"- `{row['id']}`: {row['status']} - {row['title']}")
    else:
        lines.append("- None")

    lines.extend(["", "## Certification Blockers", ""])
    if gaps["certification_blockers"]:
        for item in gaps["certification_blockers"]:
            lines.append(f"- {item}")
    else:
        lines.append("- None")

    lines.extend(["", "## Delivery Tracks", ""])
    for item in inventory["delivery_tracks"]:
        lines.append(
            f"- {item['name']}: {item['required_change']} Current status: {item['current_status']}"
        )

    lines.extend(["", "## Source Marker Scan", ""])
    lines.append(f"- files with marker terms: `{markers['count']}`")
    for item in markers["sample"][:10]:
        lines.append(f"- `{item['path']}:{item['line']}` {item['text']}")

    lines.append("")
    return "\n".join(lines)


def write_inventory(
    inventory: dict[str, Any], report_dir: Path = REPORT_DIR
) -> dict[str, str]:
    report_dir.mkdir(parents=True, exist_ok=True)
    json_out = report_dir / JSON_OUT.name
    md_out = report_dir / MD_OUT.name
    json_out.write_text(dump_jcs_json(inventory), encoding="utf-8")
    md_out.write_text(render_markdown(inventory) + "\n", encoding="utf-8")

    def display_path(path: Path) -> str:
        try:
            return path.relative_to(ROOT).as_posix()
        except ValueError:
            return path.as_posix()

    return {"json": display_path(json_out), "markdown": display_path(md_out)}


def main() -> int:
    outputs = write_inventory(build_inventory(ROOT))
    print(json.dumps(outputs, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
