"""Create the operator tables that were mapped but absent from revisions 0001-0036."""

from tigrbl_identity_storage.migrations.helpers import create_tables, drop_tables
from tigrbl_identity_storage_operator.tables import (
    OperatorActivity,
    OperatorAuditEvent,
    OperatorMetadata,
    OperatorRecord,
    OperatorTransaction,
)

revision = "0037_operator_tables"
down_revision = "0036_workload_credentials_artifacts_and_proof_replay"
branch_labels = None
depends_on = None
TABLES = (
    OperatorMetadata,
    OperatorRecord,
    OperatorTransaction,
    OperatorAuditEvent,
    OperatorActivity,
)


def upgrade(conn) -> None:
    create_tables(conn, *TABLES)


def downgrade(conn) -> None:
    drop_tables(conn, *reversed(TABLES))
