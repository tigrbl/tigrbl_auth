from pathlib import Path
import sys

import tomllib


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


def test_client_layer_is_canonical_and_not_a_facade_or_uix_layer() -> None:
    policy = tomllib.loads((ROOT / "pkgs/layers.toml").read_text(encoding="utf-8"))
    layers = {row["id"]: row for row in policy["layers"]}
    assert layers["75-clients"]["category"] == "client"
    assert layers["75-clients"]["order"] == 75


def test_required_python_and_typescript_clients_live_in_layer_75() -> None:
    expected = {
        "tba-client-authorization-admin",
        "tba-client-policy-decision",
        "tba-client-relying-party-session",
        "tba-typescript-client-oidc-relying-party",
        "tba-typescript-client-relying-party-session",
        "tba-typescript-client-tenant-admin",
        "tba-typescript-client-platform-admin",
        "tba-typescript-client-policy-decision",
    }
    actual = {path.name for path in (ROOT / "pkgs/75-clients").iterdir() if path.is_dir()}
    assert expected <= actual
    assert not (ROOT / "pkgs/105-ui/rp").exists()


def test_architecture_validator_accepts_platform_iam_packages() -> None:
    from scripts.validate_layer_boundaries import validate

    assert validate(ROOT) == ()


def test_server_protocol_router_and_app_packages_are_separate_from_clients() -> None:
    expected = (
        "pkgs/80-routers/tba-router-authorization-admin",
        "pkgs/80-routers/tba-router-policy-decision",
        "pkgs/80-routers/tba-router-relying-party-session",
        "pkgs/90-backend-apps/tba-app-backend-policy-decision",
        "pkgs/90-backend-apps/tba-app-backend-relying-party",
    )
    assert all((ROOT / path).is_dir() for path in expected)
