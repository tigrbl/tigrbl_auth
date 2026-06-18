from __future__ import annotations

from tigrbl_identity_cli.cli._fragment_loader import load_fragments as _load_fragments

_load_fragments(globals(), __file__, "reports.py", (
    '_common',
    '_contracts',
    '_truthfulness',
    '_feature_state',
    '_state_reports',
    '_execution_readiness',
    '_execution_status',
    '_execution_gates',
    '_classification',
    '_evidence_index',
))

del _load_fragments
