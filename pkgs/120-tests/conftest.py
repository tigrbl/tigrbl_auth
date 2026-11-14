"""Apply the repository's certification lanes to the migrated native suites."""

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
    if skip_reason_for_test_path(collection_path) is not None:
        return True
    return None
