from __future__ import annotations

from tba_cli_identity.cli._fragment_loader import load_fragments as _load_fragments

_load_fragments(globals(), __file__, "claim_registry.py", (
    '_common',
    '_targets',
))

del _load_fragments
