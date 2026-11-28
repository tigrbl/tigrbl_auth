from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tba_auth.cli.metadata import (
    build_cli_conformance_snapshot,
    build_cli_contract_manifest,
    render_cli_conformance_markdown,
    render_cli_markdown,
)


def main() -> int:
    reference_target = ROOT / "docs" / "reference" / "CLI_SURFACE.md"
    reference_target.parent.mkdir(parents=True, exist_ok=True)
    reference_target.write_text(render_cli_markdown(), encoding="utf-8")

    contract = build_cli_contract_manifest()
    spec_root = ROOT / "specs" / "cli"
    spec_root.mkdir(parents=True, exist_ok=True)
    (spec_root / "cli_contract.json").write_text(json.dumps(contract, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (spec_root / "cli_contract.yaml").write_text(yaml.safe_dump(contract, sort_keys=False), encoding="utf-8")

    snapshot = build_cli_conformance_snapshot()
    compliance_root = ROOT / "docs" / "compliance"
    compliance_root.mkdir(parents=True, exist_ok=True)
    (compliance_root / "cli_conformance_snapshot.json").write_text(json.dumps(snapshot, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (compliance_root / "cli_conformance_snapshot.md").write_text(render_cli_conformance_markdown(snapshot), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
