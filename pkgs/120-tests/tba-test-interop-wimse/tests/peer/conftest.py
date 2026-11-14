"""Default bindings for the peer suite. Local reference fixtures stay separate."""

import pytest


@pytest.fixture(scope="session")
def peer_adapters():
    """Map scenario family IDs to adapters backed by real peer deployments."""
    return {}


@pytest.fixture(scope="session")
def peer_setup_cache():
    return {}
