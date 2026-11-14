"""Apply the repository's certification lanes to the migrated native suites."""

import os
from pathlib import Path

from tests.lanes import active_lane, lane_allows_path, skip_reason_for_test_path


def pytest_ignore_collect(collection_path: Path, config):
    if collection_path.suffix != ".py" or not collection_path.name.startswith("test_"):
        return None
    if "tba-testkit-wimse-cred-interop" in collection_path.parts:
        return None
    lane = active_lane(config.getoption("--certification-lane", default=None))
    if not lane_allows_path(lane, collection_path):
        return True
    package_context = os.getenv("PACKAGE_UNDER_TEST") or os.getenv("TBA_AUTH_PACKAGE_UNDER_TEST")
    if "tba-tests-backend-apps" in collection_path.parts and package_context == collection_path.parent.name:
        return None
    if skip_reason_for_test_path(collection_path) is not None:
        return True
    return None
