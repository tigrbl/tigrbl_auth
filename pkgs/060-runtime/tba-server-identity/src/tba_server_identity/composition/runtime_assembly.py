"""Default server provider, durable-runtime, capability, and protocol assembly."""

from __future__ import annotations

from typing import Any

from tba_contracts_identity.capabilities import CapabilityDefinition
from tba_contracts_identity.replay import (
    ReplayReservationRequest,
    ReplayReservationResult,
)
from tba_provider_identity_jose.jwt_coder import JWTCoder
from tba_runtime_identity import (
    CapabilityFactory,
    CapabilityRegistry,
    RuntimeCapabilityAssembly,
    build_runtime_capability_assembly,
)
from tba_runtime_identity_storage.ops.replay import check_and_reserve
from tba_capability_artifact_processing import ProtocolArtifactProcessingCapability
from tba_capability_replay_protection import ReplayProtectionCapability


class DatabaseReplayProvider:
    provider_id = "replay:sql"
    persistence = "durable"

    def __init__(self, db: Any) -> None:
        self._db = db

    async def check_and_reserve(
        self,
        request: ReplayReservationRequest,
        /,
    ) -> ReplayReservationResult:
        return await check_and_reserve({"payload": request, "db": self._db})


def _build_server_runtime_assembly(
    settings_obj: object,
    *,
    token_coder: object,
) -> RuntimeCapabilityAssembly:
    def providers() -> dict[str, object]:
        return {"token-coder": token_coder}

    def storage_runtime(provider_set: dict[str, object]) -> dict[str, object]:
        from tba_server_identity.security.client_registration import (
            build_client_registration_capability,
        )
        from tba_server_identity.security.pushed_authorization import (
            build_pushed_authorization_capability,
        )
        from tba_server_identity.security.token_issuance import (
            build_token_issuance_capability,
        )
        from tba_server_identity.platform_tenant_administration import (
            build_tenant_administration_capability,
        )
        from tba_server_identity.platform_realm_administration import (
            build_realm_administration_capability,
        )
        from tba_server_identity.platform_identity_administration import (
            build_identity_administration_capability,
        )
        from tba_server_identity.account_self_service import (
            build_account_self_service_capability,
        )

        token_coder = provider_set["token-coder"]
        return {
            "account-self-service": build_account_self_service_capability,
            "client-registration": build_client_registration_capability,
            "identity-administration": build_identity_administration_capability,
            "pushed-authorization": build_pushed_authorization_capability,
            "replay-provider": DatabaseReplayProvider,
            "realm-administration": build_realm_administration_capability,
            "tenant-administration": build_tenant_administration_capability,
            "token-issuance": lambda db: build_token_issuance_capability(
                db=db,
                token_coder=token_coder,
            ),
        }

    def capabilities(
        provider_set: dict[str, object],
        storage_set: dict[str, object],
    ) -> CapabilityRegistry:
        from tba_server_identity.security.token_introspection import (
            token_introspection,
        )
        from tba_server_identity.security.token_revocation import token_revocation
        from tba_server_identity.token_exchange_runtime import (
            token_exchange_capability,
        )

        registry = CapabilityRegistry(
            (token_introspection, token_revocation, token_exchange_capability)
        )
        registry.register_factory(
            CapabilityFactory(
                CapabilityDefinition("account.self-service", "1.0"),
                (
                    "change_password",
                    "get_profile",
                    "list_authorized_apps",
                    "list_consents",
                    "list_sessions",
                    "revoke_authorized_app",
                    "revoke_consent",
                    "revoke_session",
                    "update_profile",
                ),
                storage_set["account-self-service"],
            )
        )
        registry.register_factory(
            CapabilityFactory(
                CapabilityDefinition("identity-admin.identities", "1.0"),
                (
                    "create_identity",
                    "delete_identity",
                    "list_identities",
                    "read_identity",
                    "update_identity",
                ),
                storage_set["identity-administration"],
            )
        )
        registry.register_factory(
            CapabilityFactory(
                CapabilityDefinition("identity-admin.realms", "1.0"),
                (
                    "create_realm",
                    "create_realm_tenant",
                    "delete_realm",
                    "list_realm_tenants",
                    "list_realms",
                    "read_realm",
                    "update_realm",
                ),
                storage_set["realm-administration"],
            )
        )
        registry.register_factory(
            CapabilityFactory(
                CapabilityDefinition("identity-admin.tenants", "1.0"),
                (
                    "create_tenant",
                    "delete_tenant",
                    "list_tenants",
                    "read_tenant",
                    "update_tenant",
                ),
                storage_set["tenant-administration"],
            )
        )
        registry.register_factory(
            CapabilityFactory(
                CapabilityDefinition("token.issuance", "1.0"),
                ("issue_token_pair", "redeem_refresh_token"),
                storage_set["token-issuance"],
            )
        )
        registry.register_factory(
            CapabilityFactory(
                CapabilityDefinition("oauth.pushed-authorization", "1.0"),
                ("push_authorization_request",),
                storage_set["pushed-authorization"],
            )
        )
        registry.register_factory(
            CapabilityFactory(
                CapabilityDefinition("client.registration", "1.0"),
                (
                    "disable_registration",
                    "get_registration",
                    "register_client",
                    "update_registration",
                ),
                storage_set["client-registration"],
            )
        )
        registry.register_factory(
            CapabilityFactory(
                CapabilityDefinition("security.replay-protection", "1.0"),
                ("check_and_reserve",),
                lambda db: ReplayProtectionCapability(
                    storage_set["replay-provider"](db)
                ),
            )
        )
        registry.register_factory(
            CapabilityFactory(
                CapabilityDefinition("artifact.processing", "1.0"),
                ("decode", "encode", "map_error", "validate"),
                lambda processor: ProtocolArtifactProcessingCapability(processor),
            )
        )
        return registry

    def protocols(registry: CapabilityRegistry):
        from tba_protocol_oauth import capability_report as oauth_report
        from tba_protocol_oidc import capability_report as oidc_report

        return (oauth_report(), oidc_report())

    return build_runtime_capability_assembly(
        build_providers=providers,
        build_storage_runtime=storage_runtime,
        build_capabilities=capabilities,
        build_protocols=protocols,
    )


def build_server_runtime_assembly(
    settings_obj: object,
) -> RuntimeCapabilityAssembly:
    """Build the assembly when no event loop is active."""
    return _build_server_runtime_assembly(
        settings_obj,
        token_coder=JWTCoder.default(),
    )


async def build_server_runtime_assembly_async(
    settings_obj: object,
) -> RuntimeCapabilityAssembly:
    """Build the assembly with event-loop-safe provider initialization."""
    return _build_server_runtime_assembly(
        settings_obj,
        token_coder=await JWTCoder.async_default(),
    )


__all__ = [
    "DatabaseReplayProvider",
    "build_server_runtime_assembly",
    "build_server_runtime_assembly_async",
]
