from __future__ import annotations

from tigrbl_identity_contracts.protocol_processing import ArtifactProcessingResult
from tigrbl_identity_runtime.settings import settings
from tigrbl_identity_server.api.runtime_assembly import (
    DatabaseReplayProvider,
    build_server_runtime_assembly,
)


class ArtifactProcessor:
    def decode(self, request):
        return ArtifactProcessingResult(True, request.encoded)

    def validate(self, request):
        return ArtifactProcessingResult(True, request.encoded)

    def encode(self, request):
        return ArtifactProcessingResult(True, request.encoded)

    def map_error(self, error):
        return ArtifactProcessingResult(False, errors=(str(error),))


def test_server_assembly_maps_selected_protocols_to_effective_capabilities() -> None:
    assembly = build_server_runtime_assembly(settings)

    assert assembly.construction_order == (
        "providers",
        "storage-runtime",
        "capabilities",
        "protocols",
    )
    assert tuple(report["protocol"] for report in assembly.protocols) == (
        "oauth",
        "oidc",
    )
    assert assembly.capabilities.capability_ids() == (
        "artifact.processing",
        "client.registration",
        "identity-admin.realms",
        "identity-admin.tenants",
        "oauth.pushed-authorization",
        "security.replay-protection",
        "token.exchange",
        "token.introspection",
        "token.issuance",
        "token.revocation",
    )


def test_server_assembly_materializes_database_and_processor_scoped_capabilities() -> (
    None
):
    assembly = build_server_runtime_assembly(settings)
    registry = assembly.capabilities
    db = object()

    materialized = {
        "artifact.processing": registry.materialize(
            "artifact.processing", ArtifactProcessor()
        ),
        "client.registration": registry.materialize("client.registration", db),
        "identity-admin.realms": registry.materialize("identity-admin.realms", db),
        "identity-admin.tenants": registry.materialize("identity-admin.tenants", db),
        "oauth.pushed-authorization": registry.materialize(
            "oauth.pushed-authorization", db
        ),
        "security.replay-protection": registry.materialize(
            "security.replay-protection", db
        ),
        "token.issuance": registry.materialize("token.issuance", db),
    }

    assert {
        capability_id: capability.definition().capability_id
        for capability_id, capability in materialized.items()
    } == {capability_id: capability_id for capability_id in materialized}
    assert isinstance(
        materialized["security.replay-protection"]._provider,
        DatabaseReplayProvider,
    )
    report = registry.report()["capabilities"]
    assert all(
        report[capability_id]["lifetime"] == "request-scoped"
        for capability_id in materialized
    )
