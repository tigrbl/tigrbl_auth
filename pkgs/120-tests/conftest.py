"""Apply the repository's certification lanes to the migrated native suites."""

import os
from pathlib import Path
import sys

from tests.lanes import active_lane, lane_allows_path, skip_reason_for_test_path


def pytest_configure(config):
    if location := os.environ.get("TBA_WIMSE_INTEROP_PACKAGE"):
        package = Path(location).resolve()
        for directory in (package / "src", package / "tests"):
            sys.path.insert(0, str(directory))


def pytest_ignore_collect(collection_path: Path, config):
    if collection_path.suffix != ".py" or not collection_path.name.startswith("test_"):
        return None
    if "tba-tests-interop-wimse-cred" in collection_path.parts:
        return None
    if {"interop_native", "tba-tests-interop-wimse-matrix"} & set(collection_path.parts):
        if not os.environ.get("TBA_WIMSE_INTEROP_PACKAGE"):
            return True
    lane = active_lane(config.getoption("--certification-lane", default=None))
    if not lane_allows_path(lane, collection_path):
        return True
    if skip_reason_for_test_path(collection_path) is not None:
        return True
    return None
