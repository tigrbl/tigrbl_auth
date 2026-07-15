from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.validate_layer_boundaries import CAPABILITY_PURPOSES, validate


def test_layer_40_contains_only_registered_multi_component_use_cases() -> None:
    assert CAPABILITY_PURPOSES == {
        "tigrbl-attestation-appraisal": (
            "coordinate evidence appraisal and result recording"
        ),
        "tigrbl-client-registration-capability": (
            "coordinate client and registration metadata lifecycle with optional "
            "audit recording"
        ),
        "tigrbl-digital-credential-issuance": (
            "coordinate credential configuration, wallet trust, offers, and issuance"
        ),
        "tigrbl-digital-credential-presentation": (
            "coordinate holder consent, replay defense, and presentation verification"
        ),
        "tigrbl-identity-admin-control-plane": (
            "coordinate administrative resource lifecycle use cases"
        ),
        "tigrbl-grant-negotiation-capability": (
            "coordinate negotiated grant requests, continuation, and token rotation"
        ),
        "tigrbl-protocol-artifact-processing": (
            "coordinate protocol-neutral artifact decoding, validation, encoding, "
            "and error normalization through replaceable processors"
        ),
        "tigrbl-principal-authentication": (
            "coordinate durable principal lookup with replaceable credential verifiers"
        ),
        "tigrbl-policy-evaluation-capability": (
            "coordinate normalized policy evaluation, batch evaluation, entity search, "
            "and service description"
        ),
        "tigrbl-pushed-authorization-capability": (
            "coordinate durable pushed-request creation with optional audit recording"
        ),
        "tigrbl-protected-resource-authorization-capability": (
            "coordinate normalized protected-resource token and claims authorization"
        ),
        "tigrbl-replay-protection-capability": (
            "coordinate normalized replay reservations across protocol mappings, "
            "durable repositories, and replaceable providers"
        ),
        "tigrbl-security-events": (
            "coordinate security-event transmission, receipt, and recording"
        ),
        "tigrbl-token-introspection-capability": (
            "coordinate protocol-neutral token-state lookup and profile validation"
        ),
        "tigrbl-token-issuance-capability": (
            "coordinate token-pair issuance and refresh rotation across signing and "
            "durable lifecycle operations"
        ),
        "tigrbl-token-revocation-capability": (
            "coordinate durable token revocation with optional audit recording"
        ),
        "tigrbl-token-exchange-capability": (
            "coordinate normalized security-token exchange across verification, "
            "issuance, durable lineage, and audit operations"
        ),
        "tigrbl-workload-identity": (
            "coordinate workload credential retrieval and identity verification"
        ),
    }


def test_layer_40_dependency_import_and_inheritance_boundaries() -> None:
    assert validate() == ()


def test_every_layer_40_readme_declares_the_capability_contract() -> None:
    capability_root = ROOT / "pkgs" / "40-capabilities"
    required_sections = (
        "## Injected dependencies",
        "## Operations and readiness",
        "## Protocol consumers",
        "## Non-goals",
    )

    for package in capability_root.iterdir():
        if not package.is_dir():
            continue
        readme = (package / "README.md").read_text(encoding="utf-8")
        missing = tuple(
            section for section in required_sections if section not in readme
        )
        assert not missing, f"{package.name} README missing sections: {missing}"


def test_layer_40_capabilities_do_not_construct_mutable_instance_stores() -> None:
    capability_root = ROOT / "pkgs" / "40-capabilities"
    mutable_constructors = {"dict", "list", "set", "defaultdict"}
    violations = []

    for source in capability_root.rglob("*.py"):
        tree = ast.parse(source.read_text(encoding="utf-8-sig"), filename=str(source))
        for node in ast.walk(tree):
            if not isinstance(node, (ast.Assign, ast.AnnAssign)):
                continue
            targets = node.targets if isinstance(node, ast.Assign) else (node.target,)
            value = node.value
            mutable_value = isinstance(value, (ast.Dict, ast.List, ast.Set)) or (
                isinstance(value, ast.Call)
                and isinstance(value.func, ast.Name)
                and value.func.id in mutable_constructors
            )
            if not mutable_value:
                continue
            for target in targets:
                if (
                    isinstance(target, ast.Attribute)
                    and isinstance(target.value, ast.Name)
                    and target.value.id == "self"
                ):
                    violations.append(
                        f"{source.relative_to(ROOT)}:{node.lineno}: self.{target.attr}"
                    )

    assert violations == []
