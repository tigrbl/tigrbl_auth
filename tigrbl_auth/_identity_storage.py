"""Import helpers for the identity-storage split package.

The root ``tigrbl_auth`` package keeps compatibility facades for historical
imports. In editable monorepo checkouts the split package may not be installed,
so facades use this helper to find the sibling source tree without changing
the public import contract.
"""

from __future__ import annotations

from importlib import import_module
from pathlib import Path
import sys


def ensure_identity_storage_importable() -> None:
    """Make ``tigrbl_identity_storage`` importable in repo-local checkouts."""

    try:
        import_module("tigrbl_identity_storage")
        return
    except ModuleNotFoundError as exc:
        if exc.name != "tigrbl_identity_storage":
            raise

    repo_src = (
        Path(__file__).resolve().parents[1]
        / "pkgs"
        / "tigrbl-identity-storage"
        / "src"
    )
    if repo_src.exists():
        src = str(repo_src)
        if src not in sys.path:
            sys.path.insert(0, src)

    import_module("tigrbl_identity_storage")


__all__ = ["ensure_identity_storage_importable"]
