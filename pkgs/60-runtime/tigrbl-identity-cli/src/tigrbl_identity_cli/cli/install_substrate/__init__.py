from __future__ import annotations

from tigrbl_identity_cli.cli._fragment_loader import load_fragments as _load_fragments

_load_fragments(globals(), __file__, "install_substrate.py", (
    '_common',
    '_models',
    '_checks',
))

del _load_fragments
