"""Compatibility loader for the split register implementation."""
from __future__ import annotations

from pathlib import Path as _SplitPath

_SPLIT_PARTS_DIR = _SplitPath(__file__).with_name('_register')
for _split_index in range(1, 100):
    _split_part_path = _SPLIT_PARTS_DIR / f"part_{_split_index:02d}.py"
    if not _split_part_path.exists():
        continue
    exec(compile(_split_part_path.read_text(encoding="utf-8"), str(_split_part_path), "exec"), globals())

del _SplitPath, _SPLIT_PARTS_DIR, _split_index, _split_part_path
