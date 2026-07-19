from tigrbl_workload_credential_conformance_testkit import VECTORS
from workload_credential_profiles_example import run_example

def test_vectors_cover_required_confusion_boundaries() -> None:
    profiles = {vector.profile for vector in VECTORS}
    assert {"jwt-svid", "wit-svid", "wpt", "cwt-svid-extension"}.issubset(profiles)
    assert any(not vector.expected_valid for vector in VECTORS)

def test_example_runs_structural_profiles_end_to_end() -> None:
    assert run_example() == ("wit", "wit-svid", "wpt")