from __future__ import annotations

from pathlib import Path as _SplitPath

_SPLIT_GLOBALS = globals()
for _split_index in range(1, 100):
    _split_part_path = _SplitPath(__file__).with_name(f"part_{{_split_index:02d}}.py")
    if not _split_part_path.exists():
        continue
    exec(compile(_split_part_path.read_text(encoding="utf-8"), str(_split_part_path), "exec"), _SPLIT_GLOBALS)

del _SplitPath, _SPLIT_GLOBALS, _split_index, _split_part_path
