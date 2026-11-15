"""Guard the published inventory and its native extension."""

import gzip
from hashlib import sha256
import json
import os
from pathlib import Path


def test_frozen_manifest_ids_and_native_projection():
    package = Path(os.environ["TBA_WIMSE_INTEROP_PACKAGE"])
    with gzip.open(package / "matrix/wimse-interop-all-tba-executions.json.gz", "rt", encoding="utf-8") as stream:
        manifest = json.load(stream)
    rows = manifest["workload_executions"] + manifest["planned_executions"]
    ids = {row["id"] for row in rows}
    native_ids = {row["id"] for row in rows if row.get("native_stage")}
    assert len(ids) == len(rows) == manifest["total_runs"] == 142844
    assert sha256("\n".join(sorted(ids)).encode()).hexdigest() == "4c59dbd04c8ff41cee1a33c600daaf0a63ecca3d1e32a6347a171791fb8a198c"
    assert len(native_ids) == 77963
    assert sha256("\n".join(sorted(native_ids)).encode()).hexdigest() == "ad8ca94f01620670c14167c849302aa9264adce251f2fc93845721287290634c"
