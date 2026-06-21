"""Compatibility facade for `tigrbl_auth_release_certification.release_posture`."""

from tigrbl_auth._split_imports import alias_module as _alias_module

_module = _alias_module(
    __name__,
    "tigrbl_auth_release_certification.release_posture",
    "60-runtime/tigrbl-auth-release-certification",
)
globals().update(_module.__dict__)
