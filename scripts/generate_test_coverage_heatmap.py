from __future__ import annotations

import json
from pathlib import Path
from typing import Any


from _surface_checks import categorized_tests, target_test_mappings, target_index

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "docs" / "compliance"


def build_heatmap(repo_root: Path) -> dict[str, Any]:
    categories = categorized_tests(repo_root)
    file_to_category = {
        rel: category
        for category, files in categories.items()
        for rel in files
    }
    mappings = target_test_mappings(repo_root)
    targets = target_index(repo_root)
    rows: list[dict[str, Any]] = []
    for label in sorted(targets):
        refs = [str(path).replace("\\", "/") for path in mappings.get(label, [])]
        counts = {category: 0 for category in categories}
        for ref in refs:
            category = file_to_category.get(ref)
            if category is not None:
                counts[category] += 1
        rows.append({
            "target": label,
            **counts,
            "total": sum(counts.values()),
            "tests": refs,
        })
    return {
        "schema_version": 1,
        "category_order": list(categories.keys()),
        "rows": rows,
        "summary": {
            "target_count": len(rows),
            "classified_test_count": len(file_to_category),
        },
    }


def write_heatmap(payload: dict[str, Any]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "test_coverage_heatmap.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# TEST_COVERAGE_HEATMAP",
        "",
        "Coverage counts are derived from `compliance/mappings/target-to-test.yaml` and the canonical `compliance/mappings/test_classification.yaml` manifest.",
        "",
        f"- target_count: `{payload['summary']['target_count']}`",
        f"- classified_test_count: `{payload['summary']['classified_test_count']}`",
        "",
        "| Target | Unit | Integration | Conformance | Interop | E2E | Security | Negative | Perf | Total |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in payload["rows"]:
        lines.append(
            f"| {row['target']} | {row.get('unit', 0)} | {row.get('integration', 0)} | {row.get('conformance', 0)} | "
            f"{row.get('interop', 0)} | {row.get('e2e', 0)} | {row.get('security', 0)} | {row.get('negative', 0)} | {row.get('perf', 0)} | {row['total']} |"
        )
    (OUTPUT_DIR / "TEST_COVERAGE_HEATMAP.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    payload = build_heatmap(ROOT)
    write_heatmap(payload)
