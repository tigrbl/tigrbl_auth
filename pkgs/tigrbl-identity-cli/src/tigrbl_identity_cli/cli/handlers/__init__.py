from __future__ import annotations

from tigrbl_identity_cli.cli._fragment_loader import load_fragments as _load_fragments

_load_fragments(globals(), __file__, "handlers.py", (
    '_common',
    '_runtime',
    '_contracts',
    '_claims_evidence',
    '_adr_doctor',
    '_bootstrap_migrate',
))

del _load_fragments
