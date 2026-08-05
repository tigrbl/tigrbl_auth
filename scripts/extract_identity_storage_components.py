"""Materialize independently installable identity-storage component packages.

The mapping below is the reviewed ownership boundary.  Running this script is
idempotent: source models are copied from the frozen compatibility package,
while manifests, baseline revisions, and dependency declarations are derived
deterministically from that mapping and the model sources.
"""

from __future__ import annotations

import ast
import shutil
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STORAGE = ROOT / "pkgs/01-storage"
LEGACY = STORAGE / "tigrbl-identity-storage/src/tigrbl_identity_storage/tables"
NAMESPACE = uuid.UUID("72ced0b5-f90a-47ba-b7d5-da70a6b62d4f")

COMPONENTS: dict[str, tuple[str, ...]] = {
    "foundation": ("Realm", "Tenant", "User", "Principal", "SubjectAlias", "ServiceIdentity", "MachineIdentity"),
    "authentication": ("Credential", "CredentialApiKey", "CredentialServiceKey", "CredentialAuditEvent", "CredentialClientSecret", "CredentialDpopKey", "CredentialMfaFactor", "CredentialMtlsCertificate", "CredentialPassword", "CredentialRecoveryCode", "AuthenticationChallenge"),
    "oauth": ("Client", "ClientRegistration", "AuthorizationServer", "AuthSession", "AuthCode", "DeviceCode", "RevokedToken", "PushedAuthorizationRequest"),
    "oidc": ("LogoutState", "BackchannelLogoutReplay"),
    "token": ("TokenRecord", "ProtectedArtifactReference", "PossessionProofReplay"),
    "consent": ("Consent",),
    "delegation": ("DelegationGrant", "DelegationGrantScope", "DelegationGrantProof", "DelegationGrantEdge", "DelegationGrantTokenLink"),
    "key-material": ("CryptoKey", "CryptoKeyVersion", "PrincipalKeyBinding", "KeyEnvelope", "KeyAttestationEvidence", "KeyRotationEvent", "KeyRotationPolicy"),
    "authorization-policy": ("TenantMembership", "Role", "AttributePolicy", "PolicyCondition", "Policy", "PolicyVersion", "PolicySet", "PolicySetMember", "PolicyTarget", "DelegatedAdminScope", "AuthorizationInvariant", "InvariantEvaluation", "InvariantViolation"),
    "access-governance": ("Entitlement", "EntitlementAssignment", "AccessReviewCampaign", "AccessReviewItem", "AccessReviewDecision"),
    "residency": ("ResidencyZone", "TenantResidency"),
    "audit": ("AuditEvent",),
    "federation": ("ProviderArtifact", "IdentityProvider", "Federation", "FederatedSession"),
    "digital-credential": ("CredentialIssuer", "CredentialConfiguration", "WalletRegistration", "WalletInstance", "WalletAttestation", "WalletKeyBinding", "CredentialOffer", "CredentialIssuanceTransaction", "CredentialDeferredTransaction", "CredentialNotification", "CredentialStatusList", "CredentialStatusEntry", "CredentialStatusPublication"),
    "presentation": ("VerifierRegistration", "PresentationTransaction", "PresentationConsent", "PresentationReplay"),
    "attestation": ("AttestationEvidence", "AttestationResult", "AttestationReferenceManifest", "AttestationReferenceValue", "AttestationEndorsement", "AttestationAppraisalPolicy"),
    "workload-identity": ("WorkloadIdentity", "SvidRecord", "SpiffeTrustBundle", "TrustDomainFederation", "WorkloadReferenceBinding", "WorkloadCredentialEntitlement"),
    "security-event": ("SecurityEvent", "SecurityEventSubscription", "SecurityEventDelivery", "SecurityEventReplay"),
    "replay-protection": ("ReplayReservation", "DpopReplay", "DpopNonce"),
    "did": ("DidDocument", "DidDocumentVersion", "DidVerificationMethod", "DidService", "DidResolutionCache"),
    "gnap": ("GnapGrant", "GnapContinuation", "GnapClientInstance", "GnapInteraction"),
    "certificate": ("CertificateRecord", "TrustAnchor", "CertificateStatusSnapshot"),
    "claims": ("ClaimDefinition", "ClaimSourceBinding", "ClaimReleasePolicy", "ClaimProvenanceRecord", "ClaimSnapshot"),
    "webauthn": ("CredentialWebAuthnPasskey", "WebAuthnAttestationRecord", "WebAuthnCeremony", "WebAuthnRelyingParty"),
    "authority-graph": ("AuthorityDerivationGraph", "AuthorityDerivationGraphNode", "AuthorityDerivationGraphEdge"),
    "trust-federation-graph": ("TrustFederationGraph", "TrustFederationGraphNode", "TrustFederationGraphEdge"),
    "scim": ("ScimSchemaRecord", "ScimUserRecord", "ScimGroupRecord", "ScimPatchEvent"),
    "release-governance": ("SDKPackageRecord", "PluginDescriptorRecord", "PluginLifecycleEventRecord", "ReleaseCapabilityRecord", "ReleaseAuthorizationState", "RuntimeQualificationRecord", "ReleaseSecurityPosture", "ReleasePosture", "ReleaseAttestationEvent", "ControlCorrectnessReport", "AuthzVerificationReport", "ResourceServerContract"),
    "operator": ("OperatorMetadata", "OperatorRecord", "OperatorTransaction", "OperatorAuditEvent", "OperatorActivity"),
}


