import pytest
from tigrbl import bind
from tigrbl_auth.tables import User


@pytest.mark.unit
def test_register_op_has_request_and_response_schema():
    bind(User)
    register_schema = getattr(User.schemas, "register", None) or getattr(User.schemas, "create", None)
    assert register_schema is not None
    assert hasattr(register_schema, "in_")
    assert hasattr(register_schema, "out")
