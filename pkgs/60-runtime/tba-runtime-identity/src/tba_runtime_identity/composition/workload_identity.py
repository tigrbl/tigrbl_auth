from dataclasses import dataclass
from typing import Mapping

@dataclass(frozen=True, slots=True)
class WorkloadIdentityRuntimeConfig:
    enable_spiffe_x509_svid: bool = False
    enable_spiffe_jwt_svid: bool = False
    enable_spiffe_workload_api: bool = False
    enable_spiffe_broker_api: bool = False
    enable_wimse_wit: bool = False
    enable_wimse_wpt: bool = False
    enable_spiffe_wit_svid: bool = False
    enable_cwt_svid_extension: bool = False
    workload_api_version: str = "SPIFFE-Workload-API-1.0"
    broker_api_version: str = "SPIFFE-v1.15.1-Broker-API"
    wit_version: str = "draft-ietf-wimse-workload-creds-02"
    wpt_version: str = "draft-ietf-wimse-wpt-01"
    wit_svid_version: str = "SPIFFE-v1.15.1-WIT-SVID"
    cwt_svid_extension_version: str = "TIGRBL-CWT-SVID-EXPERIMENT-1"
    workload_endpoint: str | None = None
    broker_endpoint: str | None = None
    broker_authorized_principals: tuple[str, ...] = ()

@dataclass(frozen=True, slots=True)
class WorkloadIdentityComposition:
    active_profiles: tuple[str, ...]
    dependencies: Mapping[str, object]

def build_workload_identity_composition(config: WorkloadIdentityRuntimeConfig, *, dependencies: Mapping[str, object]) -> WorkloadIdentityComposition:
    if config.enable_spiffe_workload_api and (config.workload_api_version != "SPIFFE-Workload-API-1.0" or not config.workload_endpoint):
        raise ValueError("Workload API requires exact revision and local endpoint")
    if config.enable_spiffe_broker_api and (config.broker_api_version != "SPIFFE-v1.15.1-Broker-API" or not config.broker_endpoint or not config.broker_authorized_principals):
        raise ValueError("Broker API requires exact Incubating revision, endpoint, and authorized principals")
    if config.enable_spiffe_wit_svid and not (config.enable_wimse_wit and config.enable_wimse_wpt):
        raise ValueError("WIT-SVID requires both WIT and WPT profiles")
    expected = {
        "wit": "draft-ietf-wimse-workload-creds-02",
        "wpt": "draft-ietf-wimse-wpt-01",
        "wit-svid": "SPIFFE-v1.15.1-WIT-SVID",
        "cwt-svid-extension": "TIGRBL-CWT-SVID-EXPERIMENT-1",
    }
    selected = {
        "wit": (config.enable_wimse_wit, config.wit_version),
        "wpt": (config.enable_wimse_wpt, config.wpt_version),
        "wit-svid": (config.enable_spiffe_wit_svid, config.wit_svid_version),
        "cwt-svid-extension": (config.enable_cwt_svid_extension, config.cwt_svid_extension_version),
    }
    for name, (enabled, revision) in selected.items():
        if enabled and revision != expected[name]: raise ValueError(f"{name} requires exact revision {expected[name]}")
    active = [name for name, (enabled, _) in selected.items() if enabled]
    if config.enable_spiffe_x509_svid: active.append("x509-svid")
    if config.enable_spiffe_jwt_svid: active.append("jwt-svid")
    if config.enable_spiffe_workload_api: active.append("spiffe-workload-api")
    if config.enable_spiffe_broker_api: active.append("spiffe-broker-api")
    required = {"credential_provider", "credential_verifier"} if active else set()
    missing = required.difference(dependencies)
    if missing: raise ValueError(f"missing workload composition dependencies: {sorted(missing)}")
    return WorkloadIdentityComposition(tuple(active), dict(dependencies))