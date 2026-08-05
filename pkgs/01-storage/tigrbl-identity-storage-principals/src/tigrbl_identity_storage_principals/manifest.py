"""Installed component manifest access."""
from importlib.resources import as_file, files
from tigrbl_migrations import StorageManifest

def load_manifest() -> StorageManifest:
    with as_file(files(__package__).joinpath("component.toml")) as path:
        return StorageManifest.from_toml(path)

MANIFEST = load_manifest()
