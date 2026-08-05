"""Owned mapped-table inventory."""

from .dpop_nonce import DpopNonce
from .dpop_replay import DpopReplay
from .replay_reservation import ReplayReservation

TABLE_MODELS = (
    ReplayReservation,
    DpopReplay,
    DpopNonce,
)
TABLE_MODEL_BY_NAME = {model.__name__: model for model in TABLE_MODELS}
TABLE_MODEL_BY_TABLENAME = {model.__tablename__: model for model in TABLE_MODELS}
__all__ = [model.__name__ for model in TABLE_MODELS] + [
    "TABLE_MODELS", "TABLE_MODEL_BY_NAME", "TABLE_MODEL_BY_TABLENAME",
]