def _sources() -> tuple[dict[str, Path], dict[str, str], dict[str, object]]:
    by_class: dict[str, Path] = {}
    table_names: dict[str, str] = {}
    for path in LEGACY.rglob("*.py"):
        if path.name in {"__init__.py", "_registry.py"}:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in tree.body:
            if not isinstance(node, ast.ClassDef):
                continue
            by_class[node.name] = path
            for statement in node.body:
                if not isinstance(statement, ast.Assign):
                    continue
                if any(isinstance(target, ast.Name) and target.id == "__tablename__" for target in statement.targets):
                    if isinstance(statement.value, ast.Constant) and isinstance(statement.value.value, str):
                        table_names[node.name] = statement.value.value
    sys.path[:0] = [
        str(STORAGE / "tigrbl-identity-storage/src"),
        str(STORAGE / "tigrbl-identity-storage-core/src"),
        *(
            str(path / "src")
            for path in STORAGE.glob("tigrbl-identity-storage-*")
            if (path / "src").is_dir()
        ),
    ]
    from tigrbl_identity_storage.tables import TABLE_MODELS

    models = {model.__name__: model for model in TABLE_MODELS}
    table_names.update({name: model.__tablename__ for name, model in models.items()})
    return by_class, table_names, models


def _revision(component: str) -> str:
    return str(uuid.uuid5(NAMESPACE, f"tigrbl.identity.storage.{component}:baseline:v1"))


def _rewrite(text: str, import_root: str) -> str:
    text = text.replace("tigrbl_identity_storage.framework", "tigrbl_identity_storage_core.framework")
    text = text.replace("tigrbl_identity_storage.tables._graph_base", f"{import_root}.tables._graph_base")
    return text.rstrip() + "\n"


def _split_mixed(path: Path, selected: set[str], import_root: str) -> str:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    tree.body = [
        node
        for node in tree.body
        if not isinstance(node, ast.ClassDef) or node.name in selected
    ]
    tree.body = [
        node
        for node in tree.body
        if not (
            isinstance(node, ast.Assign)
            and any(isinstance(target, ast.Name) and target.id == "__all__" for target in node.targets)
        )
    ]
    return "# ruff: noqa: F401\n" + _rewrite(
        ast.unparse(ast.fix_missing_locations(tree)) + "\n", import_root
    )


