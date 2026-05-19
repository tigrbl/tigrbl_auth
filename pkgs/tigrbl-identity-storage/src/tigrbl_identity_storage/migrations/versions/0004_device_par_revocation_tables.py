"""Executable DDL migration for 0004_device_par_revocation_tables."""

from tigrbl_auth.migrations.helpers import create_tables, drop_tables
from tigrbl_auth.tables import DeviceCode, PushedAuthorizationRequest, RevokedToken

revision = '0004_device_par_revocation_tables'
down_revision = '0003_authorization_runtime_tables'
branch_labels = None
depends_on = None


def upgrade(conn) -> None:
    create_tables(conn, DeviceCode, PushedAuthorizationRequest, RevokedToken)


def downgrade(conn) -> None:
    drop_tables(conn, DeviceCode, PushedAuthorizationRequest, RevokedToken)
