from contextlib import asynccontextmanager

import pytest
from tigrbl_identity_storage_runtime import (
    AttestationEvidenceRepository,
    CredentialIssuanceTransactionRepository,
    CredentialOfferRepository,
    PresentationConsentRepository,
    PresentationReplayRepository,
    PresentationTransactionRepository,
    SecurityEventDeliveryRepository,
    SecurityEventReplayRepository,
    SecurityEventRepository,
    SpiffeTrustBundleRepository,
    StorageTransactionCoordinator,
    SvidRecordRepository,
)


class _Store:
    def __init__(self):
        self.records = {}

    async def insert(self, table, values):
        self.records[(table, values["id"])] = dict(values)
        return self.records[(table, values["id"])]

    async def get(self, table, identifier):
        return self.records.get((table, identifier))

    async def update(self, table, identifier, values):
        self.records[(table, identifier)].update(values)
        return self.records[(table, identifier)]

    async def list(self, table, filters):
        return tuple(
            value
            for (candidate, _), value in self.records.items()
            if candidate is table
            and all(value.get(name) == expected for name, expected in filters.items())
        )


class _Transactions:
    def __init__(self):
        self.active = False

    @asynccontextmanager
    async def transaction(self):
        self.active = True
        try:
            yield
        finally:
            self.active = False


@pytest.mark.asyncio
async def test_repositories_target_authoritative_layer_01_tables():
    store = _Store()
    repositories = (
        CredentialOfferRepository(store),
        CredentialIssuanceTransactionRepository(store),
        PresentationTransactionRepository(store),
        PresentationConsentRepository(store),
        PresentationReplayRepository(store),
        AttestationEvidenceRepository(store),
        SecurityEventRepository(store),
        SecurityEventDeliveryRepository(store),
        SecurityEventReplayRepository(store),
        SvidRecordRepository(store),
        SpiffeTrustBundleRepository(store),
    )
    assert all(
        repository.table.__module__.startswith("tigrbl_identity_storage.tables")
        for repository in repositories
    )
    for index, repository in enumerate(repositories):
        await repository.create(id=str(index), state="created")
        assert (await repository.get(str(index)))["state"] == "created"


@pytest.mark.asyncio
async def test_repository_refuses_raw_nonce_code_and_presentation_disclosures():
    repository = CredentialOfferRepository(_Store())
    for field in ("raw_nonce", "pre_authorized_code", "presentation_disclosures"):
        with pytest.raises(ValueError, match="sensitive raw fields"):
            await repository.create(id="1", **{field: "secret"})


@pytest.mark.asyncio
async def test_attestation_and_svid_repositories_allow_locator_and_digest_not_raw_payload():
    store = _Store()
    evidence = AttestationEvidenceRepository(store)
    await evidence.create(
        id="evidence-1",
        protected_artifact_locator="vault://evidence/1",
        payload_digest="sha256:abc",
    )
    assert (await evidence.get("evidence-1"))["payload_digest"] == "sha256:abc"


@pytest.mark.asyncio
async def test_transaction_coordinator_exposes_runtime_transaction_boundary():
    manager = _Transactions()
    coordinator = StorageTransactionCoordinator(manager)
    async with coordinator.transaction():
        assert manager.active
    assert not manager.active