def _toml_string(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def main() -> None:
    by_class, table_names, models = _sources()
    owner_by_table = {
        table_names[class_name]: component
        for component, classes in COMPONENTS.items()
        for class_name in classes
    }
    expected = {name for names in COMPONENTS.values() for name in names}
    missing = expected - by_class.keys()
    if missing:
        raise SystemExit(f"mapped classes without source tables: {sorted(missing)}")

    for component, classes in COMPONENTS.items():
        slug = component
        import_root = "tigrbl_identity_storage_" + slug.replace("-", "_")
        distribution = "tigrbl-identity-storage-" + slug
        component_id = "tigrbl.identity.storage." + slug
        package_root = STORAGE / distribution
        source_root = package_root / "src" / import_root
        tables_root = source_root / "tables"
        migrations_root = source_root / "migrations" / "versions"
        tables_root.mkdir(parents=True, exist_ok=True)
        migrations_root.mkdir(parents=True, exist_ok=True)

        source_files = {by_class[name] for name in classes}
        for path in sorted(source_files):
            relative = path.relative_to(LEGACY)
            if relative.parts[-1] == "_table.py":
                source_dir = path.parent
                target_dir = tables_root / source_dir.name
                if target_dir.exists():
                    shutil.rmtree(target_dir)
                shutil.copytree(source_dir, target_dir)
                for copied in target_dir.rglob("*.py"):
                    copied.write_text(_rewrite(copied.read_text(encoding="utf-8"), import_root), encoding="utf-8")
            else:
                target = tables_root / path.name
                selected = {name for name in classes if by_class[name] == path}
                all_classes = {name for name, candidate in by_class.items() if candidate == path}
                if selected != all_classes:
                    target.write_text(_split_mixed(path, selected, import_root), encoding="utf-8")
                else:
                    target.write_text(_rewrite(path.read_text(encoding="utf-8"), import_root), encoding="utf-8")

        if component in {"authority-graph", "trust-federation-graph"}:
            graph_base = LEGACY / "_graph_base.py"
            (tables_root / "_graph_base.py").write_text(
                _rewrite(graph_base.read_text(encoding="utf-8"), import_root), encoding="utf-8"
            )

        imports: dict[str, list[str]] = {}
        for class_name in classes:
            relative = by_class[class_name].relative_to(LEGACY)
            module = relative.parts[0] if relative.name == "_table.py" else relative.stem
            imports.setdefault(module, []).append(class_name)
        registry_lines = ['"""Owned mapped-table inventory."""', ""]
        for module, names in sorted(imports.items()):
            registry_lines.append(f"from .{module} import {', '.join(names)}")
        registry_lines.extend([
            "",
            "TABLE_MODELS = (",
            *(f"    {name}," for name in classes),
            ")",
            "TABLE_MODEL_BY_NAME = {model.__name__: model for model in TABLE_MODELS}",
            "TABLE_MODEL_BY_TABLENAME = {model.__tablename__: model for model in TABLE_MODELS}",
            "__all__ = [model.__name__ for model in TABLE_MODELS] + [",
            '    "TABLE_MODELS", "TABLE_MODEL_BY_NAME", "TABLE_MODEL_BY_TABLENAME",',
            "]",
            "",
        ])
        (tables_root / "__init__.py").write_text("\n".join(registry_lines), encoding="utf-8")

        dependency_components: set[str] = set()
        for class_name in classes:
            for foreign_key in models[class_name].__table__.foreign_keys:
                referenced = foreign_key.target_fullname.rsplit(".", 1)[0].rsplit(".", 1)[-1]
                owner = owner_by_table.get(referenced)
                if owner is not None and owner != component:
                    dependency_components.add(owner)

        revision = _revision(component)
        manifest_lines = [
            'manifest_version = "1.0.0"',
            "",
            "[component]",
            f"id = {_toml_string(component_id)}",
            f"distribution = {_toml_string(distribution)}",
            f"import_root = {_toml_string(import_root)}",
            "",
            "[schema]",
            'contract = "1.0.0"',
            f"migration_head = {_toml_string(revision)}",
            f"migrations_package = {_toml_string(import_root + '.migrations.versions')}",
        ]
        for class_name in classes:
            table_name = table_names[class_name]
            physical_name = models[class_name].__table__.fullname
            manifest_lines.extend([
                "",
                "[[schema.objects]]",
                f"id = {_toml_string(component_id + ':table:' + table_name)}",
                'kind = "table"',
                f"physical_name = {_toml_string(physical_name)}",
                f"model = {_toml_string(import_root + '.tables:' + class_name)}",
            ])
        for dependency in sorted(dependency_components):
            manifest_lines.extend([
                "",
                "[[schema.requires]]",
                f"component = {_toml_string('tigrbl.identity.storage.' + dependency)}",
                'contract = ">=1.0.0,<2.0.0"',
                f"minimum_revision = {_toml_string(_revision(dependency))}",
            ])
        manifest_text = "\n".join(manifest_lines) + "\n"
        (package_root / "component.toml").write_text(manifest_text, encoding="utf-8")
        (source_root / "component.toml").write_text(manifest_text, encoding="utf-8")

        dependency_dists = ["tigrbl-identity-storage-" + item for item in sorted(dependency_components)]
        dependency_rows = [
            '    "tigrbl>=0.4.4.dev1,<0.5",',
            '    "tigrbl-migrations>=0.4.5.dev4",',
            '    "tigrbl-identity-storage-core>=0.4.0.dev2",',
            *(f'    "{item}>=0.4.0.dev2",' for item in dependency_dists),
        ]
        pyproject = f'''[project]
name = "{distribution}"
version = "0.4.0.dev2"
description = "Owned {component} identity database tables and migrations."
readme = "README.md"
requires-python = ">=3.10,<3.15"
license = {{ text = "Apache-2.0" }}
dependencies = [
{chr(10).join(dependency_rows)}
]

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"

[tool.poetry]
packages = [{{ include = "{import_root}", from = "src" }}]
include = ["src/{import_root}/component.toml"]
'''
        (package_root / "pyproject.toml").write_text(pyproject, encoding="utf-8")
        (package_root / "README.md").write_text(
            f"# {distribution}\n\nOwns the `{component_id}` schema component.\n", encoding="utf-8"
        )
        (source_root / "manifest.py").write_text(
            '''"""Installed component manifest access."""
from importlib.resources import as_file, files
from tigrbl_migrations import StorageManifest

def load_manifest() -> StorageManifest:
    with as_file(files(__package__).joinpath("component.toml")) as path:
        return StorageManifest.from_toml(path)

MANIFEST = load_manifest()
''', encoding="utf-8"
        )
        (source_root / "__init__.py").write_text(
            '"""Standalone identity storage component."""\n\nfrom .manifest import MANIFEST, load_manifest\nfrom .tables import *  # noqa: F401,F403\nfrom .tables import TABLE_MODEL_BY_NAME, TABLE_MODEL_BY_TABLENAME, TABLE_MODELS\n\n__all__ = ["MANIFEST", "load_manifest", "TABLE_MODELS", "TABLE_MODEL_BY_NAME", "TABLE_MODEL_BY_TABLENAME"] + [model.__name__ for model in TABLE_MODELS]\n',
            encoding="utf-8",
        )
        (source_root / "py.typed").write_text("", encoding="utf-8")
        (source_root / "migrations" / "__init__.py").write_text("", encoding="utf-8")
        (migrations_root / "__init__.py").write_text("", encoding="utf-8")
        migration_module = f'''"""Initial owned schema for {component_id}."""
from tigrbl_migrations import Migration
from {import_root}.tables import TABLE_MODELS

REVISION = "{revision}"

def upgrade(connection):
    for model in TABLE_MODELS:
        model.__table__.create(bind=connection, checkfirst=True)

def downgrade(connection):
    for model in reversed(TABLE_MODELS):
        model.__table__.drop(bind=connection, checkfirst=True)

MIGRATION = Migration(
    component="{component_id}",
    revision=REVISION,
    parents=(),
    kind="standard",
    reversible=True,
    upgrade=upgrade,
    downgrade=downgrade,
)
'''
        (migrations_root / (revision.replace("-", "_") + "_initial_schema.py")).write_text(
            migration_module, encoding="utf-8"
        )

    compatibility = [
        '"""Compatibility projection of independently owned storage components."""',
        "# ruff: noqa: F401,F403",
        "",
        "from tigrbl_identity_storage_core.framework import RestOltpTable",
    ]
    for component, classes in COMPONENTS.items():
        import_root = "tigrbl_identity_storage_" + component.replace("-", "_")
        compatibility.append(f"from {import_root}.tables import {', '.join(classes)}")
    compatibility.extend(
        [
            "from tigrbl_identity_storage_oauth.tables.client import _CLIENT_ID_RE",
            "from tigrbl_identity_storage_delegation.tables.delegation_grant import DelegationGrantRecord",
            "",
            "_TABLE_MODELS = (",
            *(f"    {name}," for names in COMPONENTS.values() for name in names),
            ")",
            "",
        ]
    )
    (LEGACY / "_registry.py").write_text("\n".join(compatibility), encoding="utf-8")

    from tigrbl_migrations import DeploymentLock, StorageComposition, StorageManifest

    manifests = tuple(
        StorageManifest.from_toml(STORAGE / ("tigrbl-identity-storage-" + component) / "component.toml")
        for component in COMPONENTS
    )
    composition = StorageComposition.from_manifests(*manifests)
    lock = DeploymentLock.from_composition(
        composition,
        artifact_versions={manifest.component_id: "0.4.0.dev2" for manifest in manifests},
    )
    (LEGACY.parent / "storage.lock.toml").write_text(lock.to_toml(), encoding="utf-8")


if __name__ == "__main__":
    main()
