from __future__ import annotations

from .models import *
from .models import _utc_now, _utc_now_iso

class ScimProvisioningPlane:
    def __init__(self) -> None:
        self._schemas: dict[str, ScimSchema] = {}
        self._users: dict[str, ScimUser] = {}
        self._groups: dict[str, ScimGroup] = {}

    @property
    def schemas(self) -> Mapping[str, ScimSchema]:
        return dict(self._schemas)

    @property
    def users(self) -> Mapping[str, ScimUser]:
        return dict(self._users)

    @property
    def groups(self) -> Mapping[str, ScimGroup]:
        return dict(self._groups)

    def register_schema(self, schema_id: str, *, resource_kind: str, required_fields: Iterable[str]) -> ScimSchema:
        schema = ScimSchema(
            schema_id=schema_id,
            resource_kind=resource_kind,
            required_fields=tuple(sorted(set(required_fields))),
            registered_at=_utc_now_iso(),
        )
        self._schemas[schema_id] = schema
        return schema

    def provision_user(
        self,
        user_id: str,
        *,
        tenant_id: str,
        user_name: str,
        attributes: Mapping[str, Any],
    ) -> ScimUser:
        schema = next((item for item in self._schemas.values() if item.resource_kind == "User"), None)
        if schema is None:
            raise RuntimeError("user schema must be registered before provisioning users")
        missing_fields = [field for field in schema.required_fields if field not in attributes]
        if missing_fields:
            raise ValueError(f"user payload missing required fields: {', '.join(missing_fields)}")
        user = ScimUser(
            user_id=user_id,
            tenant_id=tenant_id,
            user_name=user_name,
            attributes=dict(attributes),
            created_at=_utc_now_iso(),
        )
        self._users[user_id] = user
        return user

    def patch_user(
        self,
        user_id: str,
        *,
        tenant_id: str,
        operations: Iterable[ScimPatchOperation],
    ) -> ScimUser:
        user = self._users[user_id]
        if user.tenant_id != tenant_id:
            raise PermissionError("user tenant mismatch")
        attributes = dict(user.attributes)
        active = user.active
        for operation in operations:
            if operation.op not in {"add", "replace"}:
                raise ValueError(f"unsupported SCIM patch operation {operation.op!r}")
            if operation.path == "active":
                active = bool(operation.value)
            else:
                attributes[operation.path] = operation.value
        updated = ScimUser(
            user_id=user.user_id,
            tenant_id=user.tenant_id,
            user_name=str(attributes.get("userName", user.user_name)),
            attributes=attributes,
            created_at=user.created_at,
            active=active,
        )
        self._users[user_id] = updated
        return updated

    def provision_group(
        self,
        group_id: str,
        *,
        tenant_id: str,
        display_name: str,
        members: Iterable[str] = (),
    ) -> ScimGroup:
        schema = next((item for item in self._schemas.values() if item.resource_kind == "Group"), None)
        if schema is None:
            raise RuntimeError("group schema must be registered before provisioning groups")
        group = ScimGroup(
            group_id=group_id,
            tenant_id=tenant_id,
            display_name=display_name,
            members=tuple(sorted(set(members))),
            created_at=_utc_now_iso(),
        )
        self._groups[group_id] = group
        return group

    def add_group_member(self, group_id: str, *, tenant_id: str, member_id: str) -> ScimGroup:
        group = self._groups[group_id]
        if group.tenant_id != tenant_id:
            raise PermissionError("group tenant mismatch")
        updated = replace(group, members=tuple(sorted(set(group.members + (member_id,)))))
        self._groups[group_id] = updated
        return updated

    def tenant_snapshot(self, tenant_id: str) -> dict[str, Any]:
        users = [user for user in self._users.values() if user.tenant_id == tenant_id]
        groups = [group for group in self._groups.values() if group.tenant_id == tenant_id]
        return {
            "tenant_id": tenant_id,
            "schema_ids": sorted(self._schemas),
            "users": [
                {
                    "id": user.user_id,
                    "user_name": user.user_name,
                    "active": user.active,
                }
                for user in sorted(users, key=lambda item: item.user_id)
            ],
            "groups": [
                {
                    "id": group.group_id,
                    "display_name": group.display_name,
                    "member_count": len(group.members),
                }
                for group in sorted(groups, key=lambda item: item.group_id)
            ],
        }

    def summary(self) -> dict[str, Any]:
        return {
            "schema_count": len(self._schemas),
            "user_count": len(self._users),
            "group_count": len(self._groups),
        }


