from tba_provider_identity_administration_relationship_graph import (
    RelationshipGraph as CanonicalRelationshipGraph,
)
from tba_storage_core.tables import Policy as CanonicalPolicy
from tba_auth.services.advanced_identity_plane import (
    Policy,
    RelationshipGraph,
)


def test_relationship_graph_and_policy_surface_use_table_owned_policy_state():
    assert Policy is CanonicalPolicy
    assert RelationshipGraph is CanonicalRelationshipGraph

    graph = RelationshipGraph()
    initial = graph.define_relation(
        resource_type="document", relation="viewer", subject_types=("user",)
    )
    migrated = graph.define_relation(
        resource_type="document", relation="viewer", subject_types=("group", "user")
    )
    graph.define_relation(
        resource_type="group", relation="member", subject_types=("group", "user")
    )
    graph.add_tuple(
        resource_type="document",
        resource_id="roadmap",
        relation="viewer",
        subject_type="group",
        subject_id="eng",
        tenant_id="tenant-a",
    )
    graph.add_tuple(
        resource_type="group",
        resource_id="eng",
        relation="member",
        subject_type="user",
        subject_id="alice",
        tenant_id="tenant-a",
    )
    graph.add_tuple(
        resource_type="group",
        resource_id="eng",
        relation="member",
        subject_type="group",
        subject_id="staff",
        tenant_id="tenant-a",
    )
    graph.add_tuple(
        resource_type="group",
        resource_id="staff",
        relation="member",
        subject_type="group",
        subject_id="eng",
        tenant_id="tenant-a",
    )

    no_path = graph.check_access(
        tenant_id="tenant-a",
        subject="user:bob",
        relation="viewer",
        resource="document:roadmap",
    )

    assert initial.version == 1
    assert migrated.version == 2
    assert not no_path.allowed
