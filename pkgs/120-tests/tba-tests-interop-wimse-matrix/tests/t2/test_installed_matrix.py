import json
import os
from pathlib import Path
import subprocess
import sys
import zipfile

import pytest
from tba_test_interop_wimse.matrix import generate_matrix


def test_installed_wheel_catalog_and_matrix(tmp_path):
    location = os.environ.get("TBA_WIMSE_INTEROP_WHEEL")
    if not location:
        pytest.skip("TBA_WIMSE_INTEROP_WHEEL must point to a built wheel")
    with zipfile.ZipFile(Path(location)) as wheel:
        assert {Path(name).name for name in wheel.namelist() if name.endswith(".toml")} == {
            "factors.toml", "exclusions.toml", "scenarios.toml", "peers.toml", "fixtures.toml", "hops.toml",
        }
        scripts = next(name for name in wheel.namelist() if name.endswith("/entry_points.txt"))
        assert b"tba-wimse-wpt-fixture = tba_test_interop_wimse.wpt_cli:main" in wheel.read(scripts)
        # Load the distribution exactly as shipped, with no source package on sys.path.
        wheel.extractall(tmp_path)
    command = [sys.executable, "-I", "-c",
               "import runpy,sys; sys.path.insert(0,sys.argv.pop(1)); "
               "runpy.run_module('tba_test_interop_wimse',run_name='__main__')",
               str(tmp_path), "--json"]
    completed = subprocess.run(command, check=True, capture_output=True, cwd=tmp_path, timeout=60)
    assert json.loads(completed.stdout) == generate_matrix()
