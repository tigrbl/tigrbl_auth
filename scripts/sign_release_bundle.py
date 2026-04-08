from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tigrbl_auth.cli.artifacts import deployment_from_options
from tigrbl_auth.cli.reports import build_release_bundle, sign_release_bundle
from tigrbl_auth.release_signing import load_signer


PROFILES = ("baseline", "production", "hardening", "fapi2-security", "peer-claim")


def _version(repo_root: Path) -> str:
    pyproject = repo_root / "pyproject.toml"
    for line in pyproject.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("version") and "=" in line:
            return line.split("=", 1)[1].strip().strip('"')
    return "0.0.0"


def main() -> int:
    payloads = []
    shared_signer = load_signer(signing_key=os.environ.get("TIGRBL_AUTH_RELEASE_SIGNING_KEY"), signer_id=os.environ.get("TIGRBL_AUTH_RELEASE_SIGNER_ID"))
    shared_signing_key = shared_signer.private_key_pem()
    version = _version(ROOT)
    for profile in PROFILES:
        deployment = deployment_from_options(profile=profile)
        bundle_dir = ROOT / "dist" / "release-bundles" / version / deployment.profile
        if not bundle_dir.exists():
            build_release_bundle(ROOT, deployment, bundle_dir=bundle_dir)
        payload = sign_release_bundle(bundle_dir, signing_key=shared_signing_key, signer_id=shared_signer.identity.signer_id)
        payloads.append({"profile": profile, **payload})
    print(json.dumps({"signed_bundles": payloads}, indent=2))
    return 0 if all(item.get("verification", {}).get("passed", False) for item in payloads) else 1


if __name__ == "__main__":
    raise SystemExit(main())
