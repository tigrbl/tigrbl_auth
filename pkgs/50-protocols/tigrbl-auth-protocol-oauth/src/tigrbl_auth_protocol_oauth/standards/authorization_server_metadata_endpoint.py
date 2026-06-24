"""OAuth authorization server metadata endpoint exports."""

from __future__ import annotations
# ruff: noqa: F403,F405

from tigrbl_auth_protocol_oauth.standards.authorization_server_metadata import *

__all__ = [name for name in globals() if not name.startswith("_")]
