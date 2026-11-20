from tba_tests_workload_credential_conformance import VECTORS

assert any(vector.expected_valid for vector in VECTORS)
assert any(not vector.expected_valid for vector in VECTORS)
