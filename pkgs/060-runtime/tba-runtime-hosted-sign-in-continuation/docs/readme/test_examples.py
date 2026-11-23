from pathlib import Path
import runpy

import pytest


@pytest.mark.parametrize("name", ["quick_start.py", "usage.py"])
def test_example(name):
    runpy.run_path(str(Path(__file__).with_name(name)))