class EntitlementManager:
    def __init__(self) -> None:
        self._definitions: dict[str, EntitlementDefinition] = {}
        self._assignments: dict[str, EntitlementAssignment] = {}

    @property
    def definitions(self) -> Mapping[str, EntitlementDefinition]:
        return dict(self._definitions)

    @property
    def assignments(self) -> Mapping[str, EntitlementAssignment]:
        return dict(self._assignments)

    def define_entitlement(
        self,
        entitlement_id: str,
        *,
        tenant_id: str,
        name: str,
        owner: str,
        description: str,
    ) -> EntitlementDefinition:
        definition = EntitlementDefinition(
            entitlement_id=entitlement_id,
            tenant_id=tenant_id,
            name=name,
            owner=owner,
            description=description,
            created_at=_utc_now_iso(),
        )
        self._definitions[entitlement_id] = definition
        return definition

    def assign_entitlement(
        self,
        entitlement_id: str,
        *,
        subject_id: str,
        justification: str,
        assigned_by: str,
        expires_at: str | None = None,
    ) -> EntitlementAssignment:
        definition = self._definitions[entitlement_id]
        assignment = EntitlementAssignment(
            assignment_id=f"ent-{uuid4().hex}",
            entitlement_id=entitlement_id,
            tenant_id=definition.tenant_id,
            subject_id=subject_id,
            justification=justification,
            assigned_by=assigned_by,
            created_at=_utc_now_iso(),
            expires_at=expires_at,
        )
        self._assignments[assignment.assignment_id] = assignment
        return assignment

    def revoke_assignment(self, assignment_id: str, *, reason: str) -> EntitlementAssignment:
        assignment = self._assignments[assignment_id]
        updated = replace(assignment, active=False, revoked_reason=reason)
        self._assignments[assignment_id] = updated
        return updated

    def expire_assignments(self, *, reference_time: datetime | None = None) -> tuple[str, ...]:
        now = reference_time or _utc_now()
        expired: list[str] = []
        for assignment_id, assignment in list(self._assignments.items()):
            if not assignment.active or assignment.expires_at is None:
                continue
            if datetime.fromisoformat(assignment.expires_at) <= now:
                self.revoke_assignment(assignment_id, reason="entitlement expired")
                expired.append(assignment_id)
        return tuple(sorted(expired))

    def tenant_inventory(self, tenant_id: str) -> dict[str, Any]:
        definitions = [definition for definition in self._definitions.values() if definition.tenant_id == tenant_id]
        assignments = [assignment for assignment in self._assignments.values() if assignment.tenant_id == tenant_id]
        return {
            "tenant_id": tenant_id,
            "entitlements": [
                {
                    "id": definition.entitlement_id,
                    "name": definition.name,
                    "owner": definition.owner,
                }
                for definition in sorted(definitions, key=lambda item: item.entitlement_id)
            ],
            "assignments": [
                {
                    "id": assignment.assignment_id,
                    "entitlement_id": assignment.entitlement_id,
                    "subject_id": assignment.subject_id,
                    "active": assignment.active,
                    "expires_at": assignment.expires_at,
                }
                for assignment in sorted(assignments, key=lambda item: item.assignment_id)
            ],
        }

    def summary(self) -> dict[str, Any]:
        return {
            "definition_count": len(self._definitions),
            "assignment_count": len(self._assignments),
            "active_assignment_count": sum(1 for assignment in self._assignments.values() if assignment.active),
        }


