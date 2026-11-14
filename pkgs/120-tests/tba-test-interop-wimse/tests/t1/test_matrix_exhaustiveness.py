from pathlib import Path
import sys

from tba_test_interop_wimse.catalog import read_catalog
from tba_test_interop_wimse.coverage import coverage_report
from tba_test_interop_wimse.matrix import generate_matrix

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from support.reference_matrix import structural_keys


def test_exact_exhaustive_scenario_keys():
    actual = generate_matrix()
    expected = set(structural_keys(read_catalog("scenarios.toml"),
                                  read_catalog("factors.toml"), read_catalog("exclusions.toml")))
    keys = [row["id"] for row in actual["scenarios"]]
    assert set(keys) == expected and len(keys) == len(expected)
    assert keys == [row["id"] for row in generate_matrix()["scenarios"]]


def test_adapter_and_qualification_gaps_remain_visible():
    report = coverage_report(generate_matrix(), {})
    assert len(report["no_adapter"]) == 3148
    assert len(report["unqualified"]) == 4448
