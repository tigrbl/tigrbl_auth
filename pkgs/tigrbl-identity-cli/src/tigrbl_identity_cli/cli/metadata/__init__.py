from __future__ import annotations

from pathlib import Path as _Path

__file__ = str(_Path(__file__).resolve().parent.parent / "metadata.py")
_FRAGMENT_NAMES = (
    '_base',
    '_runtime_flags',
    '_arguments',
)
for _fragment_name in _FRAGMENT_NAMES:
    _fragment_path = _Path(__file__).resolve().parent / "metadata" / f"{_fragment_name}.py"
    exec(compile(_fragment_path.read_text(encoding="utf-8"), str(_fragment_path), "exec"), globals())

del _Path, _FRAGMENT_NAMES, _fragment_name, _fragment_path
