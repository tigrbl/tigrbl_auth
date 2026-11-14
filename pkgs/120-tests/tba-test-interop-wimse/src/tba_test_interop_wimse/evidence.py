"""Reconcile evidence without replacing earlier attempts."""
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
