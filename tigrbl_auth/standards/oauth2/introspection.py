"""Compatibility facade for ``tigrbl_auth_protocol_oauth.standards.introspection``."""

from pathlib import Path
import sys

from tigrbl_auth._split_imports import alias_module as _alias_module


def _prefer_workspace_oauth_protocol() -> None:
    for parent in Path(__file__).resolve().parents:
        if not (parent / "pkgs").is_dir():
            continue
        src = parent / "pkgs" / "tigrbl-auth-protocol-oauth" / "src"
        if not src.exists():
            return
        src_value = str(src)
        if src_value in sys.path:
            sys.path.remove(src_value)
        sys.path.insert(0, src_value)
        src_root = src.resolve()
        for module_name, module in list(sys.modules.items()):
            if module_name != "tigrbl_auth_protocol_oauth" and not module_name.startswith(
                "tigrbl_auth_protocol_oauth."
            ):
                continue
            module_file = getattr(module, "__file__", None)
            if module_file is None:
                continue
            try:
                if not Path(module_file).resolve().is_relative_to(src_root):
                    sys.modules.pop(module_name, None)
            except OSError:
                sys.modules.pop(module_name, None)
        return


_prefer_workspace_oauth_protocol()
_module = _alias_module(
    __name__,
    "tigrbl_auth_protocol_oauth.standards.introspection",
    "tigrbl-auth-protocol-oauth",
)
globals().update(_module.__dict__)
