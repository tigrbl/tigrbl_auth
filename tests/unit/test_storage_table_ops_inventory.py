from __future__ import annotations

import ast
from pathlib import Path


TABLES_DIR = (
    Path(__file__).resolve().parents[2]
    / "pkgs"
    / "01-storage"
    / "tigrbl-identity-storage"
    / "src"
    / "tigrbl_identity_storage"
    / "tables"
)


REQUIRED_TABLE_OPS = {
    "auth_session.py": {
        "AuthSession": {
            "create_for_user",
            "list_for_user",
            "revoke_all_for_user",
            "revoke_for_user",
            "touch",
        }
    },
    "consent.py": {
        "Consent": {"grant", "list_for_user", "revoke_for_client", "revoke_for_user"}
    },
    "token_record.py": {
        "TokenRecord": {
            "list_active_for_subject",
            "mark_rotated",
            "persist_issued_token",
            "revoke_family",
        }
    },
    "revoked_token.py": {"RevokedToken": {"revoke_token", "is_revoked"}},
    "auth_code.py": {"AuthCode": {"expire", "consume"}},
    "device_code.py": {"DeviceCode": {"approve", "consume", "poll", "deny"}},
    "pushed_authorization_request.py": {
        "PushedAuthorizationRequest": {
            "consume",
            "consume_request",
            "create_request",
            "resolve_request_uri",
        }
    },
    "client.py": {
        "Client": {
            "verify_secret",
            "disable",
            "new",
            "rotate_secret",
            "authenticate",
            "enable",
        }
    },
    "client_registration.py": {
        "ClientRegistration": {
            "delete_registration",
            "read_registration",
            "register_client",
            "update_registration",
        }
    },
    "audit_event.py": {"AuditEvent": {"record", "list_for_subject", "list_for_tenant"}},
    "logout_state.py": {"LogoutState": {"expire", "consume_logout", "create_logout"}},
    "realm.py": {"Realm": {"update_realm"}},
    "tenant.py": {"Tenant": {"update_tenant", "disable_tenant"}},
    "user.py": {
        "User": {
            "update_user",
            "list_by_tenant",
            "create_user",
            "lookup_by_identifier",
            "disable_user",
        }
    },
    "principal.py": {
        "Principal": {"create_principal", "lookup", "disable", "list_for_tenant"}
    },
    "service_identity.py": {
        "ServiceIdentity": {"lookup", "disable", "list_for_tenant"}
    },
    "machine_identity.py": {
        "MachineIdentity": {"lookup", "disable", "list_for_tenant"}
    },
    "workload_identity.py": {
        "WorkloadIdentity": {"lookup", "disable", "list_for_tenant"}
    },
    "delegation_grant.py": {
        "DelegationGrant": {
            "activate_grant",
            "create_grant",
            "expire_grant",
            "inspect_grant",
            "list_grants",
            "replace_grant",
            "revoke_grant",
        },
        "DelegationGrantProof": {"persist_provenance"},
        "DelegationGrantTokenLink": {"link_token", "list_for_grant"},
    },
    "crypto_key.py": {
        "CryptoKey": {
            "create_key",
            "lookup_by_kid",
            "rotate_record",
            "list_active",
            "retire",
        }
    },
    "crypto_key_version.py": {
        "CryptoKeyVersion": {
            "activate",
            "create_version",
            "export_public_material",
            "lookup",
            "retire",
        }
    },
    "principal_key_binding.py": {
        "PrincipalKeyBinding": {
            "lookup",
            "revoke",
            "list_for_principal",
            "list_for_key",
        }
    },
    "key_envelope.py": {"KeyEnvelope": {"lookup_by_label"}},
    "credential.py": {
        "Credential": {
            "list_for_principal",
            "rotate",
            "lookup_active",
            "revoke",
            "create_credential",
        }
    },
    "credential_api_key.py": {"CredentialApiKey": {"lookup_active"}},
    "credential_service_key.py": {"CredentialServiceKey": {"lookup_active"}},
    "credential_password.py": {
        "CredentialPassword": {"revoke", "list_for_principal", "lookup_active"}
    },
    "credential_client_secret.py": {
        "CredentialClientSecret": {"revoke", "list_for_principal", "lookup_active"}
    },
    "credential_webauthn_passkey.py": {
        "CredentialWebAuthnPasskey": {"revoke", "list_for_principal"}
    },
    "credential_mfa_factor.py": {
        "CredentialMfaFactor": {"lookup", "list_for_principal", "revoke"}
    },
    "credential_recovery_code.py": {
        "CredentialRecoveryCode": {
            "consume",
            "list_for_principal",
            "lookup_active",
            "revoke",
        }
    },
    "credential_audit_event.py": {
        "CredentialAuditEvent": {"record", "list_for_principal"}
    },
    "credential_mtls_certificate.py": {
        "CredentialMtlsCertificate": {"revoke", "list_for_principal"}
    },
    "credential_dpop_key.py": {"CredentialDpopKey": {"revoke", "list_for_principal"}},
    "tenant_membership.py": {
        "TenantMembership": {
            "grant_membership",
            "list_for_principal",
            "lookup",
            "revoke_membership",
        }
    },
    "subject_alias.py": {
        "SubjectAlias": {"lookup", "list_for_principal", "verify_alias", "bind_alias"}
    },
    "role.py": {"Role": {"lookup", "disable", "create_role", "list_for_tenant"}},
    "attribute_policy.py": {
        "AttributePolicy": {
            "create_policy",
            "disable",
            "list_active",
            "list_for_permission",
            "lookup",
        }
    },
    "policy_condition.py": {
        "PolicyCondition": {"replace_for_policy", "list_for_policy", "add_condition"}
    },
    "delegated_admin_scope.py": {
        "DelegatedAdminScope": {"lookup", "grant_scope", "revoke_scope", "list_active"}
    },
    "key_rotation_policy.py": {
        "KeyRotationPolicy": {
            "approve",
            "create_policy_version",
            "list_for_tenant",
            "lookup_version",
            "publish",
        }
    },
    "entitlement.py": {
        "Entitlement": {"disable", "lookup", "define", "list_for_tenant"}
    },
    "entitlement_assignment.py": {
        "EntitlementAssignment": {"assign", "lookup", "revoke", "list_for_subject"}
    },
    "access_review_campaign.py": {
        "AccessReviewCampaign": {
            "lookup",
            "list_for_tenant",
            "close",
            "create_campaign",
        }
    },
    "access_review_item.py": {
        "AccessReviewItem": {"lookup", "mark_decided", "create_item"}
    },
    "residency_zone.py": {
        "ResidencyZone": {"lookup", "create_zone", "disable", "list_active"}
    },
    "tenant_residency.py": {
        "TenantResidency": {"lookup", "assign_residency", "disable"}
    },
    "sdk_package.py": {"SDKPackageRecord": {"lookup", "disable", "register"}},
    "plugin_descriptor.py": {
        "PluginDescriptorRecord": {"lookup", "disable", "register"}
    },
    "plugin_lifecycle_event.py": {
        "PluginLifecycleEventRecord": {"lookup", "append_event"}
    },
    "scim_schema.py": {"ScimSchemaRecord": {"lookup", "disable", "register_schema"}},
    "scim_user.py": {
        "ScimUserRecord": {"lookup", "deactivate", "upsert_user", "list_for_tenant"}
    },
    "scim_group.py": {
        "ScimGroupRecord": {"lookup", "upsert_group", "deactivate", "list_for_tenant"}
    },
    "scim_patch_event.py": {"ScimPatchEvent": {"append_event", "list_for_tenant"}},
    "release_capability_record.py": {"ReleaseCapabilityRecord": {"record", "lookup"}},
    "release_authorization_state.py": {
        "ReleaseAuthorizationState": {"lookup", "snapshot"}
    },
    "runtime_qualification.py": {"RuntimeQualificationRecord": {"record", "lookup"}},
    "release_security_posture.py": {"ReleaseSecurityPosture": {"lookup", "snapshot"}},
    "release_posture.py": {"ReleasePosture": {"lookup", "snapshot"}},
    "release_attestation_event.py": {
        "ReleaseAttestationEvent": {"lookup", "append_event"}
    },
    "control_correctness_report.py": {
        "ControlCorrectnessReport": {"lookup", "snapshot"}
    },
    "resource_server_contract.py": {
        "ResourceServerContract": {"lookup", "disable", "register"}
    },
    "provider_artifact.py": {"ProviderArtifact": {"lookup", "disable", "register"}},
}


