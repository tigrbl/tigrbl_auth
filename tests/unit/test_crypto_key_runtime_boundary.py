from __future__ import annotations

import uuid

import pytest

from tigrbl_identity_storage.tables import CryptoKey, CryptoKeyVersion
from tigrbl_identity_storage_runtime import (
    CryptoKeyRuntimeSpec,
    CryptoKeyVersionRuntimeSpec,
    create_table_record,
    ensure_key_enabled,
    initializeIdentityRuntimeTables,
    normalize_key_usage_policy,
    seed_primary_key_version,
)


def _activate(monkeypatch, storage) -> None:
    initializeIdentityRuntimeTables(
        (CryptoKeyRuntimeSpec, CryptoKeyVersionRuntimeSpec)
    )
    for model in (CryptoKey, CryptoKeyVersion):
        runtime_handlers = model.handlers
        handlers = storage.handlers_for(model)
        for name, value in vars(runtime_handlers).items():
            if not hasattr(handlers, name):
                setattr(handlers, name, value)
        monkeypatch.setattr(model, "handlers", handlers, raising=False)


@pytest.mark.asyncio
async def test_key_usage_normalization_is_a_pre_handler_hook() -> None:
    context = {
        "payload": {
            "key_kind": "symmetric",
            "key_usages": ["kek"],
            "allowed_ops": ["wrap_key"],
        }
    }
    await normalize_key_usage_policy(context)
    assert context["payload"] == {
        "key_kind": "symmetric",
        "key_usages": ["kek"],
        "allowed_ops": ["wrap_key"],
    }


@pytest.mark.asyncio
async def test_primary_version_seed_is_idempotent(
    monkeypatch,
    administrator_storage,
) -> None:
    _activate(monkeypatch, administrator_storage)
    key = await create_table_record(
        CryptoKey,
        administrator_storage,
        {
            "id": uuid.uuid4(),
            "kid": "key-a",
            "algorithm": "EdDSA",
            "status": "active",
            "primary_version": 3,
            "allowed_ops": ["sign", "verify"],
            "public_material": {"kty": "OKP", "x": "public"},
            "provider_key_ref": "provider:key-a:3",
        },
    )
    context = {"result": key, "db": administrator_storage}

    await seed_primary_key_version(context)
    await seed_primary_key_version(context)

    versions = administrator_storage._bucket(CryptoKeyVersion)
    assert len(versions) == 1
    assert versions[0]["key_id"] == key["id"]
    assert versions[0]["version"] == 3
    assert versions[0]["provider_key_ref"] == "provider:key-a:3"


@pytest.mark.asyncio
async def test_rotation_guard_rejects_disabled_or_unknown_keys(
    monkeypatch,
    administrator_storage,
) -> None:
    _activate(monkeypatch, administrator_storage)
    await create_table_record(
        CryptoKey,
        administrator_storage,
        {
            "kid": "disabled-key",
            "algorithm": "EdDSA",
            "status": "disabled",
        },
    )
    with pytest.raises(LookupError, match="active crypto key not found"):
        await ensure_key_enabled(
            {
                "payload": {"kid": "disabled-key"},
                "db": administrator_storage,
            }
        )
    with pytest.raises(LookupError, match="active crypto key not found"):
        await ensure_key_enabled(
            {"payload": {"kid": "missing"}, "db": administrator_storage}
        )


@pytest.mark.asyncio
async def test_rotation_guard_stashes_active_key(
    monkeypatch,
    administrator_storage,
) -> None:
    _activate(monkeypatch, administrator_storage)
    key = await create_table_record(
        CryptoKey,
        administrator_storage,
        {"kid": "active-key", "algorithm": "EdDSA", "status": "active"},
    )
    context = {"payload": {"kid": "active-key"}, "db": administrator_storage}
    await ensure_key_enabled(context)
    assert context["crypto_key"] == key


def test_runtime_activation_installs_key_hook_order() -> None:
    initializeIdentityRuntimeTables((CryptoKeyRuntimeSpec,))
    hooks = {
        hook.name: hook
        for hook in CryptoKey.HOOKS
        if hook.name in {
            "normalize_key_usage_policy",
            "seed_primary_key_version",
            "ensure_key_enabled",
        }
    }
    assert tuple(hook.name for hook in CryptoKeyRuntimeSpec.hooks) == (
        "normalize_key_usage_policy",
        "seed_primary_key_version",
        "ensure_key_enabled",
    )
    assert set(hooks) == {
        "normalize_key_usage_policy",
        "seed_primary_key_version",
        "ensure_key_enabled",
    }
    assert hooks["normalize_key_usage_policy"].ops == ("create", "update")
    assert hooks["seed_primary_key_version"].ops == "create"
    assert hooks["ensure_key_enabled"].ops == "rotate_record"


def test_layer01_key_models_export_no_runtime_helpers() -> None:
    for model in (CryptoKey, CryptoKeyVersion):
        assert not hasattr(model, "normalize_key_usage_policy")
        assert not hasattr(model, "seed_primary_key_version")
        assert not hasattr(model, "ensure_key_enabled")
        assert not hasattr(model, "scrub_key_material")
