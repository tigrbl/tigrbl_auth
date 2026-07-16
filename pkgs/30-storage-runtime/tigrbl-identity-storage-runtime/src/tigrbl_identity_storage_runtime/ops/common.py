"""Compatibility facade for neutral durable table handler helpers."""

from tigrbl_identity_core.clock import utc_now
from tigrbl_identity_core.digests import token_hash
from tigrbl_table_durability import *

coerce_uuid_value = normalize_identifier
normalize_uuid_identifier = normalize_identifier


field = field_value
record_id = record_identifier
create_record = create_handler_record = create_table_record
read_record = read_handler_record = read_table_record
update_record = update_handler_record = update_table_record
delete_record = delete_handler_record = delete_table_record
list_records = list_handler_records = list_table_records
first_record = first_handler_record = first_table_record
clear_records = clear_handler_records = clear_table_records

__all__ = [name for name in globals() if not name.startswith("_")]
