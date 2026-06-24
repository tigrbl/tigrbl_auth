from __future__ import annotations

__all__: list[str] = []

# BEGIN classmethod-to-op_ctx migration
from tigrbl import op_ctx as _table_op_ctx
from . import _table as _table_module

for _table_name in dir(_table_module):
    if not _table_name.startswith("__"):
        globals().setdefault(_table_name, getattr(_table_module, _table_name))

async def _lookup(cls, db: Any, *, campaign_id: str) -> "AccessReviewCampaign | None":
    return await first_record(cls, db, {"campaign_id": campaign_id})

@_table_op_ctx(bind=AccessReviewCampaign, alias="close", target="custom", rest=False)
async def close(cls, db: Any, *, campaign_id: str) -> "AccessReviewCampaign | None":
    row = await _lookup(cls, db, campaign_id=campaign_id)
    if row is None:
        return None
    return await update_record(cls, db, record_id(row), {"status": "closed", "closed_at": utc_now()})

# END classmethod-to-op_ctx migration
