import json
from xml.etree import ElementTree

import pytest

from tba_tests_interop_wimse.evidence import audit_pytest_report


def write_report(path, *, omit=False, skipped=False, duplicate=False):
    root = ElementTree.Element("testsuite")
    for key in ["one"] if omit else ["one", "one" if duplicate else "two"]:
        item = ElementTree.SubElement(root, "testcase")
        if skipped:
            ElementTree.SubElement(item, "skipped")
        properties = ElementTree.SubElement(item, "properties")
        for name, value in {
            "execution_id": key, "scenario_id": "scenario",
            "execution_result": json.dumps({
                "execution_id": key, "scenario_id": "scenario", "status": "passed",
                "observation": {"decision": "allow"},
            }),
        }.items():
            ElementTree.SubElement(properties, "property", name=name, value=value)
    ElementTree.ElementTree(root).write(path)


def test_audit_requires_individual_qualified_results(tmp_path):
    path = tmp_path / "report.xml"
    inventory = [{"id": key, "scenario_id": "scenario", "status": "qualified"}
                 for key in ("one", "two")]
    write_report(path)
    assert audit_pytest_report(inventory, path)["complete"]
    write_report(path, omit=True)
    assert audit_pytest_report(inventory, path)["counts"] == {"not-run": 1, "passed": 1}
    inventory[0]["status"] = "pending"
    with pytest.raises(ValueError, match="Invalid pass"):
        audit_pytest_report(inventory, path)
    inventory[0]["status"] = "qualified"
    write_report(path, skipped=True)
    with pytest.raises(ValueError, match="Invalid pass"):
        audit_pytest_report(inventory, path)
    write_report(path, duplicate=True)
    with pytest.raises(ValueError, match="duplicate attempt"):
        audit_pytest_report(inventory, path)
