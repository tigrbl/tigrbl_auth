from importlib.resources import files
from pathlib import Path

from tba_storage_core import collect_migration_revisions

versions = Path(str(files("tba_storage_core").joinpath("migrations", "versions")))
revisions = collect_migration_revisions(versions)
assert revisions
print(f"{len(revisions)} packaged revisions")
