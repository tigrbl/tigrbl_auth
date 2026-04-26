from __future__ import annotations

import pytest


pytestmark = pytest.mark.skip(
    reason="Runtime profile loader is specified but not implemented yet."
)


def test_packaged_runtime_profiles_load_and_validate() -> None:
    """Every packaged tigrbl_auth/profiles/*.yaml file loads and validates."""


def test_runtime_profile_loader_fails_closed_for_invalid_profiles() -> None:
    """Malformed, duplicate, missing, or inconsistent profile files fail closed."""


def test_runtime_profile_resolver_applies_operator_overrides() -> None:
    """Profile files compose with environment and CLI overrides through the resolver."""


def test_runtime_profile_outputs_drive_contracts_and_surfaces() -> None:
    """Routes, RPC, diagnostics, OpenAPI, OpenRPC, and evidence derive from ResolvedDeployment."""
