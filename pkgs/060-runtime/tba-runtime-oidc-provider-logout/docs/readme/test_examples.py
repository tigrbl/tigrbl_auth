from pathlib import Path
from runpy import run_path

import pytest


@pytest.mark.unit
@pytest.mark.parametrize("example", ["quick_start.py", "usage.py"])
def test_readme_example(example: str) -> None:
    run_path(str(Path(__file__).with_name(example)))
