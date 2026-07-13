from __future__ import annotations

from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from tigrbl_identity_core.standards import StandardOwner, describe_owner


REPO_ROOT = Path(__file__).resolve().parents[2]
PRIMITIVES_STANDARDS_PATH = (
    REPO_ROOT
    / "pkgs"
    / "00-primitives"
    / "tigrbl-identity-core"
    / "src"
    / "tigrbl_identity_core"
    / "standards.py"
)


def test_describe_owner_uses_consistent_payload_shape() -> None:
    owner = StandardOwner(
        label="RFC 0000",
        title="Example Standard",
        runtime_status="example-runtime",
        public_surface=("/example",),
        notes="Example notes.",
    )

    payload = describe_owner(owner, spec_url="https://example.test/spec")

    assert payload == {
        "label": "RFC 0000",
        "title": "Example Standard",
        "runtime_status": "example-runtime",
        "public_surface": ["/example"],
        "notes": "Example notes.",
        "organization": None,
        "version": None,
        "status": None,
        "specification_uri": None,
        "protocol_tags": [],
        "claimable": False,
        "spec_url": "https://example.test/spec",
    }


def test_standard_owner_is_immutable() -> None:
    owner = StandardOwner(
        label="RFC 0000",
        title="Example Standard",
        runtime_status="example-runtime",
        public_surface=("/example",),
        notes="Example notes.",
    )

    with pytest.raises(FrozenInstanceError):
        owner.label = "changed"  # type: ignore[misc]


def test_standard_owner_is_defined_only_in_identity_primitives() -> None:
    definitions = [
        path
        for path in (REPO_ROOT / "pkgs").rglob("*.py")
        if "class StandardOwner" in path.read_text(encoding="utf-8")
    ]

    assert definitions == [PRIMITIVES_STANDARDS_PATH]
