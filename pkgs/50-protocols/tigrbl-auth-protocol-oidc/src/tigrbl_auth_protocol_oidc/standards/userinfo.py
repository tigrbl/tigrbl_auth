"""OIDC UserInfo compatibility exports.

The UserInfo route is owned by ``tigrbl_identity_storage.tables._oidc_userinfo``.
"""

from __future__ import annotations

from tigrbl_identity_storage.tables._oidc_userinfo import include_oidc_userinfo

__all__ = ["include_oidc_userinfo"]
