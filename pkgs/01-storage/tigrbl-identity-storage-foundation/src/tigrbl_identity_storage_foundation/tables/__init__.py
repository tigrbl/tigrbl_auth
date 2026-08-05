"""Owned mapped-table inventory."""

from .machine_identity import MachineIdentity
from .principal import Principal
from .realm import Realm
from .service_identity import ServiceIdentity
from .subject_alias import SubjectAlias
from .tenant import Tenant
from .user import User

TABLE_MODELS = (
    Realm,
    Tenant,
    User,
    Principal,
    SubjectAlias,
    ServiceIdentity,
    MachineIdentity,
)
TABLE_MODEL_BY_NAME = {model.__name__: model for model in TABLE_MODELS}
TABLE_MODEL_BY_TABLENAME = {model.__tablename__: model for model in TABLE_MODELS}
__all__ = [model.__name__ for model in TABLE_MODELS] + [
    "TABLE_MODELS", "TABLE_MODEL_BY_NAME", "TABLE_MODEL_BY_TABLENAME",
]
