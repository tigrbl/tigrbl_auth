"""Compatibility facade for `tba_certification_release.release_posture`."""

from tba_auth._split_imports import alias_module as _alias_module

_module = _alias_module(
    __name__,
    "tba_certification_release.release_posture",
    "60-runtime/tba-certification-release",
)
globals().update(_module.__dict__)
