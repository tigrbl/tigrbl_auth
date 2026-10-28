
from tba_auth.cli.reports import diff_contracts

def test_contract_diff_runs_without_crash(tmp_path=None):
    # The live repository should have generated contracts that diff cleanly.
    # This test asserts execution only.
    assert isinstance(diff_contracts(__import__('pathlib').Path(__file__).resolve().parents[2]), dict)
