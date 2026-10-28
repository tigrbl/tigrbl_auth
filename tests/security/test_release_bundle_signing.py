from pathlib import Path

from tba_auth.cli.artifacts import deployment_from_options
from tba_auth.cli.reports import build_release_bundle, sign_release_bundle, verify_release_bundle_signatures


def test_release_bundle_signing_manifest_created():
    root = Path(__file__).resolve().parents[2]
    bundle = build_release_bundle(root, deployment_from_options(profile='baseline'), bundle_dir=root / 'dist' / 'test-release-bundle')
    payload = sign_release_bundle(bundle, signing_key='test-key')
    assert payload['status'].startswith('signed')
    assert payload['algorithm'] == 'Ed25519'
    assert payload['verification']['passed'] is True
    assert (bundle / 'attestations' / 'release-attestation.json').exists()
    verified = verify_release_bundle_signatures(bundle)
    assert verified['passed'] is True
