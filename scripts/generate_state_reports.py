from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tigrbl_auth.cli.claim_registry import generate_claim_registries
from tigrbl_auth.cli.reports import generate_state_reports, summarize_evidence_status
from tigrbl_auth.cli.truth import materialize_truth_chain
from tigrbl_identity_contracts.protocol_configuration import bind_protocol_settings
from tigrbl_identity_runtime.settings import settings


def main() -> int:
    bind_protocol_settings(settings)
    generate_claim_registries(ROOT)
    payload = generate_state_reports(ROOT)
    summarize_evidence_status(ROOT)
    materialize_truth_chain(ROOT)
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
