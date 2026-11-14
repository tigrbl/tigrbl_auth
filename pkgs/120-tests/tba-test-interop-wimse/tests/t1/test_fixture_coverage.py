from tba_test_interop_wimse.coverage import inventory_report
from tba_test_interop_wimse.matrix import generate_matrix


def test_inventory_reports_every_id_without_qualifying_component_runs():
    matrix = generate_matrix()
    report = inventory_report(matrix)
    assert [row["id"] for row in report["scenarios"]] == [row["id"] for row in matrix["scenarios"]]
    assert [row["id"] for row in report["executions"]] == [row["id"] for row in matrix["executions"]]
    assert sum(bool(row["local_fixtures"]) for row in report["scenarios"]) == 12
    assert sum("wimsey_wic_component" in row["component_fixtures"] for row in report["executions"]) == 8
    assert sum("cred_wpt_component" in row["component_fixtures"] for row in report["executions"]) == 6
    assert all(row["qualification"] == "pending" and row["status"] == "not-run"
               for row in report["executions"])
