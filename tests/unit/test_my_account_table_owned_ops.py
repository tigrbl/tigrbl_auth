from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MY_ACCOUNT_ROOT = ROOT / "pkgs" / "tigrbl-auth-backend-app-my-account" / "src"


def test_my_account_api_does_not_implement_durable_storage_ops() -> None:
    offenders: list[str] = []
    forbidden = ("handlers.create.core", "handlers.update.core", "handlers.delete.core", "upsert_token_record_async")
    for path in MY_ACCOUNT_ROOT.rglob("*.py"):
        source = path.read_text(encoding="utf-8")
        for token in forbidden:
            if token in source:
                offenders.append(f"{path.relative_to(ROOT).as_posix()} uses {token}")

    assert offenders == []

