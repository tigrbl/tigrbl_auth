from __future__ import annotations
from tba_auth.services.governance_extension_plane import (
    ScimPatchOperation,
    ScimProvisioningPlane,
)


def test_scim_provisioning_supports_schema_registration_patch_and_group_membership():
    plane = ScimProvisioningPlane()
    plane.register_schema(
        "urn:ietf:params:scim:schemas:core:2.0:User",
        resource_kind="User",
        required_fields=("displayName", "userName"),
    )
    plane.register_schema(
        "urn:ietf:params:scim:schemas:core:2.0:Group",
        resource_kind="Group",
        required_fields=("displayName",),
    )

    user = plane.provision_user(
        "user-1",
        tenant_id="tenant-a",
        user_name="alice",
        attributes={
            "displayName": "Alice",
            "userName": "alice",
            "email": "alice@example.com",
        },
    )
    assert user.attributes["displayName"] == "Alice"

    patched = plane.patch_user(
        "user-1",
        tenant_id="tenant-a",
        operations=(
            ScimPatchOperation(op="replace", path="displayName", value="Alice Example"),
            ScimPatchOperation(op="replace", path="active", value=False),
        ),
    )
    group = plane.provision_group(
        "group-1", tenant_id="tenant-a", display_name="admins", members=("user-1",)
    )
    updated_group = plane.add_group_member(
        "group-1", tenant_id="tenant-a", member_id="user-2"
    )

    snapshot = plane.tenant_snapshot("tenant-a")

    assert patched.attributes["displayName"] == "Alice Example"
    assert not patched.active
    assert group.members == ("user-1",)
    assert updated_group.members == ("user-1", "user-2")
    assert snapshot["schema_ids"] == [
        "urn:ietf:params:scim:schemas:core:2.0:Group",
        "urn:ietf:params:scim:schemas:core:2.0:User",
    ]
    assert snapshot["users"][0]["active"] is False
    assert snapshot["groups"][0]["member_count"] == 2
