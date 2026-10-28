from __future__ import annotations

import importlib

from tba_capability_artifact_processing import ProtocolArtifactProcessingCapability


PROTOCOL_MODULES = (
    "tba_protocol_attestation_corim",
    "tba_protocol_attestation_eat",
    "tba_profile_haip",
    "tba_protocol_authzen",
    "tba_protocol_cwt",
    "tba_protocol_gnap",
    "tba_protocol_jwt",
    "tba_protocol_oauth",
    "tba_protocol_oid4vci",
    "tba_protocol_oid4vp",
    "tba_protocol_oidc",
    "tba_protocol_oidc_relying_party",
    "tba_protocol_authorization_resource_server",
    "tba_profile_credential_sd_jwt_vc",
    "tba_protocol_security_event_set",
)


class _Processor:
    def decode(self, request):
        return request

    def validate(self, request):
        return request

    def encode(self, request):
        return request

    def map_error(self, error):
        return error


def test_protocol_artifact_capability_is_normalized_and_fully_reported() -> None:
    capability = ProtocolArtifactProcessingCapability(_Processor())
    report = capability.capability_report()
    assert report["capability_id"] == "artifact.processing"
    assert report["operations"] == ("decode", "validate", "encode", "map_error")
    assert report["delegated_operations"] == tuple(sorted(report["operations"]))
    assert "unsupported" not in report


def test_each_versioned_protocol_reports_revision_requirements_coverage_and_evidence() -> (
    None
):
    for module_name in PROTOCOL_MODULES:
        module = importlib.import_module(module_name)
        report = module.capability_report()
        assert report["protocol"]
        assert report["selected_revision"]
        assert report["features"]
        assert report["required_capabilities"]
        assert report["requirements"]
        assert report["effective_coverage"]
        assert report["evidence_links"]
        assert "unsupported" not in report
        requirement_ids = {item.requirement_id for item in report["requirements"]}
        assert requirement_ids == set(report["effective_coverage"])
        assert all(item.capability_id for item in report["requirements"])
        assert all(item.operation for item in report["requirements"])