DEFAULT_OP_COLLAPSE_SPECIMENS = {
    "access_review_decision.py": {"AccessReviewDecision"},
    "authz_verification_report.py": {"AuthzVerificationReport"},
}


DEFAULT_OP_COLLAPSED_METHODS = {
    "access_review_item.py": {"AccessReviewItem": {"list_for_campaign"}},
    "auth_code.py": {"AuthCode": {"create_for_authorization"}},
    "control_correctness_report.py": {"ControlCorrectnessReport": {"list_for_release"}},
    "credential_audit_event.py": {"CredentialAuditEvent": {"list_for_credential"}},
    "credential_client_secret.py": {"CredentialClientSecret": {"bind_secret"}},
    "credential_dpop_key.py": {
        "CredentialDpopKey": {"bind_key", "lookup_by_thumbprint"}
    },
    "credential_mfa_factor.py": {"CredentialMfaFactor": {"bind_factor"}},
    "credential_mtls_certificate.py": {
        "CredentialMtlsCertificate": {"lookup_by_thumbprint", "bind_certificate"}
    },
    "credential_password.py": {"CredentialPassword": {"bind_password"}},
    "credential_recovery_code.py": {"CredentialRecoveryCode": {"bind_code"}},
    "credential_webauthn_passkey.py": {
        "CredentialWebAuthnPasskey": {"bind_passkey", "lookup_by_credential_id"}
    },
    "crypto_key.py": {"CryptoKey": {"enable", "disable"}},
    "crypto_key_version.py": {"CryptoKeyVersion": {"list_for_key"}},
    "device_code.py": {"DeviceCode": {"create_device_authorization"}},
    "key_attestation_evidence.py": {
        "KeyAttestationEvidence": {"mark_verified", "list_for_key", "record_evidence"}
    },
    "key_envelope.py": {
        "KeyEnvelope": {"list_for_wrapping_key", "record_envelope", "disable"}
    },
    "machine_identity.py": {
        "MachineIdentity": {"create_identity", "lookup_by_subject"}
    },
    "plugin_descriptor.py": {"PluginDescriptorRecord": {"list_enabled"}},
    "plugin_lifecycle_event.py": {"PluginLifecycleEventRecord": {"list_for_plugin"}},
    "principal.py": {"Principal": {"list_by_kind", "lookup_by_subject"}},
    "principal_key_binding.py": {"PrincipalKeyBinding": {"bind_key"}},
    "provider_artifact.py": {"ProviderArtifact": {"list_by_kind"}},
    "realm.py": {"Realm": {"create_realm", "lookup_by_slug", "list_realms"}},
    "release_attestation_event.py": {"ReleaseAttestationEvent": {"list_for_release"}},
    "release_authorization_state.py": {
        "ReleaseAuthorizationState": {"list_for_release"}
    },
    "release_capability_record.py": {"ReleaseCapabilityRecord": {"list_for_release"}},
    "release_posture.py": {"ReleasePosture": {"list_for_release"}},
    "release_security_posture.py": {"ReleaseSecurityPosture": {"list_for_release"}},
    "resource_server_contract.py": {
        "ResourceServerContract": {"list_for_resource_server"}
    },
    "runtime_qualification.py": {"RuntimeQualificationRecord": {"list_for_release"}},
    "scim_patch_event.py": {"ScimPatchEvent": {"list_for_resource"}},
    "scim_schema.py": {"ScimSchemaRecord": {"list_for_resource_kind"}},
    "sdk_package.py": {"SDKPackageRecord": {"list_by_language"}},
    "service_identity.py": {"ServiceIdentity": {"create_identity"}},
    "tenant.py": {"Tenant": {"create_tenant", "list_by_realm", "lookup_by_name"}},
    "tenant_residency.py": {"TenantResidency": {"list_for_zone"}},
    "workload_identity.py": {
        "WorkloadIdentity": {"create_identity", "lookup_by_subject"}
    },
}


