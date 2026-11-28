from __future__ import annotations

from types import SimpleNamespace

import pytest

from tba_runtime_identity_storage import crypto_keys
from tba_contracts_security_trust import SignResult, VerifySignatureResult


class _FakeSigningProvider:
    def __init__(self) -> None:
        self.calls: list[object] = []

    async def sign(self, request):
        self.calls.append(request)
        return SignResult(signature=b"sig", alg=request.alg)

    async def verify_signature(self, request):
        self.calls.append(request)
        return VerifySignatureResult(valid=True)


@pytest.mark.asyncio
async def test_storage_runtime_resolves_provider_and_signs_with_allowed_key(monkeypatch) -> None:
    provider = _FakeSigningProvider()
    row = SimpleNamespace(
        kid="kid-1",
        status="active",
        allowed_ops=["sign", "verify"],
        provider="fake",
        provider_key_ref="provider-ref",
        public_material={"kid": "kid-1", "kty": "OKP", "x": "pub"},
    )

    async def _lookup(model, db, filters):
        return row

    monkeypatch.setattr(crypto_keys, "first_record", _lookup)

    result = await crypto_keys.sign(
        object(),
        kid="kid-1",
        payload=b"payload",
        registry={"fake": provider},
        alg="EdDSA",
    )

    assert result.signature == b"sig"
    assert provider.calls[0].key == "provider-ref"


@pytest.mark.asyncio
async def test_storage_runtime_denies_operation_not_allowed_by_row(monkeypatch) -> None:
    provider = _FakeSigningProvider()
    row = SimpleNamespace(
        kid="kid-1",
        status="active",
        allowed_ops=["verify"],
        provider="fake",
        provider_key_ref="provider-ref",
        public_material={"kid": "kid-1", "kty": "OKP", "x": "pub"},
    )

    async def _lookup(model, db, filters):
        return row

    monkeypatch.setattr(crypto_keys, "first_record", _lookup)

    with pytest.raises(PermissionError):
        await crypto_keys.sign(object(), kid="kid-1", payload=b"payload", registry={"fake": provider})

    assert provider.calls == []
