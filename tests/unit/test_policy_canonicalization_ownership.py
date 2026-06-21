from __future__ import annotations

import ast
from pathlib import Path

from tigrbl_authz_policy import provenance, replay
from tigrbl_identity_core.json_canonicalization import canonical_hash, canonical_json


ROOT = Path(__file__).resolve().parents[2]


def test_policy_canonicalization_helpers_are_owned_by_identity_core() -> None:
    assert provenance.canonical_json is canonical_json
    assert provenance.canonical_hash is canonical_hash
    assert replay.canonical_json is canonical_json
    assert replay.canonical_hash is canonical_hash
    assert canonical_json({"b": 2, "a": 1}) == '{"a":1,"b":2}'
    assert canonical_json({"values": ("z", "a")}) == '{"values":["z","a"]}'
    assert canonical_json({"values": {"z", "a"}}) == '{"values":["a","z"]}'


def test_authz_policy_no_longer_defines_canonicalization_helpers() -> None:
    helper_names = {"_normalize", "canonical_json", "canonical_hash"}
    for relative_path in (
        "pkgs/40-capabilities/tigrbl-authz-policy/src/tigrbl_authz_policy/provenance.py",
        "pkgs/40-capabilities/tigrbl-authz-policy/src/tigrbl_authz_policy/replay.py",
    ):
        tree = ast.parse((ROOT / relative_path).read_text(encoding="utf-8"))
        defined = {
            node.name
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        assert not (defined & helper_names), relative_path
