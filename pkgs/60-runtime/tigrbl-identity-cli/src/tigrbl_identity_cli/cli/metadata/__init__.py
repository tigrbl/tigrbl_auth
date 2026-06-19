from __future__ import annotations

from tigrbl_identity_cli.cli._fragment_loader import load_fragments as _load_fragments

_load_fragments(globals(), __file__, "metadata.py", (
    '_base',
    '_runtime_flags',
    '_arguments',
))

del _load_fragments
