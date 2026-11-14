"""Reconcile evidence without replacing earlier attempts."""
from collections import Counter
import json
from xml.etree import ElementTree


def audit_pytest_report(executions, report):
    """Check the exact current inventory against individual JUnit outcomes."""
    expected = {row["id"]: row for row in executions}
    attempts = []
    for item in ElementTree.parse(report).iter("testcase"):
        values = {}
        for prop in item.findall("./properties/property"):
            if prop.get("name") in {"execution_id", "scenario_id", "execution_result"}:
                name = prop.get("name")
                if name in values:
                    raise ValueError(f"Repeated JUnit property: {name}")
                values[name] = prop.get("value")
        if set(values) != {"execution_id", "scenario_id", "execution_result"}:
            raise ValueError("JUnit item lacks peer execution evidence")
        result = json.loads(values["execution_result"])
        key = values["execution_id"]
        row = expected.get(key)
        if (row is None or result["execution_id"] != key
                or row["scenario_id"] != values["scenario_id"]
                or result["scenario_id"] != values["scenario_id"]):
            raise ValueError(f"Unexpected execution or scenario association: {key}")
        skipped = item.find("skipped") is not None
        unsuccessful = item.find("failure") is not None or item.find("error") is not None
        status = result["status"]
        if status == "passed" and (
            skipped or unsuccessful or row["status"] != "qualified"
            or not isinstance(result.get("observation"), dict)
        ):
            raise ValueError(f"Invalid pass evidence: {key}")
        if (status in {"failed", "setup-failure"} and not unsuccessful
                or status == "blocked" and not skipped
                or status not in {"passed", "blocked", "failed", "setup-failure"}):
            raise ValueError(f"JUnit and runner status disagree: {key}")
        attempts.append({**result, "attempt": 1})
    history = reconcile([row["id"] for row in executions], attempts)
    counts = Counter(row["status"] for row in history.values())
    return {"required": len(expected), "counts": dict(sorted(counts.items())),
            "complete": counts["passed"] == len(expected), "results": history}


def reconcile(execution_ids, attempts):
    records = {key: [] for key in execution_ids}
    if len(records) != len(execution_ids):
        raise ValueError("Duplicate execution ID")
    seen = set()
    for entry in attempts:
        key = entry["execution_id"]
        attempt = entry["attempt"]
        if key not in records or (key, attempt) in seen:
            raise ValueError("Unknown execution or duplicate attempt")
        if not isinstance(attempt, int) or attempt < 1:
            raise ValueError("Invalid attempt number")
        seen.add((key, attempt))
        records[key].append(entry)
    for rows in records.values():
        rows.sort(key=lambda row: row["attempt"])
    return {
        key: {"status": rows[-1]["status"] if rows else "not-run", "attempts": rows}
        for key, rows in records.items()
    }
