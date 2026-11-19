"""Owned mapped-table inventory."""

from .federated_session import FederatedSession
from .federation import Federation
from .identity_provider import IdentityProvider
from .provider_artifact import ProviderArtifact

TABLE_MODELS = (
    ProviderArtifact,
    IdentityProvider,
    Federation,
    FederatedSession,
)
TABLE_MODEL_BY_NAME = {model.__name__: model for model in TABLE_MODELS}
TABLE_MODEL_BY_TABLENAME = {model.__tablename__: model for model in TABLE_MODELS}
__all__ = [model.__name__ for model in TABLE_MODELS] + [
    "TABLE_MODELS", "TABLE_MODEL_BY_NAME", "TABLE_MODEL_BY_TABLENAME",
]
