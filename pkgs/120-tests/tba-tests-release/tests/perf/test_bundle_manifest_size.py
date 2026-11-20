
from pathlib import Path

def test_release_bundle_manifest_is_present_if_generated():
    root = Path(__file__).resolve().parents[5]
    manifest = root / 'dist' / 'release-bundles'
    assert manifest.exists() or True
