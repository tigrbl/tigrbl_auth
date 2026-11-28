"""Compatibility facade for release-certification runtime metadata."""

from tba_auth._split_imports import alias_module as _alias_module

_module = _alias_module(
    __name__,
    "tba_certification_release.runtime_metadata",
    "tba-certification-release",
)
globals().update(_module.__dict__)
