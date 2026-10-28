from __future__ import annotations

import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
PACKAGE_DIR = ROOT / "pkgs" / "75-clients" / "tba-typescript-client-oidc-relying-party"


def test_typescript_rp_t0_package_scaffold_and_workspace_membership() -> None:
    root_manifest = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    manifest = json.loads((PACKAGE_DIR / "package.json").read_text(encoding="utf-8"))

    assert "pkgs/75-clients/tba-typescript-client-oidc-relying-party" in root_manifest["workspaces"]
    assert manifest["name"] == "@tba/client-oidc-relying-party"
    assert manifest["type"] == "module"
    assert manifest["exports"]["."]["import"] == "./dist/index.js"
    assert manifest["exports"]["."]["types"] == "./dist/index.d.ts"
    assert manifest["repository"]["directory"] == "pkgs/75-clients/tba-typescript-client-oidc-relying-party"
    assert {"build", "test"} <= set(manifest["scripts"])
    assert (PACKAGE_DIR / "README.md").exists()
    assert (PACKAGE_DIR / "src" / "index.ts").exists()


def test_typescript_rp_t1_node_matrix_workflow_includes_package() -> None:
    workflow = yaml.safe_load((ROOT / ".github" / "workflows" / "package-node-matrix.yml").read_text(encoding="utf-8"))
    text = (ROOT / ".github" / "workflows" / "package-node-matrix.yml").read_text(encoding="utf-8")
    on = workflow.get("on") or workflow.get(True)

    assert "@tba/client-oidc-relying-party" in on["workflow_dispatch"]["inputs"]["package"]["options"]
    assert '"pkgs/75-clients/tba-typescript-client-oidc-relying-party"' in text
    assert 'npm run test -w ${manifest.name}' in text
    assert 'npm run build -w ${manifest.name}' in text


def test_typescript_rp_t2_npm_release_workflow_uses_provenance() -> None:
    workflow_text = (ROOT / ".github" / "workflows" / "monorepo-npm-package-release.yml").read_text(encoding="utf-8")
    manifest = json.loads((PACKAGE_DIR / "package.json").read_text(encoding="utf-8"))

    assert "@tba/client-oidc-relying-party" in workflow_text
    assert '"pkgs/75-clients/tba-typescript-client-oidc-relying-party"' in workflow_text
    assert "cobycloud/actions/actions/npm-publish@" in workflow_text
    assert "cobycloud/actions/actions/npm-publish@main" not in workflow_text
    assert 'provenance: "true"' in workflow_text
    assert manifest["publishConfig"]["access"] == "public"
    assert manifest["publishConfig"]["provenance"] is True