def _decorator_name(decorator: ast.expr) -> str:
    target = decorator.func if isinstance(decorator, ast.Call) else decorator
    if isinstance(target, ast.Name):
        return target.id
    if isinstance(target, ast.Attribute):
        return target.attr
    return ""


def _class_methods(path: Path, class_name: str) -> set[str]:
    module = ast.parse(path.read_text(encoding="utf-8"))
    for node in module.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            return {
                item.name
                for item in node.body
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
            }
    raise AssertionError(f"{class_name} not found in {path}")


def _classmethods(path: Path, class_name: str) -> set[str]:
    module = ast.parse(path.read_text(encoding="utf-8"))
    for node in module.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            names: set[str] = set()
            for item in node.body:
                if not isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    continue
                if any(
                    _decorator_name(decorator) == "classmethod"
                    for decorator in item.decorator_list
                ):
                    names.add(item.name)
            return names
    raise AssertionError(f"{class_name} not found in {path}")


def test_storage_tables_own_required_operation_methods() -> None:
    missing: list[str] = []

    for filename, class_requirements in REQUIRED_TABLE_OPS.items():
        path = TABLES_DIR / filename
        if not path.exists():
            path = TABLES_DIR / filename.removesuffix(".py") / "_table.py"
        for class_name, operation_names in class_requirements.items():
            defined = _class_methods(path, class_name)
            for name in sorted(operation_names - defined):
                missing.append(f"{class_name}.{name}")

    assert missing == []


def test_default_op_collapse_specimens_do_not_define_semantic_table_ops() -> None:
    offenders: list[str] = []
    for filename, class_names in DEFAULT_OP_COLLAPSE_SPECIMENS.items():
        path = TABLES_DIR / filename.removesuffix(".py") / "_table.py"
        for class_name in class_names:
            for method_name in sorted(_class_methods(path, class_name)):
                offenders.append(f"{class_name}.{method_name}")
            for method_name in sorted(_classmethods(path, class_name)):
                offenders.append(f"{class_name}.{method_name}")

    for filename, class_methods in DEFAULT_OP_COLLAPSED_METHODS.items():
        path = TABLES_DIR / filename.removesuffix(".py") / "_table.py"
        for class_name, method_names in class_methods.items():
            defined = _class_methods(path, class_name)
            classmethods = _classmethods(path, class_name)
            for method_name in sorted(method_names):
                if method_name in defined or method_name in classmethods:
                    offenders.append(f"{class_name}.{method_name}")

    assert offenders == []
